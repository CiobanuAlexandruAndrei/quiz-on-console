#!/usr/bin/env python3

from bs4 import BeautifulSoup
import requests
from card import Card

def get_quizlet_cards(quizlet_url):

    headers = {
        'authority': 'quizlet.com',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8',
        'accept-language': 'en-US,en;q=0.9',
        'cache-control': 'max-age=0',
        'referer': 'https://quizlet.com/latest',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'sec-gpc': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.0 Safari/537.36',
    }

    page = requests.get(quizlet_url, headers=headers)
    soup = BeautifulSoup(page.text, 'html.parser')
    terms = soup.find_all(class_='TermText')
    
    left_terms = []
    right_terms = []
    cards = []

    for i in range(len(terms)):
        if i % 2 == 0:
            left_terms.append(terms[i].get_text())
        else:
            right_terms.append(terms[i].get_text())
    
    for i in range(len(left_terms)):
        cards.append(Card(left_terms[i], right_terms[i]))
    
    return cards

if __name__ == "__main__":
    from learn import Learn
    
    url = ""
    cards = get_quizlet_cards(url)
    for i in cards:
        Learn.add_card_to_json_from_card(i, "Json/test.json")