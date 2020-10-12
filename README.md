# Description
This API was built thinking on use inside company, and not open to external users of a store.

It was hosted on Heroku: https://orders-api-test.herokuapp.com/

And has endpoints for:
 - Clients - https://orders-api-test.herokuapp.com/client/
 - Product - https://orders-api-test.herokuapp.com/product/
 - User registration, login/logout (some endpoints are avaliable only for admin users) - See swagger for those endpoints
 - Carts - https://orders-api-test.herokuapp.com/cart/
 - CartItems - https://orders-api-test.herokuapp.com/cart_items/
 - Orders - https://orders-api-test.herokuapp.com/order/
 - Docs - https://orders-api-test.herokuapp.com/swagger/

You can visit the API on Heroku or follow the 'Installing instructions' 

# Local installing instructions
Pre-requisites: Have Docker or Python and postgres installed on your machine.

1. Make a clone of this repo
2. Open a terminal on the folder of the cloned repository

For Docker - run the following commands:
1. docker-compose build (it will create an image of the app)
2. docker-compose up (it will run the app with the database postgres)
3. the application will be available on localhost:8000

For Python:
1. Make a new virtualenv to install the requirements ('pip install virtualenv', then 'virtualenv venv', 'venv\Scripts\activate)
2. Run 'pip install -r requirements.txt' - It will install all requirements on your virtualenv
3. Run 'python manage.py makemigrations'
4. Run 'python manage.py migrate'
5. Run 'python manage.py runserver' - It will start the application on localhost:8000

# Work Environment
Operational System: Windows 10

IDE: PyCharm

Libraries: Python 3.8, DjangoRestFramework 3.11.2, Django 3.1.2, drf_yasg(swagger) 1.17.1, django-filters 2.4.0.