from flask import Flask, render_template, request, redirect, url_for, flash
from AprioriComm import AprioriCommClass
from AprioriPersonalized import AprioriPerClass
from Rfm import RfmClass
from RealTimeRec import RealTimeRecomandationClass

import AprioriComm
import AprioriPersonalized
import importlib

app = Flask(__name__)
app.secret_key = 'many random bytes'



@app.route('/')
def Index():

    return ("connected")




@app.route('/rule/<minSupp>')
def rule(minSupp):


    importlib.reload(AprioriComm)
    items=['RATTHI FULL CREAM 400G','ANCHOR FULL CREAM 400G']
    objAprioriComm = AprioriCommClass(int(minSupp))

    start, end = objAprioriComm.indirect(1, "2019-")
    mounthlyItem = objAprioriComm.getSearchTransListSet(start,end)
    objAprioriComm.start(items,mounthlyItem)
    return ("Success")



@app.route('/rulepersonalized')
def rulePersonalized():


    importlib.reload(AprioriPersonalized)
    objAprioriPersonalized = AprioriPerClass()
    userList = objAprioriPersonalized.getUserList()
    for user in userList:
        importlib.reload(AprioriPersonalized)
        objAprioriPersonalized.start(user)
        objAprioriPersonalized.getFrequentPattern(user)



    return ("Success")


@app.route('/recomandation')
def realTimeRec():


    #itemInCart = ["RATTHI FULL CREAM 160G", "POTATO LANKA 1KG", "LAK LUNU 1KG", "DHALL 01 KG", "SUGER 1KG","B ONION  1KG", 'RED ONION', 'GARLIC  1KG', 'PLUMS 1KG', 'RULAN 1KG', 'PUHUL DOSI 1KG']
    itemInCart = ['ARALIYA KEERI SAMBA 5KG', 'ARALIYA WHITE RAW 5KG', 'NIPUNA KEERI SAMBA 1KG']

    customerId= "OPEN"
    objRealTimeRecomandationClass =RealTimeRecomandationClass()
    recom=objRealTimeRecomandationClass.start(itemInCart,customerId)
    print(recom)




    return ("Success")


@app.route('/rfm')
def rfm():

    rfm= RfmClass()
    rfm.insertCsv()
    rfm.rfm()

    return ("Success")


if __name__ == "__main__":
    app.run(debug=True)