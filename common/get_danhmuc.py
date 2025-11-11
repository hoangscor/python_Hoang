# common/get_danhmuc.py
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def get_all_danhmuc(print_result: bool = True):
    """
    Trả về list[dict] các danh mục.
    In ra dạng: ID, Tên, Mô tả nếu print_result=True.
    """
    conn = None
    try:
        conn = connect_mysql(echo=True)  # sẽ in: "✅ Kết nối MySQL thành công!"
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT
                    id      AS madm,
                    ten_dm  AS tendm,
                    mo_ta   AS mota,
                    slug
                FROM danhmuc
                ORDER BY id
            """)
            rows = cur.fetchall()

        if print_result:
            print("✅ Danh sách danh mục:")
            for r in rows:
                print(f"ID: {r['madm']}, Tên: {r['tendm']}, Mô tả: {r['mota'] or ''}")
        return rows

    except Error as e:
        print("❌ Lỗi khi lấy danh sách danh mục:", e)
        return []
    finally:
        if conn and conn.is_connected():
            conn.close()

def get_danhmuc(madm: int, print_result: bool = True):
    """
    Lấy chi tiết 1 danh mục theo ID. Trả về dict hoặc None.
    """
    conn = None
    try:
        conn = connect_mysql(echo=False)
        with conn.cursor(dictionary=True) as cur:
            cur.execute("""
                SELECT
                    id        AS madm,
                    ten_dm    AS tendm,
                    mo_ta     AS mota,
                    slug,
                    parent_id,
                    sap_xep,
                    hien_thi,
                    created_at,
                    updated_at
                FROM danhmuc
                WHERE id=%s
            """, (madm,))
            row = cur.fetchone()

        if print_result:
            if row:
                print(f"✅ Chi tiết danh mục ID {madm}: "
                      f"Tên: {row['tendm']}, Mô tả: {row['mota'] or ''}, Slug: {row['slug']}")
            else:
                print("❌ Không tìm thấy danh mục.")
        return row

    except Error as e:
        print("❌ Lỗi khi lấy danh mục:", e)
        return None
    finally:
        if conn and conn.is_connected():
            conn.close()
