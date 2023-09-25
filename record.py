
import os
import csv
import pymongo
from datetime import datetime


myclient = pymongo.MongoClient("mongodb+srv://anchi:XZhipmZScJl2Cf2j@pm25.s5e4neg.mongodb.net/")
mydb = myclient["PM25"]
mycol = mydb["Records"]


# 資料前處理
def load_data():
    # 輸入2019~2021每日紀錄
    files = [f for f in os.listdir('data/') if f.endswith('.csv')]

    # 將該日紀錄加入總匯
    for i in range(362,len(files)):
        storage = {}
        print(files[i])
        print("Process: " + str(i+1) + '/365')
        # 開檔案，呼出資料
        with open('data/' + files[i], 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            data = list(reader)

        # 讀取日期時間
        date = files[i].removesuffix('.csv').split('_')[2]
        date_object = datetime.strptime(date, "%Y%m%d")
        timestamp = str(date_object.year) + '-'\
                    + '{:02d}'.format(date_object.month) + '-'\
                    + '{:02d}'.format(date_object.day)
        print("Records Cleaning...")
        for i in range(len(data)):
            print(str(i+1) + '/' + str(len(data)))
            # 判斷資料庫裡面是否從在該測站
            if data[i]['device_id'] not in storage.keys():
                storage[data[i]['device_id']] = { "timestamp" : timestamp,
                                            "site" : data[i]['SiteName'],
                                            "PM25" : []}
            # 加入資料
            storage[data[i]['device_id']]['PM25'].append(float(data[i]['PM25']))
        records = []
        print("Creating Records...")
        for k in storage.keys():
            temp = storage[k]
            temp['ID'] = k
            temp['PM25'] = sum(temp['PM25'])/len(temp['PM25'])
            records.append(temp)
            print(temp)
        mycol.insert_many(records)


if __name__ == "__main__":

    #load_data()

    """
    display = data_reshape(data)
    with open('2019.json', 'w', encoding='utf-8') as df:
        json.dump(display, df)
        df.close()
    print('data saved')

    for site in list(data.keys()):
        print(site)
        x_time = sorted(data[site])
        y_PM25 = []
        for x in x_time:
            PM25 = [int(list(v.values())[0]) for v in data[site][x]]
            avg = sum(PM25)/len(PM25)
            y_PM25.append(avg)

        plt.figure()
        plt.plot(x_time, y_PM25, 'ro--', linewidth=2, markersize=6)
        plt.savefig('graph/' + site)
        plt.clf()
        """
    with open('data/site_info.csv', 'r', encoding='utf-8') as site_file:
        reader = csv.DictReader(site_file)
        site_dict = list(reader)

    station_name = list(set([s['station_name'].split('(2')[0] for s in site_dict]))
    print(len(station_name))




