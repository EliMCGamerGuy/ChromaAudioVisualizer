echo off
cls
call conda.bat activate ChromaVis
:anticrash
python ChromaAudioVisualizer.py
goto anticrash