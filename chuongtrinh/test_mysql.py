from ketnoidb.ketnoi_mysql import connect_mysql  # dùng hàm connect bạn đã có

def _ask(label: str, default: str | None = None) -> str:
    prompt = f"{label}" + (f" [{default}]" if default is not None else "") + ": "
    s = input(prompt).strip()
    return s if s else (default or "")

if __name__ == "__main__":
    while True:
        host = _ask("Host", "127.0.0.1")
        port_in = _ask("Port", "3306")
        try:
            port = int(port_in)
        except ValueError:
            port = 3306
        user = _ask("User", "root")
        password = _ask("Password (để trống nếu không có)", "")
        database = _ask("Database", "qlthuocankhang")

        conn = None
        try:
            conn = connect_mysql(host=host, port=port, user=user, password=password, database=database)
            print("✅ Kết nối MySQL thành công!")
            with conn.cursor() as cur:
                cur.execute("SELECT DATABASE(), VERSION()")
                db, ver = cur.fetchone()
                print(f"CSDL: {db}")
                print(f"Phiên bản: {ver}")
        except Exception as e:
            print(f"❌ Không kết nối được MySQL: {e}")
        finally:
            if conn and getattr(conn, "is_connected", lambda: False)():
                conn.close()

        con = input("TIẾP TỤC y, THOÁT THÌ NHẤN KÝ TỰ BẤT KỲ: ").strip().lower()
        if con != "y":
            break
