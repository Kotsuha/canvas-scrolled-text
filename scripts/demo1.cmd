@echo %cd%
@echo %~dp0
@echo %~dpnx0
cd "%~dp0"
cd ..
pipenv run python demo1.py