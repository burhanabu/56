@echo off
echo Kokoro offline awaaz ke liye ek baar install (Python 3.9+ chahiye: python.org)
python -m pip install --upgrade kokoro-onnx numpy
if errorlevel 1 py -3 -m pip install --upgrade kokoro-onnx numpy
echo.
echo Ho gaya. Ab WhisperPhone.exe chalayein.
pause
