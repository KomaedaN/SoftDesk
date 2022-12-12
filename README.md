# Setup :
1 - create virtual env : "python -m venv env"

2 - activate local env : "env/Scripts/activate.ps1" or "env\Scripts\activate.bat"

3 - install requirements.txt : "pip install -r requirements.txt"

4 - run the project : python manage.py runserver


# Endpoints :
you can find all documentation here : (https://documenter.getpostman.com/view/17797877/2s8YzTT2a6)
 
you can login with a test user : 
- Username = testuser
- Password = motdepassetest

with postman create an environement :
- VARIABLE = Authorization, CURRENT VALUE = Bearer (add your token here when you login).

then add in your request header :
- KEY = Authorization, VALUE = {{Authorization}}

select your new environment when you try your request
