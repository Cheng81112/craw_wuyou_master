import pymysql
import pandas as pd



print('连接到mysql服务器...')

conn = pymysql.connect(host='127.0.0.1', user='root', passwd='685568', db='recruitment_info', port=3306, charset='utf8')
print('数据库连接成功!')
cur = conn.cursor()

#判断表是否存在，若存在则删除此表
cur.execute("DROP TABLE IF EXISTS INFORMATION")
#创建表
sql = """CREATE TABLE INFORMATION(
            pos varchar(255),
            company varchar(255),
            city varchar(255),
            exp varchar(255),
            fuli varchar(255),
            shijian varchar(255),
            guimo varchar(255),
            yewu varchar(255),
            leixing varchar(255),
            href varchar(255))      
        """

try:#如果出现异常对异常处理
    # 执行SQL语句
    cur.execute(sql)
    print("创建数据库表成功")
except Exception as e:
    print("创建数据库失败：case%s" % e)


csv_name = '招聘信息3.csv'
f = pd.read_csv(csv_name, encoding="utf-8")


datas = list(f.values)

for i in datas:
    # 用sql语言写入数据表
    data = tuple(i)

    # sql = """insert into INFORMATION values{}""".format(data)

    sql = 'INSERT INTO INFORMATION(pos,company,city,exp,fuli,shijian,guimo,yewu,leixing,href) VALUES ("{}","{}","{}","{}","{}","{}","{}","{}","{}","{}")'.format(i[0],i[1],i[2],i[3],i[4],i[5],i[6],i[7],i[8],i[9])
    # sql = sql_0 %  (repr("职位名称"), repr('公司名称'), repr('所在城市'), repr('经验要求'), repr('公司福利'),
    #                repr('发布时间'), repr('公司规模'), repr('业务范围'), repr('公司类型'), repr('详情页面'))
    print(sql)
    # try:
    cur.execute(sql)

    conn.commit()  # 进行数据库提交，写入数据库

    # except:
    #     continue
    # cur.rollback()  # 数据回滚，多次操作要么都执行，要么都不执行
    # print('写入失败')

# 关闭游标
cur.close()
# 提交
conn.commit()

# 关闭数据库连接
conn.close()

# 打印结果
print("")
print("Done! ")
print("")
# columns = str(sheet.ncols)
# rows = str(sheet.nrows)
# print("我刚导入了 ", columns, " 列 and ", rows, " 行数据到MySQL!")
