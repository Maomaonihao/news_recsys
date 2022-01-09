from user_process.user_to_mysql import UserMysqlServer
from user_process.user_protrail import UserProtrail


def process_users():
    """将用户数据存入MySQL
       1.将用户的曝光数据从redis存入MySQL中。
       2.更新用户画像
    """
    user_mysql_server = UserMysqlServer()
    # 用户曝光数据存储到MySQL中
    user_mysql_server.user_exposure_to_mysql()

    # 更新用户画像
    user_protrail = UserProtrail()
    user_protrail.update_user_protrail_from_register_table()


if __name__ == "__main__":
    process_users()
