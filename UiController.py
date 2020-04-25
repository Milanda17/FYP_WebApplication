from PyQt5 import QtWidgets, uic
import importlib
from UiContent import UiContentClass
import sys
import AprioriComm
import AprioriPersonalized
from AprioriPersonalized import AprioriPerClass
from AprioriComm import AprioriCommClass



Ui_MainWindow, QtBaseClass = uic.loadUiType("MainWindow.ui")
rulePageUi, rulePageBase = uic.loadUiType("rule.ui")
recPageUi, recPageBase = uic.loadUiType("recommendation.ui")


class App(QtWidgets.QMainWindow, Ui_MainWindow):



        def __init__(self):
            QtWidgets.QMainWindow.__init__(self)
            Ui_MainWindow.__init__(self)
            self.setupUi(self)
            self.recButton.clicked.connect(self.showRec)
            self.ruleButton.clicked.connect(self.showRule)

        def showRec(self):
            self.child_win = recUi(self)
            self.child_win.show()

        def showRule(self):
            self.child_win = ruleUi(self)
            self.child_win.show()



class recUi(recPageBase, recPageUi):
    def __init__(self, parent=None):
        recPageBase.__init__(self, parent)
        self.setupUi(self)

class ruleUi(rulePageBase, rulePageUi):
    def __init__(self, parent=None):
        rulePageBase.__init__(self, parent)

        self.setupUi(self)
        self.itemList.clear()
        globleItemList = []
        for x in row:
            bad_chars = ['(', ')', ',', "'"]
            itemRecorrect = str(x)
            for i in bad_chars:
                itemRecorrect = itemRecorrect.replace(i, '')

            globleItemList.append(itemRecorrect)
            self.itemList.addItem(str(itemRecorrect))

        def search():

            seacrh = self.searchEdit.text()

            self.itemList.clear()

            res = list(filter(lambda x: seacrh in x, globleItemList))
            print(globleItemList)
            for x in res:
                self.itemList.addItem(x)

        def cleanMethod():


            search()

        def uiRuelCom():

            itemForRule = []
            itemList = [self.ruleItemList.item(i).text() for i in range(self.ruleItemList.count())]

            for item in itemList:
                itemForRule.append(item)

            print(itemForRule)

            mounth = self.mounthEdit.text()
            year = self.yearEdit.text()

            year = year + "-"
            print(mounth, year)

            minSupp = 3
            #for minSupp in range(2, 5, +1):
            print(minSupp)
            importlib.reload(AprioriComm)
            objAprioriComm = AprioriCommClass(minSupp)
            start, end = objAprioriComm.indirect(int(mounth), year)  # 1 ,2019
            mounthlyItem = objAprioriComm.getSearchTransListSet(start, end)
            objAprioriComm.start(itemForRule, mounthlyItem)
                #minSupp=minSupp+1
        # print("LOOOOOOOOOOOOOOOOOOOOOOOOOOOOOp",minSupp)

            return ("Success")

        def uiRuelPer():

            importlib.reload(AprioriPersonalized)
            objAprioriPersonalized = AprioriPerClass()
            userList = objAprioriPersonalized.getUserList()
            for user in userList:
                importlib.reload(AprioriPersonalized)
                objAprioriPersonalized.start(user)
                objAprioriPersonalized.getFrequentPattern(user)

            return ("Success")

        self.ruleUserButton.clicked.connect(uiRuelPer)
        self.searchButton.clicked.connect(cleanMethod)
        self.ruleButton.clicked.connect(uiRuelCom)


if __name__ == "__main__":
    app=QtWidgets.QApplication.instance()
    objUiContent = UiContentClass()
    row=[]
    row = objUiContent.getAllItemFromDatabase()
    if not app:
         app = QtWidgets.QApplication(sys.argv)

    window = App()
    window.show()
    sys.exit(app.exec_())







