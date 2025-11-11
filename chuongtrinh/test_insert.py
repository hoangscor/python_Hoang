from common.insertdanhmuc import insert_danhmuc

while True:
    ten = input("Nhập vào tên danh mục: ").strip()
    if not ten:
        print("Tên danh mục không được rỗng"); continue
    mota = input("Nhập vào mô tả: ").strip() or None

    try:
        new_id = insert_danhmuc(ten, mota)
        print(f"✅ Đã thêm danh mục: {ten} (id={new_id})")
    except Exception as e:
        print(f"❌ Lỗi: {e}")

    con = input("TIẾP TỤC y, THOÁT THÌ NHẤN KÝ TỰ BẤT KỲ: ").strip().lower()
    if con != "y":
        break
