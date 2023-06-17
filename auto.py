#PyMongo Import
import pymongo 
from mongo import connection_string

#Selenium Imports
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

#Set up for MongoDB
Client = pymongo.MongoClient(connection_string)
db = Client['insiderBiz']
collection = db['companies']

#Set up for Selenium
driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

#Navigation
url = "https://www.insiderbiz.in/company-list/?page="
base_url = "https://www.insiderbiz.in"
page_count = 1

try:
	for page in range(1,11):
		print("--------------------------------")
		print(f"Scrapping data from page {page}")
		print("--------------------------------")

		driver.get(url + str(page))

		wait.until(EC.presence_of_element_located((By.XPATH, "//table[@id='WebGrid']")))

		rows = driver.find_elements(By.XPATH, "//table[@id='WebGrid']/tbody/tr")

		for row in rows:
			columns = row.find_elements(By.XPATH, ".//td")
			cin = columns[0].text
			company_name = columns[1].text
			roc = columns[2].text
			address = columns[3].text

			print("-----------------------------")
			print(f"CIN: {cin}")
			print(f"Company Name: {company_name}")
			print(f"ROC: {roc}")
			print(f"address: {address}")
			print("-----------------------------")

			document = {
				"CIN": cin,
				"Company Name": company_name,
				"ROC": roc,
				"Address": address
			}
			collection.insert_one(document)

		page_count += 1

	print("Scrapping Completed!!!")
	print(f"Data added to the Database")

except Exception as e:
	print(f"Scrapping Inturrupted, Error: {e}")

finally:
	driver.quit()
	Client.close()