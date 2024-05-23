from tkinter import INSERT

#导入需要使用到的数据模块
import pandas as pd
import pymysql

#读入数据
filepath = './train.xlsx'
data = pd.read_excel(filepath)

#建立数据库连接
db = pymysql.connect(host = 'localhost',user = 'root',password = '13260615599',database = '项目表')
#获取游标对象
cursor = db.cursor()

#插入数据语句
query = "insert into 'train'(start_time,arrival_time,start_location,arrival_location,haoshi,checi,price,yupiao) values (%s,%s,%s,%s,%s,%s,%s,%s)"

#迭代读取每行数据
#values中元素有个类型的强制转换，否则会出错的
#应该会有其他更合适的方式，可以进一步了解
for r in range(0, len(data)):
    start_time = data.iloc[r,0]
    arrival_time = data.iloc[r,1]
    start_location = data.iloc[r,2]
    arrival_location = data.iloc[r,3]
    haoshi = data.iloc[r, 4]
    checi = data.iloc[r, 5]
    price = data.iloc[r, 6]
    yupiao = data.iloc[r, 7]
    values = (str(start_time), str(arrival_time), str(start_location),str(arrival_location),str(haoshi),str(price),str(yupiao),)
    cursor.execute(query, values)

#关闭游标，提交，关闭数据库连接
#如果没有这些关闭操作，执行后在数据库中查看不到数据
cursor.close()
db.commit()
db.close()




#重新建立数据库连接
db = pymysql.connect(host = 'localhost',user = 'root',password = '13260615599',database = '项目表')
cursor = db.cursor()
#查询数据库并打印内容
cursor.execute("select * from train")
results = cursor.fetchall()
for row in results:
    print(row)
#关闭
cursor.close()
db.commit()
db.close()