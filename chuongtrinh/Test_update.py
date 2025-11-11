# chuongtrinh/Test_update.py
from common.update_danhmuc import update_danhmuc

while True:
    madm = input("Mã danh mục: ")
    ten = input("Nhập vào tên danh mục: ")
    mota = input("Nhập vào mô tả: ")
    update_danhmuc(madm, ten, mota)
    con = input("TIẾP TỤC y, THOÁT THÌ NHẤN KÝ TỰ BẤT KỲ: ").strip().lower()
    if con != "y":
        break
# Thêm dòng này