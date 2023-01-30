
# Forever Ecommerce
![Forever](https://github.com/omarreda22/Forever/blob/main/static/Forever.PNG)

## Django Ecommerce Store with
- Full-featured shopping cart with PayPal & credit/debit payments
- Product rating & review system
- An actual real-world project built in a linear and progressive manner
- Admin area to manage customers, products & orders
- Product search, carousel, pagination & more

## How to install on Windows
1. clone this project
2. install virtualenv
```
pip install virtualenv
```
3. create new virtual environment
```
py -m venv venv
```
4. activate the new virtual
```
.\venv\Scripts\activate
```
5. install requirements.txt
```
pip install -r requirements.txt
```
6. run local server to begin
 ```
 py manage.py runserver
 ```
 7. go live with [localhost:8000](http://localhost:8000/)
 
 ** to install on Unix/macOS  [see this document](https://packaging.python.org/en/latest/guides/installing-using-pip-and-virtual-environments)
 
 
 
 ## to add new products and access admin panel 
 1. run on trimnal 
 ```
 py manage.py createsuperuser
 ```
 2. create new admin user
 2. go to [localhost:8000/admin](http://localhost:8000/admin)
