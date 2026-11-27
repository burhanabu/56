# WhisperPhone - Kokoro offline TTS server (sirf aapke apne PC par, internet nahi chahiye)
# App isay khud chalati hai. Files exe ke saath: kokoro.onnx, voices.bin
# Pehli baar:  pip install kokoro-onnx numpy      (install_kokoro.bat double-click)
import sys, os, json, threading
import numpy as np
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 5005
MODEL = os.path.join(HERE, "kokoro.onnx")
VOICES = os.path.join(HERE, "voices.bin")

# 24000 Hz -> 8000 Hz (telephone). Pehle low-pass (aliasing se bachne ke liye), phir har 3rd sample.
def _lowpass_taps(n=63, cutoff=3600.0, fs=24000.0):
    m = np.arange(n) - (n - 1) / 2.0
    h = np.sinc(2 * cutoff / fs * m) * (2 * cutoff / fs)
    h *= np.hamming(n)
    return h / h.sum()
TAPS = _lowpass_taps()

def to_8k_pcm16(samples, sr):
    x = np.asarray(samples, dtype=np.float32).reshape(-1)
    if sr != 24000:                      # kokoro hamesha 24000 deta hai; safety ke liye
        t = np.arange(0, len(x) * 8000.0 / sr) * (sr / 8000.0)
        x = np.interp(t, np.arange(len(x)), x).astype(np.float32)
        return np.clip(x * 32767.0 * 0.9, -32768, 32767).astype("<i2").tobytes()
    y = np.convolve(x, TAPS, mode="same")[::3]
    peak = float(np.max(np.abs(y))) if len(y) else 0.0
    if peak > 0.98:
        y = y / peak * 0.98              # clip na ho
    return np.clip(y * 32767.0 * 0.92, -32768, 32767).astype("<i2").tobytes()

kokoro = None
lock = threading.Lock()
ready = False
err = ""

def load():
    global kokoro, ready, err
    try:
        from kokoro_onnx import Kokoro
        kokoro = Kokoro(MODEL, VOICES)
        kokoro.create("Ready.", voice="am_adam", speed=1.0, lang="en-us")   # garam karo (pehli awaaz tez ho)
        ready = True
        print("KOKORO READY", flush=True)
    except Exception as e:
        err = str(e)
        print("KOKORO LOAD ERROR:", e, flush=True)

class H(BaseHTTPRequestHandler):
    def log_message(self, *a): pass
    def _send(self, code, body=b"", ctype="text/plain"):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def do_GET(self):
        if self.path.startswith("/ping"):
            self._send(200 if ready else 503, (b"ok" if ready else (b"loading" if not err else err.encode("utf-8", "ignore"))))
        else:
            self._send(404)
    def do_POST(self):
        if self.path != "/tts":
            return self._send(404)
        if not ready:
            return self._send(503, b"loading")
        try:
            n = int(self.headers.get("Content-Length", "0"))
            req = json.loads(self.rfile.read(n).decode("utf-8"))
            text = (req.get("text") or "").strip()
            voice = req.get("voice") or "am_adam"
            speed = float(req.get("speed") or 1.0)
            speed = min(1.6, max(0.5, speed))
            if not text:
                return self._send(400, b"empty")
            with lock:
                samples, sr = kokoro.create(text, voice=voice, speed=speed, lang="en-us")
            self._send(200, to_8k_pcm16(samples, sr), "application/octet-stream")
        except Exception as e:
            self._send(500, str(e).encode("utf-8", "ignore"))

if __name__ == "__main__":
    if not (os.path.exists(MODEL) and os.path.exists(VOICES)):
        print("kokoro.onnx / voices.bin exe ke saath nahi mile", flush=True)
        sys.exit(2)
    threading.Thread(target=load, daemon=True).start()
    ThreadingHTTPServer(("127.0.0.1", PORT), H).serve_forever()
