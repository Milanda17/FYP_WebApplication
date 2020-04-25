from flask import Flask, render_template, flash, request, session, abort, redirect
from App.nutrition_module.person_bios import personRegister,personLogin
from App.nutrition_module.nutrition_select_algorithm import selectedProctDetails,suggestProductUsingDiseases, getAllProducts
from App.nutrition_module.nurition_download import insertProductValue,nutritionDownload
from App.recipe_module.recipe_download_selenium import downloadRecipes
from App.recipe_module.recipe_suggestion_algorithm import preSuggestRecipeDiseases, start

import os

from DB_config import mydb

app = Flask(__name__)

product_list = []
suggest_recipe = []

@app.route('/addProduct')
def addProduct():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        return render_template('addProduct.html')

@app.route('/customerRecipeUsingDisease')
def customerRecipeUsingDisease():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data= preSuggestRecipeDiseases(session.get('username'))
        return render_template('customerRecipeUsingDisease.html',data=data)

@app.route('/customerHome')
def customerHome():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data=product_list
        return render_template('customerHome.html',data=data)

@app.route('/customerAddToCart')
def customerAddToCart():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        data = getAllProducts()
        return render_template('customerAddToCart.html', data=data)

@app.route('/productAddToCart', methods=['GET','POST'])
def productAddToCart():

        product_list_from_customer=request.form.getlist("product")
        global product_list
        product_list = product_list_from_customer

        return home()

@app.route('/customerSuggestIngredient')
def customerSuggestIngredient():
    if not session.get('logged_in'):
        return render_template('login.html')
    else:
        # itemInCart = ['ELEPANT HUSE GO SUGAR FREE NECTO 200ML','RED ONION', 'GARLIC  1KG', 'chilli','Dhall','bean','beef','SUPOSHA 250G']
        # itemInCart = ['beef', 'ASTRA 125G', 'ELEPANT HUSE GO SUGAR FREE NECTO 200ML','RED ONION', 'GARLIC  1KG', 'chicken', 'RED ONION', 'GARLIC  1KG' ]
        global product_list
        itemInCart = product_list
        customerId = "15"
        data = start(itemInCart, customerId)
        print(itemInCart)

        return render_template('customerSuggestIngredient.html', data=data)


#add prouct by shop owners
@app.route('/addProdcutValue', methods=['GET','POST'])
def addProdcutValue():
    username = session.get('username')
    productData = request.form
    insertProductValue(productData)
    return render_template('addProduct.html',username=username)

@app.route('/downloadNutritionValues', methods=['GET','POST'])
def downloadNutritionValues():
    nutritionDownload()
    return home()

@app.route('/downloadRecipe', methods=['GET','POST'])
def downloadRecipe():
    downloadRecipes()
    return home()


# --------------------------------------------API-----------------------------------------------------------------------

# Register
@app.route('/register', methods=['GET','POST'])
def register():
    personalData=request.get_json()
    personRegister(personalData)

    return "Success"

@app.route('/')
def home():
    username = session.get('username')
    if not session.get('logged_in'):
      return render_template('login.html')
    elif(username =='admin'):
      return render_template('home.html',username = username)
    else:
      return redirect('/customerHome')

@app.route('/login', methods=['POST'])
def do_admin_login():

    if (request.form['username']== 'admin'):
        if request.form['password'] == 'password' and request.form['username'] == 'admin':
         session['logged_in'] = True
         session['username'] = request.form['username']

        else:
            flash('wrong password!')
        return home()
    else:

        username = request.form['username']
        teleno = request.form['password']

        mycursor = mydb.cursor()
        sql=("SELECT customer_telephoneNo FROM customers WHERE customer_username =%s")
        val = (username,)
        mycursor.execute(sql,val)
        customer_telephoneNo = mycursor.fetchall()

        for tele in customer_telephoneNo:

            if teleno == tele[0] and request.form['username'] == username :
                session['logged_in'] = True
                session['username'] = request.form['username']

            else:
                flash('wrong password!')
            return home()


@app.route("/logout")
def logout():
    session['logged_in'] = False
    return home()

#Suggest products using disease
@app.route('/suggestProduct', methods=['GET', 'POST'])
def suggestProduct():
    customerId = request.get_json()
    suggestProductUsingDiseases(customerId)
    return customerId


#Pick recipes from database using selected product in cart
@app.route('/selectRecipes', methods=['GET', 'POST'])
def selectRecipes():
    selectedProductsInCart = request.get_json()
    return selectedProductsInCart


#view product details such as price,discount,nutrition
@app.route('/viewProductDetails', methods=['GET', 'POST'])
def viewProductDetails():
    selectedProduct = request.get_json()
    selectedProctDetails(selectedProduct)
    return selectedProduct


if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=True)


