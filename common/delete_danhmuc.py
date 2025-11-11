# common/delete_danhmuc.py
from mysql.connector import Error
from ketnoidb.ketnoi_mysql import connect_mysql

def delete_danhmuc(identifier, by: str = "id", transfer_to: int | None = None) -> int:
    """
    Xóa 1 danh mục.
    - identifier: giá trị id (int) hoặc slug (str) tùy tham số 'by'.
    - by: 'id' | 'slug'.
    - transfer_to: id danh mục đích để CHUYỂN sản phẩm sang trước khi xóa.
      Nếu không truyền và danh mục còn sản phẩm -> báo lỗi.
    Trả về số dòng đã xóa (0 hoặc 1).
    """
    conn = None
    try:
        conn = connect_mysql(autocommit=False, echo=False)

        with conn.cursor() as cur:
            # Lấy id danh mục cần xóa
            if by == "id":
                id_dm = int(identifier)
            elif by == "slug":
                cur.execute("SELECT id FROM danhmuc WHERE slug=%s", (identifier,))
                row = cur.fetchone()
                if not row:
                    conn.rollback()
                    return 0
                id_dm = row[0]
            else:
                raise ValueError("by chỉ nhận 'id' hoặc 'slug'")

            # Khóa bản ghi, xác nhận tồn tại
            cur.execute("SELECT id FROM danhmuc WHERE id=%s FOR UPDATE", (id_dm,))
            if not cur.fetchone():
                conn.rollback()
                return 0

            # Xử lý sản phẩm cùng danh mục
            if transfer_to is not None:
                if int(transfer_to) == int(id_dm):
                    raise ValueError("transfer_to không được trùng id cần xóa")
                # kiểm tra danh mục đích tồn tại
                cur.execute("SELECT id FROM danhmuc WHERE id=%s", (transfer_to,))
                if not cur.fetchone():
                    raise ValueError("transfer_to không tồn tại")
                # chuyển sản phẩm sang danh mục đích
                cur.execute(
                    "UPDATE sanpham SET danh_muc_id=%s WHERE danh_muc_id=%s",
                    (transfer_to, id_dm),
                )
            else:
                # nếu không chuyển, kiểm tra còn sản phẩm -> chặn
                cur.execute(
                    "SELECT COUNT(*) FROM sanpham WHERE danh_muc_id=%s", (id_dm,)
                )
                count_sp = cur.fetchone()[0]
                if count_sp > 0:
                    raise RuntimeError(
                        f"Danh mục còn {count_sp} sản phẩm. Hãy chuyển sang danh mục khác (transfer_to) rồi xóa."
                    )

            # Xóa danh mục (child categories sẽ tự SET NULL do FK)
            cur.execute("DELETE FROM danhmuc WHERE id=%s", (id_dm,))
            deleted = cur.rowcount
            conn.commit()
            return deleted

    except Error as e:
        if conn:
            conn.rollback()
        raise RuntimeError(f"Lỗi khi xóa danh mục: {e}")
    finally:
        if conn and conn.is_connected():
            conn.close()


# Tiện ích gọi nhanh
def delete_danhmuc_by_id(id_dm: int, transfer_to: int | None = None) -> int:
    return delete_danhmuc(id_dm, by="id", transfer_to=transfer_to)

def delete_danhmuc_by_slug(slug: str, transfer_to: int | None = None) -> int:
    return delete_danhmuc(slug, by="slug", transfer_to=transfer_to)


if __name__ == "__main__":
    # Chạy trực tiếp để test nhanh: nhập id/slug và id danh mục đích (nếu muốn chuyển sản phẩm)
    ident = input("Nhập id hoặc slug danh mục cần xóa: ").strip()
    mode = "id" if ident.isdigit() else "slug"
    trans = input("Chuyển sản phẩm sang id (Enter nếu không chuyển): ").strip()
    transfer = int(trans) if trans.isdigit() else None
    try:
        n = delete_danhmuc(ident, by=mode, transfer_to=transfer)
        print("Đã xóa." if n else "Không tìm thấy.")
    except Exception as ex:
        print("Lỗi:", ex)
