"""
Bioz - Home task - Web scrapper (Selenium)

For this home test, you have been provided with a text file containing 10 article titles.
Your task is to create a dictionary of each article title with its corresponding PubMed ID.
To find the PubMed ID for each article, you need to search for the article title on the PubMed website, which can be accessed via the following URL: “https://pubmed.ncbi.nlm.nih.gov/”.
To automate this process, you will use the Selenium library.
If a specific article cannot be found on the PubMed website, then the corresponding value in the dictionary should be “no results for article title”.

Once you have completed the task, please send:
 -your Python script and the dictionary in a JSON file format.
 -In addition, please record and send a short video using https://www.loom.com/ where your describe your thought process,
  the resources you used, new things you learned, and problems you faced along the way.

"""

# IMPORTS
from selenium import webdriver
from selenium.webdriver.common.by import By
import json
import time

# CONSTANTS
URL = "https://pubmed.ncbi.nlm.nih.gov/"
TEXT_FILE = "titles.txt"


# FUNCTIONS
def initialize(text_file):
    '''
    Initiliaze program by reading titles from files, setting up the webdriver and pmid_dict.
    :parameter: text_file, text file containing 10 article titles.
    :return: titles, list of titles
    :return: driver, webdriver for Chrome
    :return: pmid_dict, empty dictionary used for pmid numbers
    '''

    # load the article titles from the text file
    with open(text_file, 'r') as f:
        titles = [line.strip() for line in f.readlines()]

    # initialize the web driver in Chrome
    driver = webdriver.Chrome()

    # create an empty dictionary to store the PubMed IDs
    pmid_dict = {}

    return titles, driver, pmid_dict


def parse_titles(titles, driver, pmid_dict):
    '''
    Parse titles by navigating into the URL and searching for the PMID number.
    :parameter: titles, list of titles
    :parameter: driver, webdriver for Chrome
    :parameter: pmid_dict, empty dictionary used for pmid numbers
    :return: pmid_dict, dictionary filled with key-value: title:pmid
    '''

    # loop through each article title and search for its PubMed ID
    for article_title in titles:
        # start parsing
        print("Parsing title: " + article_title)

        # navigate to the PubMed website
        driver.get(URL)

        # find the search box and enter the article title
        search_box = driver.find_element(By.ID, 'id_term')
        search_box.send_keys(article_title)

        time.sleep(2)

        # find the search button and click it
        search_button = driver.find_element(By.CLASS_NAME, "search-btn")
        search_button.click()

        # check if the search returns any results
        # no results
        if 'No results were found' in driver.page_source:
            pmid_dict[article_title] = str('no results for "' + article_title + '"')
        # entered directly into the article page
        elif 'article-page' in driver.page_source:
            pmid = driver.find_element(By.CSS_SELECTOR, 'strong[title="PubMed ID"]').text
            pmid_dict[article_title] = pmid
        # search results
        elif 'search-results' in driver.page_source:
            # find the link to the first article and extract its PubMed ID
            pmid = driver.find_element(By.XPATH, "//article[1]//span[@class='docsum-pmid']").text
            real_article_title = driver.find_element(By.XPATH, "//article[1]//a[@class='docsum-title']").text
            pmid_dict[real_article_title] = pmid
        # unknown page
        else:
            pmid_dict[article_title] = str('no results for "' + article_title + '"')

    # close the web driver
    driver.quit()

    return pmid_dict


def save_to_json(json_file, pmid_dict):
    '''
    Saves pmid_dict to a JSON file with the name given: json_file
    :parameter: json_file, file name for the json_file
    :parameter: pmid_dict, dictionary with key-value: titles:pmid
    :return: no return
    '''
    # save the dictionary to a JSON file
    print("Saving to " + json_file)
    with open(json_file, 'w') as f:
        json.dump(pmid_dict, f, indent=4)


def main():
    '''
    Main function, controls the general logic.
    Receives a text file containing 10 article titles and generates a JSON file with a dictionary containing the
    PMID number.
    :return: no return
    '''
    # start message
    print("Started execution")

    # initializations
    titles, driver, pmid_dict = initialize(TEXT_FILE)

    # parse titles in the URL
    pmid_dict = parse_titles(titles, driver, pmid_dict)

    # save pmid_dict to json
    save_to_json('pmid_dict.json', pmid_dict)

    # End message
    print("Finished execution")

    time.sleep(1)


if __name__ == '__main__':
    main()
