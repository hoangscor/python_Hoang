# chuongtrinh/test_danh_muc.py
from common.get_danhmuc import get_all_danhmuc, get_danhmuc

# In toàn bộ danh sách
get_all_danhmuc()

# Xem thêm chi tiết theo ID (tùy chọn)
opt = input("Nhập ID để xem chi tiết (Enter để bỏ): ").strip()
if opt.isdigit():
    get_danhmuc(int(opt))
