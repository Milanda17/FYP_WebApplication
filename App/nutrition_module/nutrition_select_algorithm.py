from App.nutrition_module.person_bios import customerDetails
from DB_config import mydb
import json
import re
from Application_data import remove_data_from_nutrition, avoid_prodcut_cholesterol

def allNutritionValue():
    mycursor = mydb.cursor()
    sql1= "SELECT * FROM nutrition"
    mycursor.execute(sql1)
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult


def nutritionValuePreprocess(nutritionData):

    if(nutritionData):
        if('Kcal|kcal' in nutritionData):
            filted = re.sub(remove_data_from_nutrition, "",nutritionData)
            return float(float(filted)*1000)
        elif('mg' in nutritionData):
            filted = re.sub(remove_data_from_nutrition, "",nutritionData)
            return float(float(filted)/1000)
        else:
            filted = re.sub(remove_data_from_nutrition, "",nutritionData)
            return float(filted)
    else:
        return float(0)

#Suggest products using disease
def suggestProductUsingDiseases(customerId):

    customerDetail = customerDetails(customerId)

    for x in customerDetail:
        disease = x[9]
    product = set()
    red = set()
    yellow = set()
    green = set()
    myresult = allNutritionValue()
    for i in myresult:
      try:
            calories = float(nutritionValuePreprocess(i[3]))
            total_fat = float(nutritionValuePreprocess(i[4]))
            cholesterol = float(nutritionValuePreprocess(i[5]))
            protein = float(nutritionValuePreprocess(i[6]))
            carbohydrate = float(nutritionValuePreprocess(i[7]))
            sugar = float(nutritionValuePreprocess(i[9]))

            #cholesterol persons
            if(disease == 'cholesterol'):
                # if(((cholesterol*9*100)/calories)<0.1 and cholesterol<10):
                    product.add(i[1])

            #diabetes persons
            # elif (disease == 'diabetes'):
            #     if(((sugar*4*100)/calories)<10 and (calories<50) and (calories<5)):
            #         product.add(i[1])
            #
            # #High blood presser
            # elif (disease == 'HBP'):
            #     if(((total_fat*9*100)/calories)<6 and (((protein*4*100)/calories)<6) and (((carbohydrate*4*100)/calories)<55)):
            #         product.add(i[1])

            # #cholesterol persons
            # if(disease == 'cholesterol'):
            #     if(total_fat>=17.5):
            #         product.add(i[1])
            #         red.add(i[1])
            #     elif(total_fat<17.5 and total_fat>=3):
            #        product.add(i[1])
            #        yellow.add(i[1])
            #     else:
            #         product.add(i[1])
            #         green.add(i[1])
            #
            # #diabetes persons
            # elif (disease == 'diabetes'):
            #     if(sugar>=22):
            #         product.add(i[1])
            #         red.add(i[1])
            #     elif(sugar<22 and sugar>=8):
            #         product.add(i[1])
            #         yellow.add(i[1])
            #     else:
            #         product.add(i[1])
            #         green.add(i[1])
            #         # print("green =",i[1])
            #
            #
            # # #High blood presser
            # elif (disease == 'HBP'):
            #     if(sugar>=22):
            #         product.add(i[1])
            #         red.add(i[1])
            #         print("red =",i[1])
            #     elif(sugar<22 and sugar>=8):
            #         product.add(i[1])
            #         yellow.add(i[1])
            #         print("yellow =",i[1])
            #     else:
            #         product.add(i[1])
            #         green.add(i[1])
            #         print("green =",i[1])


      except Exception:
        print(i[1])
        print("error")
    return product


# def suggestProductUsingBMI():



#view product details such as price,discount,nutrition
def selectedProctDetails(productName):
    mycursor = mydb.cursor()
    sql= "SELECT * FROM nutrition N JOIN (SELECT D.*,P.* FROM product P JOIN details D ON P.detail_id=D.details_id WHERE P.product_name = %s) X ON N.nutrition_id=X.nutrition_id "
    val=(productName,)
    mycursor.execute(sql,val)
    productDetails = mycursor.fetchall()
    mycursor.close()

    return productDetails


# print(suggestProductUsingDiseases(13))

def getAllProducts():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM product")
    productDetails = mycursor.fetchall()
    mycursor.close()

    return productDetails


