import re
from bs4 import BeautifulSoup
from selenium import webdriver
from DB_config import mydb
from datetime import date
from bs4 import BeautifulSoup
import requests
import xlsxwriter
from Application_data import remove_data_from_recipies
today = date.today()

def nutritionDownload():
    chrome_path="E:/All in/Final Year Project/Akki/Programmes/chromedriver_win32/chromedriver.exe"
    driver = webdriver.Chrome(chrome_path)

    count=0
    types=["https://www.nutrition-and-you.com/fruit-nutrition.html",
           "https://www.nutrition-and-you.com/vegetable-nutrition.html",
           "https://www.nutrition-and-you.com/nuts_nutrition.html",
           "https://www.nutrition-and-you.com/dairy-products.html"]
    typen=[]
    name=[]

    workbook = xlsxwriter.Workbook('nutrition.xlsx')
    worksheet = workbook.add_worksheet()

    # nuritionTypes = driver.find_elements_by_xpath("//*[@id='mySidebar']//a[@href]")
    # for nuritionType in nuritionTypes:
    # 	types.append(nuritionType.get_attribute("href"))
    #
    # types.pop(0)


    for type in types:
        # print (type)
        driver.get(type)
        typename = driver.find_elements_by_xpath("/html/body/div[3]/div[2]/div/div/table//a[@href]")

        for Typex in typename:
            typen.append(Typex.get_attribute("href"))

            # print(len(typen))
            # print(Typex)

    for i in range(len(typen)):
        driver.get(typen[i])
        print(typen[i])
        try:
            downloadNames = driver.find_element_by_xpath("/html/body/div[3]/div[1]/div[1]/h1").text
            name = re.sub("nutrition facts", "",downloadNames)
        except Exception:
            print("No name")
        res = requests.get(typen[i])
        soup = BeautifulSoup(res.text, "lxml")
        try:
            # print(name)
            for tr in soup.find(id="tab").find_all("tr"):
                data = [item.get_text(strip=True) for item in tr.find_all(["th", "td"])]
                # print(data)
                worksheet.write(count, 0, name)
                if(data[0]=="Energy"):
                    worksheet.write(count, 1, data[1])
                    energy = data[1]
                if(data[0]=="Carbohydrates"):
                    worksheet.write(count, 2, data[1])
                    carbohydrates = data[1]
                if(data[0]=="Protein"):
                    worksheet.write(count, 3, data[1])
                    protein = data[1]
                if(data[0]=="Total Fat"):
                    worksheet.write(count, 4, data[1])
                    totalFat = data[1]
                if(data[0]=="Cholesterol"):
                    worksheet.write(count, 5, data[1])
                    cholesterol = data[1]
                if(data[0]=="Dietary Fiber"):
                    worksheet.write(count, 6, data[1])
                    fiber = data[1]
            count = count + 1

            mycursor = mydb.cursor()
            sql = "INSERT INTO nutrition(name,calories,total_fat,cholesterol,protein,carbohydrate,fiber) VALUES (%s, %s, %s, %s,%s, %s, %s)"
            val = (name, energy, totalFat,cholesterol, protein, carbohydrates, fiber)
            mycursor.execute(sql, val)
            mydb.commit()

        except Exception:
            continue
            print("Nutrition table not exist ")
            worksheet.write(count, 0, "null")
            count = count + 1

        print("---------------------------------------------------------------------------------")

    driver.close()
    workbook.close()

def insertProductValue(productData):

    name = productData['name']
    servingSize = productData['servingSize']
    energy = productData['energy']
    carbohydrate = productData['carbohydrate']
    protein = productData['protein']
    totalFat = productData['totalFat']
    sugar = productData['sugar']
    cholesterol = productData['cholesterol']
    fiber = productData['fiber']

    mycursor = mydb.cursor()
    sql = "INSERT INTO nutrition(name,serving_size,calories,total_fat,cholesterol,protein,carbohydrate,fiber,sugar) VALUES(%s, %s, %s, %s,%s, %s, %s, %s, %s)"
    val = (name, servingSize, energy, totalFat, cholesterol, protein, carbohydrate, fiber, sugar)
    mycursor.execute(sql, val)
    mydb.commit()

    insertProductDetails(productData)



def getNutritionId(name):
    mycursor = mydb.cursor()
    sql= "SELECT nutrition_id FROM nutrition WHERE name = %s"
    val=(name,)
    mycursor.execute(sql,val)
    myResult = mycursor.fetchall()
    for nutrition_id in myResult:
        return nutrition_id[0]

def insertProductDetails(productData):


    name = productData['name']
    price = productData['price']
    discount = productData['discount']
    netWeight = productData['netWeight']
    nutrition_id = getNutritionId(name)

    mycursor = mydb.cursor()
    sql = "INSERT INTO details(price,discount,net_weight,nutrition_id) VALUES(%s, %s, %s, %s)"
    val = (price, discount, netWeight,nutrition_id)
    mycursor.execute(sql, val)
    mydb.commit()

    insertProduct(productData,nutrition_id)


def getDetailId(nutrition_id):

    mycursor = mydb.cursor()
    sql= "SELECT details_id FROM details WHERE nutrition_id = %s"
    val=(nutrition_id,)
    mycursor.execute(sql,val)
    myResult = mycursor.fetchall()
    for detail_id in myResult:
        return detail_id[0]

def insertProduct(productData,nutrition_id):

    detail_id = getDetailId(nutrition_id)
    name = productData['name']

    mycursor = mydb.cursor()
    sql = "INSERT INTO product(product_name,detail_id,start_date) VALUES(%s, %s, %s)"
    val = (name, detail_id, today)
    mycursor.execute(sql, val)
    mydb.commit()

