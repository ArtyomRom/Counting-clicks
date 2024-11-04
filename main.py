import re

from dotenv import load_dotenv
import requests
import os


def is_shorten_link(token, url):
    params = {'access_token': token, 'url': url, 'v': '5.199'}
    response = requests.get('https://api.vk.com/method/utils.checkLink', params=params)
    response.raise_for_status()
    return url != response.json()['response']['link']

def shorten_link(token, url):
    params = {'access_token': token, 'url': url, 'private': '0', 'v': '5.199'}
    checking_response = requests.get(url)
    checking_response.raise_for_status()
    response = requests.get('https://api.vk.com/method/utils.getShortLink', params=params)
    response.raise_for_status()
    return response.json()['response']['short_url']


def count_clicks(token, link):
    link = re.sub('http[s]?://vk.cc/', '', link)
    params = {'access_token': token, 'key': link, 'v': '5.199'}
    response = requests.get('https://api.vk.com/method/utils.getLinkStats', params=params)
    response.raise_for_status()
    clicks_count = response.json()['response']['stats'][0]['views']
    return clicks_count

def main():
    load_dotenv()
    try:
        link = is_shorten_link(os.environ['TOKEN_VK'], input())
        if link:
            short_link = shorten_link(os.environ['TOKEN_VK'], link)
            print('Сокращенная ссылка: ', short_link)
            count_click = count_clicks(os.environ['TOKEN_VK'], short_link)
            print('Количество кликов: ', count_click)
        else:
            short_link = shorten_link(os.environ['TOKEN_VK'], link)
            print('Сокращенная ссылка: ', short_link)
    except requests.exceptions.HTTPError as error:
        print(error)

if __name__ == '__main__':
    main()
