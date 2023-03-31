# For this home test, you have been provided with a text file containing 10 article titles.
# Your task is to create a dictionary of each article title with its corresponding PubMed ID.
# To find the PubMed ID for each article, you need to search for the article title on the PubMed website, which can be accessed via the following URL: “https://pubmed.ncbi.nlm.nih.gov/”.

# To automate this process, you will use the Selenium library.
# If a specific article cannot be found on the PubMed website, then the corresponding value in the dictionary should be “no results for article title”.

# Once you have completed the task, please send your Python script and the dictionary in a JSON file format.

# In addition, please record and send a short video using https://www.loom.com/ where your describe your thought process,
# the resources you used, new things you learned, and problems you faced along the way

# IMPORTS
from seleniumwire import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time

def make_request(url):
    '''

    :param url:
    :return:
    '''
    try:
        response = requests.get(url)
        # If the response was successful, no Exception will be raised
        response.raise_for_status()
        return response
    except HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except Exception as err:
        print(f'Other error occurred: {err}')
    else:
        print('Success!')


def main():
    '''
    Main function, controls the general logic.
    :return:
    '''
    print(f'Started main')

    base_url = "https://pubmed.ncbi.nlm.nih.gov/"
    title_searched = "Men's Feminist Identification and Reported Use of Prescription Erectile Dysfunction Medication"

    # Selenium
    driver = webdriver.Chrome()
    driver.get(base_url)

    # sleep for 2 sec
    #time.sleep(2)

    # Search 'search bar' inside the site
    search_input = driver.find_element(By.ID, 'id_term')
    search_input.send_keys(title_searched)

    # sleep for 1 sec
    time.sleep(1)

    # Click on 'search'
    #search_button = driver.find_element(By.CSS_SELECTOR, 'input[type="submit"]')
    search_button = driver.find_element(By.CLASS_NAME, "search-btn")
    search_button.click()

    # Sleep for 2 sec
    time.sleep(2)

    # Search for PMID of the first result
    #first_article = driver.find_element(By.TAG_NAME, "article")
    pmid = driver.find_element(By.XPATH, "//article[1]//span[@class='docsum-pmid']").text
    print(f"pmid = {pmid}")

    # Sleep for 5 sec
    time.sleep(5)

    # Close window
    driver.quit()


if __name__ == '__main__':
    main()

