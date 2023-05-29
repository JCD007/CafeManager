@echo off

CALL .env\Scripts\activate

set FLASK_APP=.\server\routes.py
set FLASK_ENV=development

@REM python -m flask run --cert=adhoc && Fix this to run ssl

python -m flask --debug run &&