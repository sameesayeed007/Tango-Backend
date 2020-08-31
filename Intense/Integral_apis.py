import requests


site_path = "http://127.0.0.1:8000/"

def get_email_config():
    url = site_path+ "email/config_value"
    value = requests.get(url = url) 
    return (value.json())


def create_user_balance(data):
    url = site_path+ "user/balance/"
    requests.post(url = url,data = data) 
   
def create_user_profile(data):
    url = site_path + "user/create_profile/"
    requests.post(url = url,data = data) 

def create_product_code(data):
    url = site_path + "product/insert_value/"
    requests.post(url = url,data = data) 


def ratings(product_id):
	product_id=int(product_id)
	url = site_path+ "product/ratings/product_id/"
	value = requests.get(url = url) 
	return (value.json())

   

