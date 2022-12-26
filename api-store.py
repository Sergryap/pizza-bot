import os
import time
from pprint import pprint

import requests

from environs import Env
from slugify import slugify


def check_token(error=False):
    if not os.environ.get('TOKEN_EXPIRES') or int(os.environ['TOKEN_EXPIRES']) < int(time.time()) or error:
        url = 'https://api.moltin.com/oauth/access_token'
        client_id = os.getenv('CLIENT_ID')
        client_secret = os.getenv('CLIENT_SECRET')
        data = {
            'client_id': client_id,
            'client_secret': client_secret,
            'grant_type': 'client_credentials'
        }
        response = requests.post(url, data)
        response.raise_for_status()
        token_data = response.json()
        os.environ['TOKEN_EXPIRES'] = str(token_data['expires'] - 60)
        os.environ['ACCESS_TOKEN'] = token_data['access_token']


def create_product(name: str, sku: str, description: str, price: int):
    url = 'https://api.moltin.com/v2/products'
    headers = {
        'Authorization': f'Bearer {os.environ["ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    json_data = {
        'data': {
            'type': 'product',
            'name': name,
            'slug': slugify(name),
            'sku': sku,
            'manage_stock': False,
            'description': description,
            'price': [
                {
                    'amount': price,
                    'currency': 'RUB',
                    'includes_tax': True
                }
            ],
            'status': 'live',
            'commodity_type': 'physical'
        }
    }
    response = requests.post(url=url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def create_pcm_product(name: str, sku: str, description: str):
    url = 'https://api.moltin.com/pcm/products'
    headers = {
        'Authorization': f'Bearer {os.environ["ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    json_data = {
        'data': {
            'type': 'product',
            'attributes': {
                'name': name,
                'commodity_type': 'physical',
                'sku': sku,
                'slug': slugify(name),
                'description': description,
                'status': 'live',
            },
        }
    }
    response = requests.post(url=url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def add_product_price(price_book_id: str, sku: str, price: int):
    url = f'https://api.moltin.com/pcm/pricebooks/{price_book_id}/prices'
    headers = {
        'Authorization': f'Bearer {os.environ["ACCESS_TOKEN"]}',
        'Content-Type': 'application/json'
    }
    json_data = {
        'data': {
            'type': 'product-price',
            'attributes': {
                'sku': sku,
                'currencies': {
                    'RUB': {
                        'amount': price,
                        'includes_tax': True,
                    }
                }
            }
        }
    }
    response = requests.post(url=url, headers=headers, json=json_data)
    response.raise_for_status()
    return response.json()


def upload_image(file_location):
    url = 'https://api.moltin.com/v2/files'
    headers = {
        'Authorization': f'Bearer {os.environ["ACCESS_TOKEN"]}'
    }
    files = {
        'file_location': (None, file_location),
    }
    response = requests.post(url, headers=headers, files=files)
    response.raise_for_status()
    return response.json()


def get_pcm_products():
    url = 'https://api.moltin.com/pcm/products'
    headers = {'Authorization': f'Bearer {os.environ["ACCESS_TOKEN"]}'}
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()


if __name__ == '__main__':
    env = Env()
    env.read_env()
    check_token()
    # pprint(create_pcm_product('test test test2', 'test-6', 'description-test'))
    # pprint(add_product_price('8b0a9130-1cda-4450-bec3-b96e383d42a0', 'test-6', 999))
    # pprint(get_pcm_products())
    pprint(upload_image('https://dodopizza-a.akamaihd.net/static/Img/Products/Pizza/ru-RU/1626f452-b56a-46a7-ba6e-c2c2c9707466.jpg'))

