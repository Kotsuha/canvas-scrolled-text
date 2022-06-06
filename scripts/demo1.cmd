@echo %cd%
@echo %~dp0
@echo %~dpnx0
cd "%~dp0"
:: should be in script dir now
cd ..
:: should be in project dir now
cd canvas_scrolled_text
:: should be in source dir now
pipenv run python demo1.py