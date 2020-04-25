import builtins

import pymysql
from DictList import DictList

d1 = DictList()
d2 = DictList()


class RealTimeRecomandationClass():

    def start(self,itemInCart,customerId):

        itemString=self.queryForItemInCart(itemInCart)
        freqSet = dict()
        recommendationList =[]
        currFreqTermSet = self.listconvert(itemInCart)
        freqOneTermSet = self.getSubSetWithRule(currFreqTermSet,customerId,itemString)
        currFreqTermSet = freqOneTermSet
        k = 1
        while currFreqTermSet != set():
                #print(k)
                freqSet[k] = currFreqTermSet
                k += 1
                currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k)
                currFreqTermSet = self.getSubSetWithRule(currCandiItemSet,customerId,itemString)


        sortList=list(d1.values())

        sortList.sort(reverse=True)
        sortList = list(dict.fromkeys(sortList))

        for x in sortList:

            for item, confidence in d1.items():

                if confidence == x:

                    li = list(item.split(","))


                    builtins.set
                    if (set(li).issubset(set(itemInCart))):

                            li2 = list(d2.get(item).split(","))

                            for x in li2:

                                if x not in itemInCart:
                                    #

                                    if x not in recommendationList:
                                        recommendationList.append(x)

                                # put flag if you want break the loop


        return recommendationList




    def listconvert(self,itemInCart):
        itemSet_ = set()

        for x in itemInCart:

            itemSet_.add(frozenset([x]))
        return itemSet_

    def getJoinedItemSet( self,termSet, k):

            return set([term1.union(term2) for term1 in termSet for term2 in termSet
                        if len(term1.union(term2))==k])

    def getSubSetWithRule(self,currFreqTermSet,customerId,queryString):

        itemSet_=set()
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        mainString = "SELECT LEFT_ITEM,CONFIDENCE,RIGHT_ITEM FROM FINALYEARPROJECT.`ASSOCIATE ITEM` WHERE CUSTOMER_ID='"
        stringWithUser=mainString+customerId
        stringWithUser=stringWithUser + "' AND "
        for x in (currFreqTermSet):
            combineString = ""
            for item in list(x):
                patternDes = " LEFT_ITEM like '%"
                patternDes = patternDes + item
                patternDes = patternDes + "%' AND "
                combineString = combineString + patternDes
            queryWithAnd = stringWithUser + combineString
            queryWithAnd= queryWithAnd+queryString
            #queryOutwithAnd = queryWithAnd.rsplit(' ', 1)[0]

            #print(queryWithAnd)
            cursor.execute(queryWithAnd)

            if 1 <= (cursor.rowcount):
                itemSet_.add(x)
                for row in cursor.fetchall():
                   if row[0] not in d1:
                        #consider the same left with different right// limitation
                        d1[row[0]] = row[1]
                        d2[row[0]] = row[2]


            currFreqTermSet = itemSet_

        return currFreqTermSet


    def queryForItemInCart(self,itemInCart):
        queryString="("
        for x in itemInCart:
            itemGenRule = " ITEM_GEN_RULE='"
            itemGenRule= itemGenRule+ x
            itemGenRule= itemGenRule+ "' OR "
            queryString=queryString+itemGenRule
        queryString= queryString+ "ITEM_GEN_RULE='AAA'"
        queryString =queryString+ ")"





        return queryString
