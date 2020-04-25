from DB_config import mydb
import json

def personRegister(personalData):

    height = (int(personalData["height"])/100)
    BMI = int(personalData["weight"])/(height*height)

    mycursor = mydb.cursor()
    sql = "INSERT INTO customers (customer_username, customer_telephoneNo,customer_age,customer_height,customer_weight,customer_BMI) " \
          "VALUES (%s, %s, %s, %s, %s, %s)"
    val = (personalData['username'], personalData['telephoneNo'], personalData['age'], personalData['height'],personalData['weight'],BMI)
    mycursor.execute(sql, val)
    mydb.commit()
    # return json.dumps(personalData['username'])

def personLogin(personalLoginData):

    return "mila"

#select customer details
def customerDetails(customerId):
    mycursor = mydb.cursor()
    sql1 = "SELECT * FROM customers C JOIN diseases D ON C.disease_id=D.disease_id WHERE C.customer_id=%s"
    val=(customerId,)
    mycursor.execute(sql1,val)
    myresult = mycursor.fetchall()
    mycursor.close()
    return myresult
