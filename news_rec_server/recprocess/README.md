### Redis中key的详细说明

**前端展示信息的静态和动态信息**

- 静态信息，存在db_num=1中（可以在命令行中使用select 1跳转到对应的db）， 存储的形式是string(也就是存的时候用set, 取的时候用get), 具体格式：static_news_detail:4862eef1-79f1-4117-99e7-b857b27c5073，其中static_news_detail:表示的是标识符前缀，4862eef1-79f1-4117-99e7-b857b27c5073表示的是news_id
    ```shell
        命令行中输入：get static_news_detail:4862eef1-79f1-4117-99e7-b857b27c5073
        显示信息：
        {'news_id': '4862eef1-79f1-4117-99e7-b857b27c5073', 'title': '探索“五水共治”，建运河文化园 浙江绍兴积极落实河湖长制', 'ctime': '2021-12-09 05:15', 'content': '《人民日报》（2021年12月09日第12版）本报杭州12月8日电（记者王珏）近年来，浙江绍兴市越城区积极落实河湖长制，探索“五水共治”实践窗口，打造集文博、文创、文旅于一体的浙东运河文化园。据了解，绍兴古运河是中国大运河的一部分，其中的山阴故水道是中国最早的人工运河之一。近年来，越城区以“污水零直排区”创建等为抓手，积极落实河湖长制，通过多种方式将水利环境效益和文化价值传递给公众。目前，绍兴正在筹建浙东运河文化园（浙东运河博物馆），布置运河博物馆主馆等，总建筑面积约12.4万平方米。版式设计：张芳曼责任编辑：李墨轩', 'cate': '财经', 'url': 'https://finance.sina.com.cn/china/gncj/2021-12-09/doc-ikyamrmy7746224.shtml'}
    ```
- 动态信息，存在db_num=2中（可以在命令行中使用select 2跳转到对应的db）， 存储的形式是string(也就是存的时候用set, 取的时候用get), 具体格式：dynamic_news_detail:fc546951-bc4a-4738-8d87-70fbf8bf8334，其中dynamic_news_detail:表示的是标识符前缀，fc546951-bc4a-4738-8d87-70fbf8bf8334表示的是news_id
    ```shell
        命令行中输入：get dynamic_news_detail:fc546951-bc4a-4738-8d87-70fbf8bf8334 
        显示信息：
        {'likes': 0, 'collections': 0, 'read_num': 1}
    ```


**用户曝光信息**

redis中存储了用户已经曝光的news_id，存在了db_num=3中（可以在命令行中使用select 3跳转到对应的db），存储的形式是set（集合有去重功能），key的具体格式为：user_exposure:4566645517672517633，前面的user_exposure:表示的是标识符前缀，后面的4566645517672517633使用户的id
```shell
    命令行中输入 smembers user_exposure:4566645517672517633
    显示信息:
    ee6c87da-d0ff-4055-8048-53fa58654296:1639361332980
    ffb3946a-5c04-4f45-86ac-d8a0d5beaaa5:1639361324826
    f2962ae9-ef94-44f1-8c5d-4e384cdc3b88:1639361332980
    ff5879a0-3c92-4096-bc77-741d10fcd1b9:1639361332980
    ff1747fd-5a1b-4335-af1a-b638bca142ad:1639361332980
    6c0d09cb-2ca2-46be-a11c-00c27b2519d2:1639361324826
    f0afee36-370e-4ade-b66d-4c4d7b13a12d:1639361324826
    397f5e97-d55e-4334-a5de-8f4b31d2b591:1639361339149
    390553bd-0d91-4c55-9040-ea20e524bf11:1639361332980
    ...
    其中冒号前面表示的是当前用户(userid=4566645517672517633)曝光的新闻id(例如第一条数据，ee6c87da-d0ff-4055-8048-53fa58654296)，冒号后面表示的是给该用户曝光这个新闻的时间戳。
```

**倒排索引表**


- 热门页倒排索引表模板（因为所有用户的热门页的倒排索引都是相同的新闻类别）
    - 模板key：hot_list_news_cate:2511，其中hot_list_news_cate:表示前缀，2511表示新闻类别，对于模板中的倒排表都是根据新闻的热度进行排序的，存储的形式是一个有序的列表，
      - 查看key中对应的value, 命令行中输入：ZREVRANGE hot_list_news_cate:2512 0 5 withscores
        ```shell
            体育_fbf47c67-58e7-4ebb-a216-3b4e383d154c
            2.6880716819115182
            体育_fad1977c-5597-4f82-bd5d-4cb3cf73542f
            1.6047250236808379
            体育_dc15897f-fcd1-4986-9b13-9b4159a14331
            0.84995589542132166
            体育_e4d1fecb-73bc-465b-b328-b8078285c5d3
            0.8021365550834475
            体育_e91491c7-d39b-47d5-9959-0435b5b79c5f
            0.78938472455284958
            体育_dee03f49-4d0f-4f81-98b9-8d01438a9350
        ``` 
    - 用户key: user_id_hot_list:4566645517672517633:2510, 其中user_id_hot_list:表示的是前缀，4566645517672517633表示的是用户id, 2510表示当前用户的新闻类别
      - 查看key中对应的value, 命令行中输入：ZREVRANGE user_id_hot_list:4566645517672517633:2510 0 5 withscores
        ```shell
            国内_ff841614-e609-45f9-ad19-0a785c7d1671
            0
            国内_fe912fdf-8c56-4968-b6be-68ebd3497326
            0
            国内_fd6586ed-36cf-4651-a097-3e99f87c4e94
            0
            国内_fd56439a-e9f1-4ec0-81f1-5945e89f3035
            0
            国内_fca1f7c2-9b1b-463a-8473-72f95a6c38e5
            0
            国内_fc7b7372-ff2e-4652-886f-a3b545680654
            0
        ```
- 推荐页（冷启动）倒排索引表模板（因为冷启动策略把用户分成了四群人，所以需要先得到这四群人的模板）
  - 模板key: cold_start_group:1:2515，其中cold_start_group:表示的是标识符前缀，1表示的是用户分组id, 2515表示的是当前用户分组中的新闻类别id
  - 查看key中对应的value, 命令行中输入：ZREVRANGE cold_start_group:1:2515 0 5 withscores
    ```shell
        科技_fb4059a7-0ca9-4408-bbb4-5586d6730ffc
        0.83023968686638971
        科技_fecfb59e-bf43-4c9b-9e17-5848dc4e3eac
        0.82817058013476941
        科技_d3144958-dd68-449e-9d8a-0860d91a2e55
        0.82669405303344412
        科技_b6bdaa08-c738-4404-aba3-5253468eaa03
        0.81550978800521023
        科技_fe720684-ddfe-445c-8711-701bc007a59e
        0.81101884242079114
        科技_d2f55b5a-862f-4388-93f7-ee8eec53f3f3
        0.80569707406382796
    ```
  - 用户key: cold_start_user:4567404047253901313:2510, 其中cold_start_user:表示的是标识符前缀，4567404047253901313表示的是用户id, 2510表示的是新闻的id
  - 查看key中对应的value, 命令行中输入：ZREVRANGE cold_start_user:4567404047253901313:2510 0 5 withscores
    ```shell
        国内_6c0d09cb-2ca2-46be-a11c-00c27b2519d2
        25.288702038209784
        国内_390553bd-0d91-4c55-9040-ea20e524bf11
        18.166208189511678
        国内_58401c12-ce39-42f4-aa36-6902e5446978
        17.68821319851174
        国内_397f5e97-d55e-4334-a5de-8f4b31d2b591
        17.550739229505592
        国内_0af880a3-d0f1-4a80-9ce5-815309ffb9e7
        17.046616325578892
        国内_4e342f91-a761-4d65-b498-c47b0c4eba34
        14.048019077556772
    ```


### 注意点

这里说明redis中key的一些定义模式其实是不唯一的，只需要我们存和取的时候，key能够对应上就行。上述描述中提到无论是模板key还是用户的key都涉及到了新闻类别，其实这里是为了后续获取用户推荐列表的时候使用轮询的方式打散不同类别的新闻。