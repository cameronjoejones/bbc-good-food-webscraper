# BBC Good Food Recipe Scraper
This code is a scraper that is built to extract dinner recipes from the BBC Good Food website. It makes use of the requests library in python to retrieve HTML content from the website and then uses the BeautifulSoup library to parse the HTML content. The scraper also makes use of the pandas library to store the extracted data in a DataFrame.

### Requirements

- Requests
- BeautifulSoup4
- Numpy
- Pandas
### Usage
The code has two functions, range_of_numbers and extract. The range_of_numbers function takes a single argument n, which is an integer, and returns a list of numbers from 1 to n. The extract function takes two arguments: pages and sleep_timer. The pages argument is a list of integers that specify the pages to scrape and the sleep_timer argument is the number of seconds the scraper should wait between making requests to the website.

The extract function returns three DataFrames: list_urls, urls_df, and recipes_df. The list_urls DataFrame contains a list of URLs for all the recipes, urls_df is a DataFrame of all the recipe URLs, and recipes_df is a DataFrame containing all the extracted information about the recipes.

### Information Extracted
The following information is extracted for each recipe:

- Title
- Difficulty
- Serves
- Rating
- Number of Reviews
- Prep Time
- Cook Time
- Ingredients
- Vegetarian
- Vegan
- Dairy-free
- Keto
- Gluten-free


### Conclusion
This scraper is a simple example of how to extract information from a website using the requests and BeautifulSoup libraries in Python. It can be used as a starting point for more complex web scraping projects or adapted to suit different scraping needs.
