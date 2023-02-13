import datetime
import time
import warnings

import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

warnings.filterwarnings('ignore')


def range_of_numbers(n):
    return list(range(1, n + 1))


def extract(pages, sleep_timer):
    def get_urls():
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36'}
        urls_df = pd.DataFrame(columns=['recipe_urls'])

        for page in pages:
            time.sleep(sleep_timer)
            url = f'https://www.bbcgoodfood.com/search/recipes/page/{page}/?sort=-popular&meal-type=dinner'
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')
            recipe_urls = pd.Series([a.get("href") for a in soup.find_all("a")])
            recipe_urls = recipe_urls[(recipe_urls.str.count("-") > 0)
                                      & (recipe_urls.str.contains("/recipes/") == True)
                                      & (recipe_urls.str.contains("category") == False)
                                      & (recipe_urls.str.contains("collection") == False)].unique()
            df = pd.DataFrame({"recipe_urls": recipe_urls})
            urls_df = pd.concat([urls_df, df], ignore_index=True)

        urls_df['recipe_urls'] = 'https://www.bbcgoodfood.com' + urls_df['recipe_urls'].astype(str)
        recipes_df = pd.DataFrame(
            columns=['title', 'difficulty', 'serves', 'rating', 'reviews', 'vegetarian', 'vegan', 'dairy_free', 'keto',
                     'gluten_free', 'prep_time', 'cook_time', 'ingredients'])
        list_urls = urls_df['recipe_urls'].to_list()
        return list_urls, urls_df, recipes_df

    def get_recipes(list_urls, urls_df, recipes_df):

        for i in range(len(list_urls)):
            time.sleep(sleep_timer)
            url = list_urls[i]
            html = requests.get(url)
            soup = BeautifulSoup(html.text, 'html.parser')

            try:
                recipe_title = soup.find('h1', {'class': 'heading-1'}).text
            except:
                recipe_title = np.nan
            try:
                difficulty = soup.find_all('div', {'class': 'icon-with-text__children'})[1].text
            except:
                difficulty = np.nan
            try:
                serves = soup.find_all('div', {'class': 'icon-with-text__children'})[2].text
            except:
                serves = np.nan
            try:
                rating = soup.find_all('span', {'class': 'sr-only'})[26].text
            except:
                rating = np.nan
            try:
                number_of_review = soup.find('span', {'class': 'rating__count-text body-copy-small'}).text
            except:
                number_of_review = np.nan
            try:
                prep_time = soup.find('li', {'class': 'body-copy-small list-item'}).text
            except:
                prep_time = np.nan
            try:
                cook_time = soup.find_all('li', {'class': 'body-copy-small list-item'})[1].text
            except:
                cook_time = np.nan
            try:
                categories = soup.find_all('ul', {
                    'class': 'terms-icons-list d-flex post-header__term-icons-list mt-sm hidden-print list list--horizontal'})[
                    0].text
                if 'Vegetarian' in categories:
                    vegetarian = 'True'
                if not 'Vegetarian' in categories:
                    vegetarian = False
                if 'Vegan' in categories:
                    vegan = True
                if not 'Vegan' in categories:
                    vegan = False
                if 'Keto' in categories:
                    keto = True
                if not 'Keto' in categories:
                    keto = False
                if 'Dairy-free' in categories:
                    dairy_free = True
                if not 'Dairy-free' in categories:
                    dairy_free = False
                if 'Gluten-free' in categories:
                    gluten_free = True
                if not 'Gluten-free' in categories:
                    gluten_free = False
            except:
                vegetarian = False
                vegan = False
                keto = False
                dairy_free = False
                gluten_free = False

            i = 0
            ingredient_list = []
            ingredient = soup.find_all('li', {'class': 'pb-xxs pt-xxs list-item list-item--separator'})
            while i < len(ingredient):
                try:
                    ingredient_string = ''.join(str(ingredient[i]).split('<!-- -->')[1])
                except Exception as e:
                    # print(e)
                    ingredient_string = ''.join(ingredient[i].text)
                    pass
                ingredient_list.append(ingredient_string)
                ingredient_list = [l.replace('</li>', '') for l in ingredient_list]
                i = i + 1

            print(f'Loaded recipe: {recipe_title}')
            recipes_df = recipes_df.append(
                {'title': recipe_title, 'difficulty': difficulty, 'serves': serves, 'rating': rating,
                 'reviews': number_of_review, 'vegetarian': vegetarian, 'vegan': vegan, 'keto': keto,
                 'dairy_free': dairy_free, 'gluten_free': gluten_free, 'prep_time': prep_time, 'cook_time': cook_time,
                 'ingredient': ingredient_list}, ignore_index=True)

        recipes_df = recipes_df.join(urls_df)

        return recipes_df

    list_urls, urls_df, recipes_df = get_urls()
    recipes_df = get_recipes(list_urls, urls_df, recipes_df)
    return recipes_df


if __name__ == '__main__':
    # enter how many pages of recipes you would like to scrape
    pages = range_of_numbers(2)
    # here you can change the amount of time between each request to scrape data
    sleep_timer = 1
    week = datetime.datetime.now().strftime("%Y-%m-%d")

    print(f'Scraping {pages} pages from BBC good food')
    recipes_df = extract(pages, sleep_timer)
    recipes_df.to_csv(f'output/recipes_data_{week}.csv', index=False)
    print('Complete')
