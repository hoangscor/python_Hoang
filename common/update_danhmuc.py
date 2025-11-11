# common/update_danhmuc.py
import re, unicodedata
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def _slugify(text: str) -> str:
    txt = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    txt = re.sub(r'[^a-zA-Z0-9]+', '-', txt).strip('-').lower()
    return re.sub(r'-{2,}', '-', txt) or "danh-muc"

def _unique_slug(conn, base: str, exclude_id: int) -> str:
    """Tạo slug duy nhất, bỏ qua bản ghi có id = exclude_id."""
    slug, n = base, 2
    with conn.cursor() as cur:
        while True:
            cur.execute("SELECT id FROM danhmuc WHERE slug=%s AND id<>%s LIMIT 1", (slug, exclude_id))
            if cur.fetchone() is None:
                return slug
            slug = f"{base}-{n}"
            n += 1

def update_danhmuc(madm: str, ten: str | None, mota: str | None) -> None:
    """
    Cập nhật tên và mô tả cho danh mục theo ID.
    - Nếu nhập tên mới => tự cập nhật slug theo tên, đảm bảo duy nhất.
    - Nếu mô tả để trống => set NULL.
    In ra thông báo kết quả.
    """
    try:
        id_dm = int(madm)
    except ValueError:
        print("❌ Mã danh mục phải là số.")
        return

    conn = None
    try:
        conn = connect_mysql(autocommit=False)  # đã in: "✅ Kết nối MySQL thành công!"
        set_cols, params = [], []

        ten = (ten or "").strip()
        mota = (mota or "").strip()

        if ten:
            # cập nhật tên và slug
            slug = _unique_slug(conn, _slugify(ten), exclude_id=id_dm)
            set_cols += ["ten_dm=%s", "slug=%s"]
            params += [ten, slug]

        # cập nhật mô tả (NULL nếu rỗng)
        set_cols.append("mo_ta=%s")
        params.append(mota if mota else None)

        if not set_cols:
            print("❌ Không có dữ liệu để cập nhật.")
            conn.rollback()
            return

        sql = "UPDATE danhmuc SET " + ", ".join(set_cols) + " WHERE id=%s"
        params.append(id_dm)

        with conn.cursor() as cur:
            cur.execute(sql, tuple(params))
            affected = cur.rowcount
        conn.commit()

        if affected == 1:
            print(f"✅ Đã cập nhật danh mục có ID = {id_dm}")
        else:
            print("❌ Không tìm thấy ID cần cập nhật.")
    except Error as e:
        if conn: conn.rollback()
        print(f"❌ Lỗi cập nhật: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()
