from DB_config import mydb
import numpy as np
import xlsxwriter
import xlrd
import re
import builtins
import pymysql
from DictList import DictList

mycursor = mydb.cursor()
mycursor.execute("SELECT r.recipe_id, rd.recipe_ingredient,r.recipe_name,r.recipe_type FROM recipe_data rd JOIN recipe r ON rd.recipe_id=r.recipe_id")
myresult = mycursor.fetchall()


def getIdFromRecipe():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT DISTINCT(recipe_id) FROM recipe_data")
    recipe_id = mycursor.fetchall()
    return recipe_id

def getCustomerDisease(username):
    mycursor = mydb.cursor()
    sql=("SELECT D.disease_name FROM customers C JOIN diseases D ON C.disease_id=D.disease_id WHERE C.customer_username =%s")
    val = (username,)
    mycursor.execute(sql,val)
    disease = mycursor.fetchall()
    mycursor.close()

    for customer_disease in disease:
        return customer_disease[0]

def preSuggestRecipeDiseases(username):
    product_and_weight={}
    count=0
    disease = getCustomerDisease(username)

    loc = ("E:/Final year project final/App/recipe_module/dataset/diseasesValues.xlsx")
    wb = xlrd.open_workbook(loc)
    sheet = wb.sheet_by_index(0)

    recipe_id = getIdFromRecipe()
    # recipe_id = selectedId

    for id in recipe_id:
        # print("id", id[0])

        for ingredient in myresult:
            if (ingredient[0]== id[0]):
                for i in range(sheet.nrows):
                    # if(disease == "cholesterol")
                        if(sheet.cell_value(i, 2)==disease):
                                if(ingredient[1].find(sheet.cell_value(i, 0)) != -1):
                                    count = count + sheet.cell_value(i, 1)
        # print(id[0], count)
        product_and_weight[id[0]] = count
        count = 0
    # print(product_and_weight)
    return suggestRecipeDiseases(product_and_weight)

def suggestRecipeDiseases(product_and_weight):

    all_recipe = {}
    very_high = []
    high = []
    medium = []
    low = []
    very_low = []

    for i in product_and_weight:
        if(product_and_weight[i]>= 1.5):
            very_high.append(i)
            all_recipe[i] = 1
        elif(product_and_weight[i]<1.5 and product_and_weight[i]>= 1.0):
            high.append(i)
            all_recipe[i] = 2
        elif(product_and_weight[i]<1.0 and product_and_weight[i]>= 0.5):
            medium.append(i)
            all_recipe[i] = 3
        elif(product_and_weight[i]<0.5 and product_and_weight[i]>= 0.3):
            low.append(i)
            all_recipe[i] = 4
        elif(product_and_weight[i]<0.3):
            very_low.append(i)
            all_recipe[i] = 5
    very_low_recipes = selectGroupOfRecipes(very_low)
    low_recipes = selectGroupOfRecipes(low)
    medium_recipes = selectGroupOfRecipes(medium)
    high_recipes = selectGroupOfRecipes(high)
    very_high_recipes = selectGroupOfRecipes(very_high)

    print(very_low_recipes)
    print(low_recipes)
    print(medium_recipes)
    print(high_recipes)
    print(very_high_recipes)

    return very_low_recipes, low_recipes, medium_recipes, high_recipes, very_high_recipes, myresult

def selectGroupOfRecipes(recipeIdList):
    print(recipeIdList)
    if len(recipeIdList)!=0:
        if len(recipeIdList)>1:
            try:
                mycursor = mydb.cursor()
                sql= 'SELECT r.recipe_id,r.recipe_name,r.recipe_type FROM recipe r WHERE r.recipe_id IN %s ORDER BY r.recipe_id' % str(tuple(recipeIdList))
                mycursor.execute(sql)
                myresult = mycursor.fetchall()
                mycursor.close()
                return myresult
            except:
                print("error")
        else:
            try:
                mycursor = mydb.cursor()
                sql= 'SELECT r.recipe_id,r.recipe_name,r.recipe_type FROM recipe r WHERE r.recipe_id = %s'
                val = (recipeIdList[0],)
                mycursor.execute(sql,val)
                myresult = mycursor.fetchall()
                mycursor.close()
                return myresult
            except:
                print("error")



d1 = DictList()
d2 = DictList()

def start(itemInCart,customerId):

    freqSet = dict()

    list_of_suggest_ingredient_list= []

    currFreqTermSetForRecipes = listconvert(itemInCart)
    freqOneTermSet = recipesConditionCheck(currFreqTermSetForRecipes,customerId,list_of_suggest_ingredient_list)
    currFreqTermSetForRecipes = freqOneTermSet
    k = 1
    while currFreqTermSetForRecipes != set():
        freqSet[k] = currFreqTermSetForRecipes
        k += 1
        currCandiItemSet = getJoinedItemSet(currFreqTermSetForRecipes, k)
        currFreqTermSetForRecipes = recipesConditionCheck(currCandiItemSet,customerId,list_of_suggest_ingredient_list)

    if(list_of_suggest_ingredient_list):
        res_list = []
        for i in range(len(list_of_suggest_ingredient_list)):
            if list_of_suggest_ingredient_list[i] not in list_of_suggest_ingredient_list[i + 1:]:
                print(list_of_suggest_ingredient_list[i])
                res_list.append(list_of_suggest_ingredient_list[i])
        return res_list


def listconvert(itemInCart):
    itemSet_ = set()

    for x in itemInCart:
        itemSet_.add(frozenset([x]))

    return itemSet_


def getJoinedItemSet(termSet, k):

    return set([term1.union(term2) for term1 in termSet for term2 in termSet
                if len(term1.union(term2))==k])


def recipesConditionCheck(currFreqTermSet,customerId, list_of_suggest_ingredient_list):
    itemSet_ = set()

    for x in (currFreqTermSet):
        selectRecipes(x,customerId,list_of_suggest_ingredient_list)
        itemSet_.add(x)
    return itemSet_

def mapWithDic(name,proDic):

    for listName, rName in proDic.items():
        if(name == listName):
            return str(rName)



def selectRecipes(groupOfProduct,customerId,list_of_suggest_ingredient_list):

    locDic = ("E:/Final year project final/App/recipe_module/dataset/productDictionary.xlsx")
    wb = xlrd.open_workbook(locDic)
    sheet = wb.sheet_by_index(0)
    proDic =dict()
    test =dict()

    for i in range(sheet.nrows):
        proDic[sheet.cell_value(i, 0)]=sheet.cell_value(i, 1)

    count=0
    recipe_id = getIdFromRecipe()

    for id in recipe_id:
        ingredientList=set()
        noOfIngredient=0
        for ingredient in myresult:
            if (ingredient[0]== id[0]):
                noOfIngredient=noOfIngredient+1
                ingredientList.add(ingredient[1])


        if(len(groupOfProduct)>1 and noOfIngredient >= len(groupOfProduct)):
            suggest_ingredient_list = ingredientList
            for x in groupOfProduct:
              dicName = mapWithDic(x,proDic)
              for ing in ingredientList:
                if(dicName !='aaaaaaaaaa' and dicName != None):
                  if ing.find(dicName) != -1:
                    count=count+1
                    suggest_ingredient_list.remove(ing)

                    break

              # print(len(groupOfProduct))

              if(count==len(groupOfProduct)):
                    for id_ in id:
                        test["id"]=id_
                    test["groupOfProduct"]=groupOfProduct
                    test["suggest_ingredient_list"]=suggest_ingredient_list
                    list_of_suggest_ingredient_list.append(test)

            count=0

def getCustomerDisese(customerId):
     mycursor = mydb.cursor()
     sql = ("SELECT disease_name FROM customers C JOIN diseases D ON C.disease_id = D.disease_id WHERE customer_id = %s")
     val = (customerId,)
     mycursor.execute(sql,val)
     customerDisease= mycursor.fetchall()

     for disease in customerDisease:
          return disease[0]

