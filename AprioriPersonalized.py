import re
from collections import defaultdict
import pymysql
from DictList import DictList

transListSet = []


class AprioriPerClass():

    def getUserList(self):
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        # execute SQL query using execute() method.

        cursor.execute("SELECT CUSTOMER_ID FROM FINALYEARPROJECT.`CUSTOMER` WHERE STATUS='INIT'")

        # Fetch a single row using fetchone() method.

        for row in cursor.fetchall():
            transListSet.append(row)

        db.close()
        return transListSet

    def fit(self, user):
        """ Run the apriori algorithm, return the frequent *-term sets.
        """
        # Initialize some variables to hold the tmp result

        transListSet, userRecorrect = self.getSearchTransListSet(user)  # get transactions (list that contain sets)
        minSupp = ((len(transListSet)) / 100) * 50
        itemSet = self.getOneItemSet(transListSet)  # get 1-item set
        itemCountDict = defaultdict(int)  # key=candiate k-item(k=1/2/...), value=count
        freqSet = dict()  # a dict store all frequent *-items set

        self.transLength = len(transListSet)  # number of transactions
        self.itemSet = itemSet

        # Get the frequent 1-term set
        freqOneTermSet = self.getItemsWithMinSupp(transListSet, itemSet,
                                                  itemCountDict, minSupp)

        # Main loop
        k = 1
        currFreqTermSet = freqOneTermSet
        while currFreqTermSet != set():
            freqSet[k] = currFreqTermSet  # save the result
            k += 1
            currCandiItemSet = self.getJoinedItemSet(currFreqTermSet, k)  # get new candiate k-terms set
            currFreqTermSet = self.getItemsWithMinSupp(transListSet, currCandiItemSet,
                                                       itemCountDict, minSupp)  # frequent k-terms set

        #
        self.itemCountDict = itemCountDict
        self.freqSet = freqSet  # Only frequent items(a dict: freqSet[1] indicate frequent 1-term set )
        return itemCountDict, freqSet, userRecorrect

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

    def getPatternRule(self, freqSet, bestPatternLenth, user):
        """ Get rule of best pattern
        """
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        patternList = []
        itemList = []
        for key, value in freqSet.items():

            for itemset in value:

                lenght = (len(list(itemset)))
                if (lenght != bestPatternLenth):

                    itemList.append(list(itemset))
                else:
                    patternList.append(list(itemset))

        print(
            "======================================================================================================================")
        print("Frequent pattern related to user id ", user)

        sqlDelete = ("DELETE  FROM FINALYEARPROJECT. `CUSTOMER FREQUENT PATTERN` WHERE CUSTOMER_ID=%s ")
        deleteUser = (user)
        cursor.execute(sqlDelete, deleteUser)
        db.commit()

        sqlDelete = ("DELETE  FROM FINALYEARPROJECT.`ASSOCIATE ITEM` WHERE CUSTOMER_ID=%s ")
        deleteUser = (user)
        cursor.execute(sqlDelete, deleteUser)
        db.commit()

        patternNumber = 0
        for pattern in patternList:
            patternNumber = patternNumber + 1
            print(pattern, user, patternNumber)

            patternString = ','.join(pattern)  # convert the pattern list to string
            sqlInsert = (
                "INSERT INTO FINALYEARPROJECT. `CUSTOMER FREQUENT PATTERN`(PATTERN_NUMBER, CUSTOMER_ID, PATTERN_DES) VALUE (%s,%s,%s)")

            insertValue = (patternNumber, user, patternString)
            cursor.execute(sqlInsert, insertValue)
            db.commit()
        for pattern in patternList:

            patternCount = self.getCount(pattern)

            for item in (itemList):
                flag = 0
                if (all(x in pattern for x in item)):
                    flag = 1

                if (flag):
                    differnce = (set(pattern) - set(item))

                    differnceCount = self.getCount(differnce)

                    if (0.5 <= patternCount / differnceCount):
                        print(differnce, "==>", item, '==== Confidence ====> ', patternCount / differnceCount)
                        differnceString = ','.join(differnce)
                        itemString = ','.join(item)
                        sqlInsert = (
                            "INSERT INTO FINALYEARPROJECT.`ASSOCIATE ITEM`(CUSTOMER_ID,CONFIDENCE,LEFT_ITEM,RIGHT_ITEM ) VALUE (%s,%s,%s,%s)")
                        insertValue = (user, patternCount / differnceCount, differnceString, itemString)
                        cursor.execute(sqlInsert, insertValue)
                        db.commit()
        db.close()

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
        except:
            print("Amount of the minSupport is higher")

    def start(self, user):
        itemCountDict, freqSet, userRecorrect = self.fit(user)
        bestPatternLenth = self.getBestPatternLenth(freqSet)
        self.getPatternRule(freqSet, bestPatternLenth, userRecorrect)

    def getFrequentPattern(self, user):

        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        oneCursor = db.cursor()
        cursor = db.cursor()

        sqlSearch = (
            "SELECT PATTERN_DES,PATTERN_NUMBER FROM FINALYEARPROJECT.`CUSTOMER FREQUENT PATTERN`WHERE CUSTOMER_ID=%s")

        searchValue = (user)
        oneCursor.execute(sqlSearch, searchValue)

        sqlDelete = ("DELETE  FROM FINALYEARPROJECT. `CUSTOMER FREQUENT PATTERN GROUP` WHERE CUSTOMER_ID=%s ")
        deleteUser = (searchValue)
        cursor.execute(sqlDelete, deleteUser)
        db.commit()
        row = oneCursor.fetchone()
        while row is not None:
            self.getPatternGroup(row[0], row[1], searchValue)
            row = oneCursor.fetchone()

        db.close()
        self.getCompledtedUser()

    def getPatternGroup(self, patternList, patternNumber, user):
        dbmy = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = dbmy.cursor()
        levelOne = []
        levelTwo = []
        levelThree = []
        groupList = []
        items = (str(patternList)).split(",")
        for item in items:

            sqlSearch = ("SELECT * FROM FINALYEARPROJECT.`ITEMS DETAILS`WHERE ITEM_DESC=%s ")

            searchValue = (item)
            cursor.execute(sqlSearch, searchValue)

            row = cursor.fetchone()
            while row is not None:
                levelOne.append((row[1]))
                levelTwo.append(row[4])
                levelThree.append((row[3]))
                # levelOne.append("'" + (row[1]) + "'")
                # levelTwo.append("'" + (row[4]) + "'")
                # levelThree.append("'" + (row[3]) + "'")
                row = cursor.fetchone()

        groupList.append(levelOne)
        groupList.append(levelTwo)
        groupList.append(levelThree)
        y = 0

        for x in groupList:
            y = y + 1
            patternString = ','.join(x)  # convert the pattern list to string
            sqlInsert = ("INSERT INTO FINALYEARPROJECT. `CUSTOMER FREQUENT PATTERN GROUP` "
                         "(PATTERN_NUMBER, CUSTOMER_ID, PATTERN_GROUP_DES,GROUP_LEVEL) VALUE (%s,%s,%s,%s)")

            insertValue = (patternNumber, user, patternString, y)
            cursor.execute(sqlInsert, insertValue)
            dbmy.commit()

        dbmy.close()
        return

    def jacCardSimilarity(self, x, y):
        intersection_cardinality = len(set.intersection(*[set(x), set(y)]))
        union_cardinality = len(set.union(*[set(x), set(y)]))
        return intersection_cardinality / float(union_cardinality)

    def getCompledtedUser(self):

        for level in range(1, 4, +1):
            initUserPattern = []
            initUserId = []
            comUserPattern = []
            comUserId = []
            db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
            cursor = db.cursor()

            sqlInitSearch = ("SELECT A.CUSTOMER_ID ,PATTERN_GROUP_DES FROM "
                             "(SELECT * FROM FINALYEARPROJECT.CUSTOMER WHERE STATUS='INIT') AS A "
                             "INNER JOIN "
                             "(SELECT * FROM FINALYEARPROJECT.`CUSTOMER FREQUENT PATTERN GROUP` "
                             "WHERE   GROUP_LEVEL=%s) AS B "
                             "ON A.CUSTOMER_ID=B.CUSTOMER_ID ")
            initLevel = level
            cursor.execute(sqlInitSearch, initLevel)
            # Fetch a single row using fetchone() method.

            for row in cursor.fetchall():
                initUserPattern.append(row[1])
                initUserId.append(row[0])
                sqlDelete = (
                    "DELETE  FROM FINALYEARPROJECT.`SIMILAR CUSTOMER` WHERE CUSTOMER_ID=%s AND PATTERN_LEVEL=%s ")
                deleteUser = (row[0], level)
                cursor.execute(sqlDelete, deleteUser)
                db.commit()

            sqlComSearch = ("SELECT A.CUSTOMER_ID ,PATTERN_GROUP_DES FROM "
                            "(SELECT * FROM FINALYEARPROJECT.CUSTOMER WHERE STATUS='COM') AS A "
                            "INNER JOIN "
                            "(SELECT * FROM FINALYEARPROJECT.`CUSTOMER FREQUENT PATTERN GROUP` "
                            "WHERE   GROUP_LEVEL=%s) AS B "
                            "ON A.CUSTOMER_ID=B.CUSTOMER_ID ")
            cursor.execute(sqlComSearch, level)
            # Fetch a single row using fetchone() method.

            for row in cursor.fetchall():
                comUserPattern.append(row[1])
                comUserId.append(row[0])

            for (initPattern, initId) in zip(initUserPattern, initUserId):

                d1 = DictList()
                d2 = DictList()
                simiList = []
                for (comPattern, comId) in zip(comUserPattern, comUserId):

                    d1[comPattern] = comId
                    x = initPattern.split(",")
                    y = comPattern.split(",")
                    similarity = self.jacCardSimilarity(y, x)
                    if similarity not in d2:
                        d2[similarity] = comPattern

                        # print(similarity)
                        simiList.append(similarity)
                # print(max(simiList))
                pattern = d2.get(max(simiList))
                #d1.get(pattern) this can be give two result
                sqlSimlarCustomerInsert = ("INSERT INTO FINALYEARPROJECT. `SIMILAR CUSTOMER` "
                                           "(PATTERN_LEVEL,CUSTOMER_ID,MATCHING_CUSTOMER_ID,SIMILARITY_MATCH) VALUE (%s,%s,%s,%s) ")

                insertSimlarCustomerValue = (level, initId, d1.get(pattern), max(simiList))
                cursor.execute(sqlSimlarCustomerInsert, insertSimlarCustomerValue)
                db.commit()
        db.close()

        return

    def getSearchTransListSet(self, user):
        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        result = {}
        bad_chars = ['(', ')', ',', "'"]
        userRecorrect = str(user)
        for i in bad_chars:
            userRecorrect = userRecorrect.replace(i, '')
        # execute SQL query using execute() method.

        sqlSearch = ("SELECT * FROM FINALYEARPROJECT.`ORDER  DETAILS` AS A "
                     "INNER JOIN FINALYEARPROJECT.`CUSTOMERS ORDER` AS B "
                     "ON A.INVOICE_NUMBER=B.INVOICE_NUMBER "
                     "WHERE B.CUSTOMER_ID=%s ")

        customerId = (userRecorrect)
        cursor.execute(sqlSearch, customerId)
        # Fetch a single row using fetchone() method.

        for row in cursor.fetchall():

            if row[0] in result:
                result[row[0]].append(row[1])

            else:
                result[row[0]] = [row[1]]
        appendlist = list(result.values())
        for items in appendlist:
            transListSet.append(set(items))

        db.close()
        return transListSet, userRecorrect
