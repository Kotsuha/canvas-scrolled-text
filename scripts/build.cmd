@CD "%~dp0"
@CD ..
:: ECHO %pythonpath%
:: PAUSE
:: pythonpath is empty
SET pythonpath=.venv\Lib\site-packages
RD out /S /Q
python -m nuitka --onefile --follow-imports --enable-plugin=tk-inter --plugin-enable=numpy --remove-output --output-dir=out demo1.py
ROBOCOPY img out\img /E