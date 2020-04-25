import re
from selenium import webdriver
from datetime import date
import xlsxwriter
# from App.recipe_module.recipe_data_insert import insertRecipe1,insertRecipeIngredient1
today = date.today()

def downloadRecipes():
	chrome_path="E:/All in/Final Year Project/Akki/Programmes/chromedriver_win32/chromedriver.exe"
	driver = webdriver.Chrome(chrome_path)
	driver.get("http://www.knorr.lk/recipes")

	workbook = xlsxwriter.Workbook('dataset/RecipeDataset '+today.strftime("%d-%b-%Y")+'.xlsx')
	worksheet = workbook.add_worksheet()
	count = 1

	i=1
	types=[]
	filted=""
	foodTypes = driver.find_elements_by_xpath("//div[@id='col1_content']//a[@href]")

	try:
		for foodType in foodTypes:
			types.append(foodType.get_attribute("href"))

		for type in types:
			print (type)
			driver.get(type)
			links=[]
			foodLinks = driver.find_elements_by_xpath("//div[@class='subcolumns']//a[@href]")
			typename = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[2]/div/div[1]/ul/li/div/h1").text
			print(typename)
			for foodLink in foodLinks:
				links.append(foodLink.get_attribute("href"))


			a = set(links)
			a = list(set(a))
			seen = set()
			result = []
			for item in a:
				if item not in seen:
					seen.add(item)
					result.append(item)


			for x in result:
				driver.get(x)
				ingredients = driver.find_elements_by_class_name('recipe-ingredients-list')
				name = driver.find_element_by_xpath("/html/body/div[1]/div[2]/div[3]/div[1]/div/div[1]/h1").text

				for comment in ingredients:

					print(name)
					separated = re.sub('\n', "**", comment.text)

					filted=separated

					worksheet.write(count-1, 0, count)
					worksheet.write(count-1, 1, name)
					worksheet.write(count-1, 2, filted)
					worksheet.write(count-1, 3, typename)
					worksheet.write(count-1, 4, today)
					count = count+1
	finally:
		workbook.close()
		driver.close()
