# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import datetime
# useful for handling different item types with a single interface
import time
import pymongo
from pymongo.errors import DuplicateKeyError
from sinanews.items import SinanewsItem


class SinanewsPipeline:
    """数据持久化：将数据存放到mongodb中
    """

    def __init__(self, host, port, db_name, collection_name):
        self.host = host
        self.port = port
        self.db_name = db_name
        self.collection_name = collection_name
        self.client = None
        self.db = None
        self.collection = None

    @classmethod
    def from_crawler(cls, crawler):
        """自带的方法，这个方法可以重新返回一个新的pipline对象，并且可以调用配置文件中的参数
        """
        return cls(
            # 获取MongoDB数据库配置信息
            host=crawler.settings.get("MONGO_HOST"),
            port=crawler.settings.get("MONGO_PORT"),
            # 获取SinaNews库
            db_name=crawler.settings.get("SINA_DB_NAME"),
            # mongodb中数据的集合按照日期存储
            collection_name=crawler.settings.get("COLLECTION_NAME_PREFIX")
                            + "_" + time.strftime("%Y%m%d", time.localtime())
        )

    def open_spider(self, spider):
        """开始爬虫的操作，主要就是连接数据库及对应的集合
        """
        self.client = pymongo.MongoClient(self.host, self.port)
        self.db = self.client[self.db_name]
        self.collection = self.db[self.collection_name]

    def close_spider(self, spider):
        """关闭爬虫操作的时候，需要将数据库断开
        """
        self.client.close()

    def process_item(self, item, spider):
        """处理每一条数据，需要将item返回
        注意：判断新闻是否是今天的，每天只保存当天产出的新闻，这样可以增量的添加新的新闻数据源
        """
        if isinstance(item, SinanewsItem):
            try:
                # TODO 物料去重逻辑，根据title进行去重，去重逻辑在画像处理环节实现

                # 获取当前新闻的时间戳
                cur_time = int(time.mktime(time.strptime(item['ctime'], '%Y-%m-%d %H:%M')))

                # str_today = str(datetime.date.today())
                # 每次爬取新闻的时候是爬取前一天的
                yesterday = str(datetime.date.today() - datetime.timedelta(days=1))
                min_time = int(time.mktime(time.strptime(yesterday + " 00:00:00", '%Y-%m-%d %H:%M:%S')))
                max_time = int(time.mktime(time.strptime(yesterday + " 23:59:59", '%Y-%m-%d %H:%M:%S')))
                # 如果在24小时范围内，则存入当天的集合中
                if min_time < cur_time <= max_time:
                    self.collection.insert_one(dict(item))
            except DuplicateKeyError:
                """
                说明有重复
                """
                pass
        return item
