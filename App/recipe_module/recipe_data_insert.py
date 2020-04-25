from DB_config import mydb
import xlrd
from datetime import date
today = date.today()

# loc1 = ("E:/Final year project final/App/recipe_module/dataset/RecipeDataset "+today.strftime("%d-%b-%Y")+".xlsx")
loc1 = ("E:/Final year project final/App/recipe_module/dataset/RecipeDataset 10-Mar-2020.xlsx")
wb1 = xlrd.open_workbook(loc1)

def insertRecipe1():

    sheet = wb1.sheet_by_index(0)

    for i in range(sheet.nrows):

        mycursor = mydb.cursor()
        sql = "INSERT INTO recipe (recipe_id, recipe_name, recipe_type, start_date) VALUES (%s, %s, %s, %s)"
        val = (sheet.cell_value(i, 0), sheet.cell_value(i, 1), sheet.cell_value(i, 3), today)
        mycursor.execute(sql, val)
        mydb.commit()



def insertRecipeIngredient1():

    sheet = wb1.sheet_by_index(0)

    for i in range(sheet.nrows):
        data = sheet.cell_value(i, 2).split("**")
        for index in range(len(data)):
            print(data[index])
            mycursor = mydb.cursor()
            sql = "INSERT INTO recipe_data (recipe_id, recipe_ingredient,start_date) VALUES (%s, %s, %s)"
            val = (sheet.cell_value(i, 0), data[index], today)
            mycursor.execute(sql, val)
            mydb.commit()
