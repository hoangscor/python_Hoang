# giaodien/GiaodienDanhMuc.py
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, messagebox

# Các hàm bạn đã có ở common/*
from common.insertdanhmuc import insert_danhmuc
from common.delete_danhmuc import delete_danhmuc_by_id
from common.update_danhmuc import update_danhmuc as update_dm_func
from common.get_danhmuc import get_all_danhmuc


class DanhMucApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Quản lý Danh mục")
        self.geometry("900x560")
        self._build_ui()
        self._bind_events()
        self.load_data()

    # ---------- UI ----------
    def _build_ui(self):
        frm = ttk.Frame(self, padding=12)
        frm.pack(fill="both", expand=True)

        # Form nhập
        f_form = ttk.LabelFrame(frm, text="Thông tin danh mục", padding=12)
        f_form.pack(fill="x")

        ttk.Label(f_form, text="ID:").grid(row=0, column=0, sticky="w", padx=(0, 8), pady=6)
        self.var_id = tk.StringVar()
        ent_id = ttk.Entry(f_form, textvariable=self.var_id, width=10, state="readonly")
        ent_id.grid(row=0, column=1, sticky="w", pady=6)

        ttk.Label(f_form, text="Tên danh mục:").grid(row=0, column=2, sticky="w", padx=(16, 8))
        self.var_ten = tk.StringVar()
        self.ent_ten = ttk.Entry(f_form, textvariable=self.var_ten, width=40)
        self.ent_ten.grid(row=0, column=3, sticky="we", pady=6)

        ttk.Label(f_form, text="Mô tả:").grid(row=1, column=0, sticky="nw", padx=(0, 8))
        self.txt_mota = tk.Text(f_form, width=70, height=3)
        self.txt_mota.grid(row=1, column=1, columnspan=3, sticky="we")

        f_form.columnconfigure(3, weight=1)

        # Nút thao tác
        f_btn = ttk.Frame(frm)
        f_btn.pack(fill="x", pady=(10, 6))

        self.btn_add = ttk.Button(f_btn, text="➕ Thêm", width=14, command=self.on_add)
        self.btn_edit = ttk.Button(f_btn, text="✏️  Sửa", width=14, command=self.on_update)
        self.btn_del = ttk.Button(f_btn, text="🗑️  Xóa", width=14, command=self.on_delete)
        self.btn_clear = ttk.Button(f_btn, text="🧹 Xóa ô", width=12, command=self.clear_form)
        self.btn_reload = ttk.Button(f_btn, text="🔄 Nạp lại", width=12, command=self.load_data)
        self.btn_quit = ttk.Button(f_btn, text="⏻ Thoát", width=10, command=self.destroy)

        self.btn_add.pack(side="left", padx=4)
        self.btn_edit.pack(side="left", padx=4)
        self.btn_del.pack(side="left", padx=4)
        self.btn_clear.pack(side="left", padx=12)
        self.btn_reload.pack(side="left", padx=4)
        self.btn_quit.pack(side="right")

        # Bảng danh sách
        f_table = ttk.LabelFrame(frm, text="Danh sách", padding=8)
        f_table.pack(fill="both", expand=True)

        columns = ("id", "ten", "mota", "slug")
        self.tree = ttk.Treeview(f_table, columns=columns, show="headings", height=12)
        self.tree.heading("id", text="ID")
        self.tree.heading("ten", text="Tên danh mục")
        self.tree.heading("mota", text="Mô tả")
        self.tree.heading("slug", text="Slug")
        self.tree.column("id", width=60, anchor="center")
        self.tree.column("ten", width=260)
        self.tree.column("mota", width=360)
        self.tree.column("slug", width=160)

        ybar = ttk.Scrollbar(f_table, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=ybar.set)
        self.tree.pack(side="left", fill="both", expand=True)
        ybar.pack(side="right", fill="y")

    def _bind_events(self):
        self.tree.bind("<<TreeviewSelect>>", self.on_select)
        self.ent_ten.bind("<Return>", lambda e: self.on_add())  # Enter để thêm

    # ---------- Helpers ----------
    def _get_mota_text(self) -> str:
        return self.txt_mota.get("1.0", "end-1c").strip()

    def clear_form(self):
        self.var_id.set("")
        self.var_ten.set("")
        self.txt_mota.delete("1.0", "end")
        self.ent_ten.focus_set()

    def load_data(self):
        # lấy toàn bộ danh mục (list[dict])
        rows = get_all_danhmuc(print_result=False)
        # clear bảng
        for iid in self.tree.get_children():
            self.tree.delete(iid)
        # insert
        for r in rows:
            self.tree.insert(
                "", "end",
                iid=str(r["madm"]),
                values=(r["madm"], r["tendm"], r["mota"] or "", r["slug"])
            )

    # ---------- Actions ----------
    def on_select(self, _):
        item = self.tree.selection()
        if not item:
            return
        vals = self.tree.item(item[0], "values")
        self.var_id.set(vals[0])
        self.var_ten.set(vals[1])
        self.txt_mota.delete("1.0", "end")
        self.txt_mota.insert("1.0", vals[2])

    def on_add(self):
        ten = self.var_ten.get().strip()
        mota = self._get_mota_text()
        if not ten:
            messagebox.showwarning("Thiếu dữ liệu", "Nhập tên danh mục.")
            self.ent_ten.focus_set()
            return
        try:
            new_id = insert_danhmuc(ten, mota or None)
            messagebox.showinfo("Thành công", f"Đã thêm danh mục. ID = {new_id}")
            self.clear_form()
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi thêm", str(e))

    def on_update(self):
        id_txt = self.var_id.get().strip()
        if not id_txt:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn 1 danh mục để sửa.")
            return
        ten = self.var_ten.get().strip()
        mota = self._get_mota_text()
        try:
            # Hàm update_danhmuc do bạn đã viết: update_danhmuc(madm, ten, mota)
            update_dm_func(id_txt, ten, mota)
            # Nếu không raise lỗi thì coi như OK
            messagebox.showinfo("Thành công", f"Đã cập nhật ID = {id_txt}")
            self.load_data()
        except Exception as e:
            messagebox.showerror("Lỗi cập nhật", str(e))

    def on_delete(self):
        id_txt = self.var_id.get().strip()
        if not id_txt:
            messagebox.showwarning("Thiếu dữ liệu", "Chọn 1 danh mục để xóa.")
            return
        if not messagebox.askyesno("Xác nhận", f"Bạn chắc chắn xóa ID = {id_txt}?"):
            return
        try:
            deleted = delete_danhmuc_by_id(int(id_txt), transfer_to=None)
            if deleted:
                messagebox.showinfo("Thành công", "Đã xóa.")
                self.clear_form()
                self.load_data()
            else:
                messagebox.showwarning("Không tìm thấy", "ID không tồn tại.")
        except Exception as e:
            messagebox.showerror("Lỗi xóa", str(e))


if __name__ == "__main__":
    DanhMucApp().mainloop()
