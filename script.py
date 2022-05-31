from selenium import webdriver
import time
import re
import csv


starsConv = {"One": 1, "Two": 2, "Three": 3,  "Four": 4, "Five": 5}
driver = webdriver.Chrome("./chromedriver")

pages = [f"http://books.toscrape.com/catalogue/category/books_1/page-{i}.html" for i in range(1, 51)]
driver.get("http://books.toscrape.com/catalogue/category/books_1/page-1.html")
allBooks = []
all_details = []
csvFile = open('book_data.csv', 'w', newline='')
csvWriter = csv.writer(csvFile)
csvWriter.writerow(["Title", "Category", "Stock", "Stars",
                   "Price", "Tax", "UPC", "Description"])

for page in pages:
    driver.get(page)
    booksInPage = [i.get_attribute(
        "href") for i in driver.find_elements_by_xpath("//li//h3//a")]
    allBooks.extend(booksInPage)

for bookLink in allBooks:
    driver.get(bookLink)
    title = driver.find_element_by_xpath("//div[@class='col-sm-6 product_main']/h1").text
    price = driver.find_element_by_xpath("//p[@class='price_color']").text
    stock = driver.find_element_by_xpath("//p[@class='instock availability']")
    stock = int(re.findall("\d+", stock.text)[0])
    stars = driver.find_element_by_xpath("//p[starts-with(@class, 'star-rating')]").get_attribute("class")
    stars = starsConv[stars.split()[1]]
    upc = driver.find_element_by_xpath("//article/table/tbody/tr[1]/td").text
    tax = driver.find_element_by_xpath("//article/table/tbody/tr[5]/td").text
    category_a = driver.find_element_by_xpath("//ul[@class='breadcrumb']/li[3]/a").text
    
    try:
        description = driver.find_element_by_xpath("//article/p").text
    except:
        description = ""
    
    csvWriter.writerow([title, category_a, stock, stars, price, tax, upc, description])


time.sleep(4)

driver.close()
