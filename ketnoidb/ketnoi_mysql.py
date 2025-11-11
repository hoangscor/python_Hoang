import mysql.connector
from mysql.connector import Error

def connect_mysql(
    host="127.0.0.1", port=3306,
    user="root", password="",
    database="qlthuocankhang",
    autocommit=True, echo=True
):
    try:
        conn = mysql.connector.connect(
            host=host, port=port, user=user, password=password,
            database=database, autocommit=autocommit, charset="utf8mb4"
        )
        conn.ping(reconnect=True, attempts=1, delay=0)
        if echo:
            print("✅ Kết nối MySQL thành công!")
        return conn                     # QUAN TRỌNG: trả về connection, không trả về chuỗi
    except Error as e:
        raise RuntimeError(f"Lỗi kết nối MySQL: {e}")
