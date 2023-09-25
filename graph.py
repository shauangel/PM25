import pymongo
from datetime import datetime
import csv
from itertools import product
import matplotlib.pyplot as plt
import numpy as np


myclient = pymongo.MongoClient("mongodb+srv://anchi:XZhipmZScJl2Cf2j@pm25.s5e4neg.mongodb.net/")
mydb = myclient["PM25"]
mycol = mydb["Records"]


if __name__ == "__main__":
    with open('data/site_info.csv', 'r', encoding='utf-8') as site_file:
        reader = csv.DictReader(site_file)
        site_dict = list(reader)

    station_name = list(set([s['station_name'].split('(2')[0] for s in site_dict]))
    x_time = [str(i[0]) + '-' + '{:02d}'.format(i[1])
              for i in list(product(range(2019, 2022), range(1, 13)))]

    for n in station_name:
        print(n)
        month = {key: np.nan for key in x_time}
        mydoc = mycol.find({'site':{'$regex':'^' + n + ''}})
        for r in mydoc:
            print(r)
            date_object = datetime.strptime(r['timestamp'], "%Y-%m-%d")
            time = str(date_object.year) + '-' + '{:02d}'.format(date_object.month)
            if month[time] is np.nan:
                month[time] = []
            month[time].append(r['PM25'])

        y_PM25 = []
        for k, v in month.items():
            if v is not np.nan:
                month[k] = sum(v)/len(v)
            y_PM25.append(month[k])

        # draw
        plt.rcParams['font.family'] = ['Heiti TC']
        plt.figure(figsize=(9,5))
        plt.title(n)
        plt.ylabel('PM25')
        plt.xlabel('時間')
        plt.ylim(0, 150)
        plt.xlim(0,35)
        plt.xticks(ticks=range(36), labels=x_time, rotation=45)
        plt.plot(range(36), y_PM25, 'r')
        plt.savefig("graph/" + n)
