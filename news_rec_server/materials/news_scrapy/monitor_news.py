# -*- coding: utf-8 -*-
import sys, time
import pymongo
from sinanews.settings import MONGO_HOST, MONGO_PORT, SINA_DB_NAME, COLLECTION_NAME_PREFIX

if __name__ == "__main__":
    # 用于监控爬取新闻的状态，是否小于指定的新闻数量
    news_num = int(sys.argv[1])
    time_str = time.strftime("%Y%m%d", time.localtime())

    # 实际的collection_name
    collection_name = COLLECTION_NAME_PREFIX + "_" + time_str

    # 链接数据库
    client = pymongo.MongoClient(MONGO_HOST, MONGO_PORT)
    db = client[SINA_DB_NAME]
    collection = db[collection_name]

    # 查找当前集合中所有文档的数量
    cur_news_num = collection.estimated_document_count()

    if cur_news_num < news_num:
        print("the news nums of {}_{} collection is {} and less then {}.".format(
            COLLECTION_NAME_PREFIX, time_str, cur_news_num, news_num))