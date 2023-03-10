import os
import requests
import urllib.parse
from dotenv import load_dotenv
import argparse


def shorten_link(url, bitly_token):
    headers = {'Authorization': f'Bearer {bitly_token}'}
    request_parameters = {'long_url': url}
    response = requests.post(
      url='https://api-ssl.bitly.com/v4/bitlinks',
      json=request_parameters,
      headers=headers
    )

    response.raise_for_status()
    return response.json().get('link')


def count_clicks(url, bitly_token):
    headers = {'Authorization': f'Bearer {bitly_token}'}
    parsed_url = urllib.parse.urlparse(url)
    url = 'https://api-ssl.bitly.com/v4/bitlinks/' \
          f'{parsed_url.netloc}{parsed_url.path}/clicks/summary'
    params = (
      ('unit', 'month'),
      ('units', '-1')
    )

    response = requests.get(
      url=url,
      params=params,
      headers=headers
    )

    response.raise_for_status()
    return response.json().get('total_clicks')


def is_bitlink(url, bitly_token):
    headers = {'Authorization': f'Bearer {bitly_token}'}
    parsed_url = urllib.parse.urlparse(url)
    response = requests.get(
      url='https://api-ssl.bitly.com/v4/bitlinks/'
      f'{parsed_url.netloc}{parsed_url.path}',
      headers=headers
    )
    return response.ok


if __name__ == '__main__':
    load_dotenv()
    parser = argparse.ArgumentParser(description='Создание короткой ссылки или подсчет кликов по уже существующей ссылке через сервис Bit.ly')
    parser.add_argument('url', help='Ссылка для обработки', type=str)
    args = parser.parse_args()
    bitly_token = os.environ['BITLY_TOKEN']
    inputted_url = args.url
    if is_bitlink(inputted_url, bitly_token):
        clicks = count_clicks(inputted_url, bitly_token)
        print(f"Total clicks of {inputted_url} = {clicks}")
    else:
        short_link = shorten_link(inputted_url, bitly_token)
        print(f"Bitlink: {short_link}")
        