from sqlite3 import Date

from peewee import *

from conf import BASE_DIR
from utils.log import api_logger

# 创建 SQLite 数据库连接
db = SqliteDatabase(BASE_DIR / 'db/social-auto-upload.db')


# 定义模型
class UploadRecord(Model):
    platform = CharField()
    title = CharField()
    file_name = CharField()
    account_name = CharField()
    upload_date = DateField()

    class Meta:
        database = db  # 指定数据库


# 创建表
db.connect()
db.create_tables([UploadRecord])

# 插入数据
UploadRecord.create(platform='DouYin',
                    title='Hello, World!',
                    file_name='hello.mp4',
                    account_name='Alice',
                    upload_date=Date.today())

# 查询数据
for upload_record in UploadRecord.select():
    api_logger.info(upload_record)

# 关闭连接
db.close()
