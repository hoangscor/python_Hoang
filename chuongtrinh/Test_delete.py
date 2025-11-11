from common.delete_danhmuc import delete_danhmuc_by_id

if __name__ == "__main__":
    raw = input("Nhập mã ID danh mục cần xóa: ").strip()
    try:
        id_dm = int(raw)
    except ValueError:
        print("Mã ID phải là số."); raise SystemExit(1)

    # Nếu danh mục có sản phẩm và bạn muốn chuyển sang ID khác, điền ở đây (hoặc để None)
    transfer_to = None  # ví dụ: 1

    try:
        deleted = delete_danhmuc_by_id(id_dm, transfer_to=transfer_to)
        print("Đã xóa." if deleted else "Không tìm thấy ID cần xóa.")
    except Exception as e:
        print(f"Lỗi: {e}")
