@CD "%~dp0"
:: should be in script dir now

@CD ..
:: should be in project dir now

RD out /S /Q

cd canvas_scrolled_text
:: should be in source dir now

:: ECHO %pythonpath%
:: PAUSE
:: pythonpath is empty
SET pythonpath=..\.venv\Lib\site-packages

python -m nuitka --onefile --follow-imports --enable-plugin=tk-inter --plugin-enable=numpy --remove-output --output-dir=..\out demo1.py
ROBOCOPY img ..\out\img /E