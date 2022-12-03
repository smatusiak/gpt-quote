'''
A simple package that receives large text, calculates it in  GPT tokens,
scrapes OpenAI's website for current costs, and calculates text cost.
'''

import requests
from bs4 import BeautifulSoup
from transformers import GPT2TokenizerFast


def count_tokens(text):
    '''
    Count number of tokens in text
    '''
    # Get the number of tokens
    tokenizer = GPT2TokenizerFast.from_pretrained('gpt2')
    tokens = len(tokenizer.encode(text))
    print(f'Tokens: {tokens}')
    return tokens


def scrape_cost():
    '''
    Scrape OpenAI's website for current cost per thousand tokens
    '''
    # Scrape OpenAI's website for current cost
    url = 'https://openai.com/api/pricing/'
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')

    models = {}

    # iterate through the divs to find the model name and cost
    for div in soup.find_all('div', class_='mb-thin-gutter'):
        # get the name of the model. Get the first word since Ada and Davinci include hepler text
        model = div.find('div', class_='mb-0.125').text.strip().split('\u2002', 1)[0]
        cost = float(div.find('span', class_='large-copy').text.strip().replace('$', ''))
        models[model] = {'cost': cost}
    
    print(models)
    return models

def get_quote(text, model='all'):
    '''
    Calculate the cost of text in dollars
    '''
    # Get the number of tokens
    tokens = count_tokens(text)
    # Scrape OpenAI's website for current cost
    models = scrape_cost()

    if model == 'all':
        # calculate the cost of the text for each model and store in models dictionary
        for model in models:
            models[model]['quote'] = models[model]['cost'] * (tokens/1000)
        return models
    else:
        # convert model to lowercase
        model = model.lower()
        try:
            models[model]['quote'] = models[model]['cost'] * (tokens/1000)
        except KeyError:
            error = f'Invalid model. Please choose from {list(models.keys())}'
            print(error)
            return error

    
    