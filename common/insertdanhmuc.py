import re, unicodedata
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def _slugify(text: str) -> str:
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^a-zA-Z0-9]+', '-', text).strip('-').lower()
    return re.sub(r'-{2,}', '-', text) or "danh-muc"

def insert_danhmuc(ten: str, mo_ta: str | None = None,
                   parent_id: int | None = None, sap_xep: int = 0,
                   hien_thi: int = 1) -> int:
    if not ten or not ten.strip():
        raise ValueError("ten danh muc khong duoc rong")

    conn = None
    try:
        conn = connect_mysql()  # in "Kết nối MySQL thành công!" và trả về connection
        slug_base = _slugify(ten)
        slug = slug_base

        with conn.cursor() as cur:
            # đảm bảo slug duy nhất
            n = 2
            while True:
                cur.execute("SELECT id FROM danhmuc WHERE slug=%s LIMIT 1", (slug,))
                if cur.fetchone() is None:
                    break
                slug = f"{slug_base}-{n}"
                n += 1

            cur.execute("""
                INSERT INTO danhmuc (ten_dm, slug, mo_ta, parent_id, sap_xep, hien_thi)
                VALUES (%s, %s, %s, %s, %s, %s)
            """, (ten.strip(), slug, mo_ta, parent_id, sap_xep, hien_thi))
            conn.commit()
            return cur.lastrowid
    except Error as e:
        raise RuntimeError(f"Lỗi insert danhmuc: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
