from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pandas import DataFrame

# Create a new instance of the Chrome driver
service = Service('chromedriver.exe')
driver = webdriver.Chrome(service=service)

url = "https://www.google.com/search?q=-Contatos+%2B%2294.91-0-00+-+Atividades+de+organiza%C3%A7%C3%B5es+religiosas+ou+filos%C3%B3ficas%22+%2B+%22Situa%C3%A7%C3%A3o%3A+Ativa%22+site%3Ahttps%3A%2F%2Fcnpj.biz%2F&biw=1536&bih=714&sxsrf=AJOqlzVuTHC5EFkfLu_1IHW1fmWDxLa2XQ%3A1678764016146&ei=8OcPZNfKCN6U9u8PoNaD8AI&ved=0ahUKEwjXguCmu9r9AhVeiv0HHSDrAC4Q4dUDCA8&oq=-Contatos+%2B%2294.91-0-00+-+Atividades+de+organiza%C3%A7%C3%B5es+religiosas+ou+filos%C3%B3ficas%22+%2B+%22Situa%C3%A7%C3%A3o%3A+Ativa%22+site%3Ahttps%3A%2F%2Fcnpj.biz%2F&gs_lcp=Cgxnd3Mtd2l6LXNlcnAQDEoECEEYAVDUGVjUGWDWKWgBcAB4AIABAIgBAJIBAJgBAKABAqABAcABAQ&sclient=gws-wiz-serp"

driver.get(url)

current = 0
while True:
    # Wait for the page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "result-stats")))

    links = []
    descriptions = []
    titles = []

    # Get the links
    fetch_links = driver.find_elements(By.TAG_NAME, "a")
    for link in fetch_links:
        href = link.get_attribute("href")
        if href is not None and href.startswith("https://cnpj.biz/"):
            links.append(href)
            titles.append(link.find_element(By.TAG_NAME, "h3").text)
            parent = link.find_element(By.XPATH, "./../..")
            descriptions.append(parent.find_element(By.XPATH, "./following-sibling::*").text)

    # Create a DataFrame
    df = DataFrame({'Title': titles, 'Description': descriptions, 'Link': links})
    df.to_csv(f'responses/links_{current}.csv', mode='a', header=False, index=False)
    current += 10
    driver.implicitly_wait(10)
    driver.implicitly_wait(20)

    try:
        next_page = driver.find_element(By.ID, "pnnext")
    except:
        break
    next_page.click()

# Close the browser
driver.quit()