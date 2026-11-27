WHISPERPHONE v3  -  Kokoro OFFLINE awaaz + naya dark UI
=========================================================
NAYA KYA HAI
1) AWAAZ: Adam / Jessica / Sarah ab Kokoro se (aapke apne PC par, internet nahi, free). Voice chip par ▶ = sirf aap ko test.
2) Button DABATE hi (mouse-down) awaaz Line 1 ko. Cache RAM mein hota hai. Delay nahi.
3) Phrase Pad par tabs: All / Greetings / Answers / Closing / General (+ apni category likh sakte hain).
4) Likhein + Enter = bol do (button nahi banta).  "+ Button" = wo text hamesha ke liye button.
   "jessica: hello" likhein to Jessica ki awaaz. Button par right-click: Delete / Move to category / Voice.
5) SPEED slider (0.70x - 1.30x). Badalne par awaazein background mein dobara banti hain (button thori der gray).
6) LOG ab chhupa hai: upar right "LOG" button dabayein to khulta hai. Error/call-fail ki wajah beech wale column ke neeche chhoti line mein aati hai.
7) MIC MUTE (F1): shor ho to aapka mic Line 1 ko band. Phrase button phir bhi chalte hain. Line 2 ko mic KABHI nahi jata.
8) Do pause switch: F2 = CUSTOMER->CLIENT, F3 = CLIENT->CUSTOMER. F4 = Auto-answer. F5..F12 = pehle 8 buttons. Esc = awaaz band.
   Koi switch app khud nahi badalti, hangup bhi sirf aap karein.
8b) BUTTON AWAAZ MUJHE: Ctrl+H ya neeche wala button. Default = SIRF LINE 1 (aap ko repeat nahi sunai deti). Orange = aap ko bhi sunai de. Voice test ▶ hamesha sunai deta hai.
9) AUTO-ANSWER: customer (Line 2) ke lafz pakde to Line 1 ko jawab-awaaz. Rules ki list neeche, right-click = delete.

SAFETY (code mein): Line 2 (customer) ko sirf client ki awaaz ya khamoshi jati hai. Mic, phrase, test, auto-answer - sab sirf Line 1 (+ aap ke speaker).

SETUP (sirf 1 baar)
A) GitHub: .github/workflows/build.yml is zip wali se badal dein > Commit.
B) Actions > Build WhisperPhone > Run workflow > Artifacts zip download > extract.
C) Apni PURANI files us folder mein rakhein: config.json, model\ (Vosk), aur ye 2 (aap ne upload ki thin):
      kokoro.onnx   voices.bin
   (kokoro_server.py aur install_kokoro.bat build ke saath khud aa jate hain.)
D) Python 3.9+ install karein (python.org, "Add to PATH" tick). Phir install_kokoro.bat double-click (ek baar, internet chahiye).
E) WhisperPhone.exe chalayein. Kokoro 5-20 sec mein tayyar (neeche "Awaaz tayyar ... Kokoro (offline)"). Pehli baar awaazein bante hi button gray se hare ho jate hain.
   Kokoro na chale to app khud ElevenLabs (agar key) ya Windows ki awaaz par aa jati hai - app kharab nahi hoti.

config.json (optional): config_new_fields.json mein example hai. "Engine": auto | kokoro | eleven | windows.
Purani phrases mein "Cat" na ho to app khud category laga deti hai.

NOTES
- "dob" jaisa chhota lafz Vosk aksar nahi pakadta; poore lafz rakhein: date of birth, birthday, born.
- Delay: ~0.02 sec (audio ka apna 20ms frame). 0.001 sec Windows audio mein mumkin nahi.
- Phrase ka text ab seedha wahi hai jo bolna hai (jaise "Could you please repeat that?").

START PAR: customer ki awaaz Line 1 ko shuru mein BAND (PAUSED). Line 1 ko sunwana ho to F2. config.json: "CustToClientOnStart": true se purana tareeqa; "HearButtonVoice": true se button awaaz hamesha sunai de.
