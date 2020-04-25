from collections import defaultdict
import pymysql



transListSet = []

class AprioriCommClass(object):
    def __init__(self, minSupp):
        """ Parameters setting
        """
        self.minSupp = minSupp  # min support (used for mining frequent sets)


    def fit(self,transListSet):
        """ Run the apriori algorithm, return the frequent *-term sets.
        """
        #transListSet = self.getSearchTransListSet(productlist)  # get transactions (list that contain sets)
        #transListSet=self.removeItemUseInRule(mounthlyItem,productlist)
        itemSet = self.getOneItemSet(transListSet)  # get 1-item set
        itemCountDict = defaultdict(int)  # key=candiate k-item(k=1/2/...), value=count
        freqSet = dict()  # a dict store all frequent *-items set

        self.transLength = len(transListSet)  # number of transactions
        self.itemSet = itemSet

        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet,
                                                  itemCountDict, self.minSupp)

        # Main loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  # save the result
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k)  # get new candiate k-terms set
            currFreqTermSet = self.getItemsWithMinSupp(transListSet, currCandiItemSet,
                                                       itemCountDict, self.minSupp)  # frequent k-terms set

        #
        self.itemCountDict = itemCountDict
        self.freqSet = freqSet  # Only frequent items(a dict: freqSet[1] indicate frequent 1-term set )
        return itemCountDict, freqSet

    def getSupport(self, item):
        """ Get the support of item """
        return self.itemCountDict[item] / self.transLength

    def getJoinedItemSet(self, termSet, k):
        """ Generate new k-terms candiate itemset
        """
        return set([term1.union(term2) for term1 in termSet for term2 in termSet
                    if len(term1.union(term2)) == k])

    def getOneItemSet(self, transListSet):
        """ Get unique 1-item set in `set` format to easy to make subset
        """
        itemSet = set()
        for line in transListSet:
            for item in line:
                itemSet.add(frozenset([item]))
        return itemSet


    def getCount(self, differnce):

        """ Get pattern count
        """
        list3 = []
        for txn in transListSet:

            if (all(x in txn for x in differnce)):
                list3.append(txn)

        return len(list3)

    def getItemsWithMinSupp(self, transListSet, itemSet, freqSet, minSupp):
        """ Get frequent item set using min support
        """
        itemSet_ = set()
        localSet_ = defaultdict(int)
        for item in itemSet:
            freqSet[item] += sum([1 for trans in transListSet if item.issubset(trans)])
            localSet_[item] += sum([1 for trans in transListSet if item.issubset(trans)])

        # Only conserve frequent item-set

        for item, cnt in localSet_.items():
            itemSet_.add(item) if float(cnt) >= minSupp else None

        return itemSet_

    def getPatternRule(self, freqSet, bestPatternLenth,productlist):
        """ Get rule of best pattern
        """
        patternList = []
        itemList = []
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        a = db.cursor()
        for key, value in freqSet.items():

            for itemset in value:

                lenght = (len(list(itemset)))
                if (lenght != bestPatternLenth):

                    itemList.append(list(itemset))
                else:
                    patternList.append(list(itemset))

        print( "======================================================================================================================")
        print("Frequent pattern related to "+productlist)
        print(patternList)
        print("======================================================================================================================")

        count=("SELECT LEFT_ITEM,RIGHT_ITEM ,CONFIDENCE FROM finalyearproject.`associate item` where ITEM_GEN_RULE=%s ")
        number_of_rows=a.execute(count, productlist)
        left=[]
        right=[]
        pro=[]
        for row in a.fetchall():

            left.append(row[0])
            right.append(row[1])
            pro.append(row[2])


        if(number_of_rows>0 and bestPatternLenth >1):


            sqlDelete = ("DELETE  FROM FINALYEARPROJECT.`ASSOCIATE ITEM` WHERE CUSTOMER_ID='OPEN' AND ITEM_GEN_RULE=%s ")
            cursor.execute(sqlDelete, productlist)
            db.commit()
            print("delettttttt")


        for pattern in patternList:

            patternCount = self.getCount(pattern)

            for item in (itemList):
                flag = 0

                if (all(x in pattern for x in item)):
                    flag = 1

                if (flag):
                    differnce = (set(pattern) - set(item))
                    x = 0
                    probability=0
                    differnceCount = self.getCount(differnce)

                    if (0.5<=patternCount / differnceCount):

                        differnceString = ','.join(differnce)
                        itemString = ','.join(item)
                        for (l, R,P) in zip(left, right,pro):




                            if (len(l)==len(differnceString) and len(R)==len(itemString)):

                                leftLIst = list(l.split(","))
                                rightLIst = list(R.split(","))
                                leftSet=set(leftLIst)
                                rightSet=set(rightLIst)

                                if(0==(len(leftSet.intersection(differnce))-len(leftSet.union(differnce))) and 0==(len(rightSet.intersection(item))-len(rightSet.union(item)))):


                                    x=1
                                    probability=P

                        if(x==0):


                            print("AAAAAAAAAAAAAAAAAAAAAAAAAAa",differnce, "==>", item, '==== Confidence ====> ', patternCount / differnceCount)

                            sqlInsert = ("INSERT INTO FINALYEARPROJECT.`ASSOCIATE ITEM`(ITEM_GEN_RULE,CUSTOMER_ID,CONFIDENCE,LEFT_ITEM,RIGHT_ITEM ) VALUE (%s,%s,%s,%s,%s)")
                            insertValue = (productlist, "OPEN", patternCount / differnceCount, differnceString, itemString)
                            cursor.execute(sqlInsert, insertValue)
                            db.commit()

                        else:
                            print("+++++++++++++++++++++++++++++++++++++++++++++++++++")
                            print(differnce, "==>", item, '==== Confidence ====> ', patternCount / differnceCount)
                            confidenceWithlastMonth = ((patternCount / differnceCount) + probability) / 2
                            print(differnce, "==>", item, '==== Confidence ====> ', confidenceWithlastMonth)
                            sqlInsert = ("INSERT INTO FINALYEARPROJECT.`ASSOCIATE ITEM`(ITEM_GEN_RULE,CUSTOMER_ID,CONFIDENCE,LEFT_ITEM,RIGHT_ITEM ) VALUE (%s,%s,%s,%s,%s)")
                            insertValue = (
                                productlist, "OPEN", confidenceWithlastMonth, differnceString, itemString)
                            cursor.execute(sqlInsert, insertValue)
                            db.commit()







    def getBestPatternLenth(self, freqSet):
        """ Get best pattern length.last pattern content the all sub pattern of item set
        """

        try:
            for key, value in self.freqSet.items():
                for item in value:
                    length = len(item)

            if (length > 1):

                return length
            else:

                print("Amount of the minSupport is higher can't generating rule")
                length = 0
                return length
        except:

            print("Amount of the minSupport is higher")
            length = 0
            return length

    def start(self,items,mounthlyItem):
            """ Start
            """


            for x in items:


                transListSet,temp  = self.removeItemUseInRule(mounthlyItem, x)
                itemCountDict, freqSet = self.fit(transListSet)
                bestPatternLenth = self.getBestPatternLenth(freqSet)
                self.getPatternRule(freqSet, bestPatternLenth,x)
                mounthlyItem=temp

                transListSet.clear()



    def getSearchTransListSet(self,start,end):
        """ get the search transaction from database
        """
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        result = {}
        # execute SQL query using execute() method.
        """sqlSearch = ("SELECT * FROM FINALYEARPROJECT.`ORDER DETAILS` AS A "
                     "INNER JOIN FINALYEARPROJECT.`CUSTOMERS ORDER` AS B "
                     "ON A.INVOICE_NUMBER=B.INVOICE_NUMBER "
                     "WHERE B.CUSTOMER_ID=%s")"""

        sqlSearch = ("SELECT A.invoice_number,A.order_item FROM FINALYEARPROJECT.`ORDER  DETAILS` AS A "
                     "INNER JOIN FINALYEARPROJECT.`customers invoice` AS B "
                     "ON A.INVOICE_NUMBER=B.INVOICE_NUMBER "
                     "WHERE B.CUSTOMER_ID=%s and date BETWEEN %s AND %s")
        customerId = ("OPEN",start,end)
        cursor.execute(sqlSearch, customerId)
        # Fetch a single row using fetchone() method.

        for row in cursor.fetchall():

            if row[0] in result:
                result[row[0]].append(row[1])

            else:
                result[row[0]] = [row[1]]
        appendlist = list(result.values())


        ''''for items in appendlist:
            for search in items:
                if productlist in search:
                    items.remove(productlist)
                    transListSet.append(set(items))'''''

        db.close()

        return appendlist



    def removeItemUseInRule(self,mounthlyItem,productlist):


        y=[]

        for items in mounthlyItem:
            new_list = items.copy()
            y.append(new_list)

            for search in items:

                if  productlist == search:

                    items.remove(productlist)
                    transListSet.append(set(items))

        #mounthlyItem = new_list.copy()
        return transListSet,y





    def jun(self,year):
        start = "01-01"
        end = "01-31"
        return year + start, year + end

    def feb(self,year):
        start = "02-01"
        end = "02-28"
        return year + start, year + end

    def mar(self,year):
        start = "03-01"
        end = "03-31"
        return year + start, year + end

    def apr(self,year):
        start = "04-01"
        end = "04-30"
        return year + start, year + end

    def may(self,year):
        start = "05-01"
        end = "05-31"
        return year + start, year + end

    def june(self,year):
        start = "06-01"
        end = "06-30"
        return year + start, year + end

    def jule(self,year):
        start = "07-01"
        end = "07-31"
        return year + start, year + end

    def aug(self,year):
        start = "08-01"
        end = "08-31"
        return year + start, year + end

    def sep(self,year):
        start = "09-01"
        end = "09-30"
        return year + start, year + end

    def ocu(self,year):
        start = "10-01"
        end = "10-31"
        return year + start, year + end

    def nov(self,year):
        start = "11-01"
        end = "11-30"
        return year + start, year + end

    def dec(self,year):
        start = "12-01"
        end = "12-31"
        return year + start, year + end

    def indirect(self ,i, year):
        switcher = {
            1: self.jun,
            2: self.feb,
            3: self.mar,
            4: self.apr,
            5: self.may,
            6: self.june,
            7: self.jule,
            8: self.aug,
            9: self.sep,
            10: self.ocu,
            11: self.nov,
            12: self.dec

        }
        func = switcher.get(i, 'Invalid')
        return func(year)


