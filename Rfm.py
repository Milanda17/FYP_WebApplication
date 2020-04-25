import csv
import sys
import pymysql
import pandas as pd

from datetime import datetime, date

class RfmClass():

    def insertCsv(self):

        db = pymysql.connect("127.0.0.1", "root", "password", "finalyearproject")
        cursor = db.cursor()
        sql=("SELECT * FROM finalyearproject.`test rfm`")
        csv_file_path = 'data/data.csv'

        try:
            cursor.execute(sql)
            rows = cursor.fetchall()
        finally:
            db.close()
            print("close")

        if rows:
            result = list()
            column_names = list()
            for i in cursor.description:
                column_names.append(i[0])

            result.append(column_names)
            for row in rows:
                result.append(row)
            with open(csv_file_path, 'w', newline='') as csvfile:
                csvwriter = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                for row in result:
                    csvwriter.writerow(row)
        else:
            sys.exit("No rows found for query: {}".format(sql))



    def rfm(self):
        inputfile = 'data/data.csv'
        outputfile= 'data/Rfm.csv'
        inputdate = '2018-01-01' # year/month/date
        #inputdate = str(date.today()) # year/month/date
        print(" ")
        print("---------------------------------------------")
        print(" Calculating RFM segmentation for " + inputdate)
        print("---------------------------------------------")

        NOW = datetime.strptime(inputdate, "%Y-%m-%d")

        orders = pd.read_csv(inputfile, sep=',')
        orders['order_date'] = pd.to_datetime(orders['order_date'])

        rfmTable = orders.groupby('customer').agg({'order_date': lambda x: (NOW - x.max()).days,  # Recency
                                                   'order_id': lambda x: len(x),  # Frequency
                                                   'grand_total': lambda x: x.sum()})  # Monetary Value

        rfmTable['order_date'] = rfmTable['order_date'].astype(int)
        rfmTable.rename(columns={'order_date': 'recency',
                                 'order_id': 'frequency',
                                 'grand_total': 'monetary_value'}, inplace=True)

        quantiles = rfmTable.quantile(q=[0.25, 0.5, 0.75])

        quantiles = quantiles.to_dict()
        rfmSegmentation = rfmTable
        rfmSegmentation['R_Quartile'] = rfmSegmentation['recency'].apply(self.RClass, args=('recency', quantiles,))
        rfmSegmentation['F_Quartile'] = rfmSegmentation['frequency'].apply(self.FMClass, args=('frequency', quantiles,))
        rfmSegmentation['M_Quartile'] = rfmSegmentation['monetary_value'].apply(self.FMClass,
                                                                                args=('monetary_value', quantiles,))

        rfmSegmentation['RFMClass'] = rfmSegmentation.R_Quartile.map(str) + rfmSegmentation.F_Quartile.map(
            str) + rfmSegmentation.M_Quartile.map(str)
        rfmSegmentation.to_csv(outputfile, sep=',')

        print(" ")
        print(" DONE! Check %s" % (outputfile))
        print(" ")


    # two classes for the RFM segmentation since, being high recency is bad, while high frequency and monetary value is good.
    # Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
    def RClass(self,x, p, d):
        if x <= d[p][0.25]:
            return 1
        elif x <= d[p][0.50]:
            return 2
        elif x <= d[p][0.75]:
            return 3
        else:
            return 4


    # Arguments (x = value, p = recency, monetary_value, frequency, k = quartiles dict)
    def FMClass(self,x, p, d):
        if x <= d[p][0.25]:

            return 4
        elif x <= d[p][0.50]:
            return 3
        elif x <= d[p][0.75]:
            return 2
        else:
            return 1


