import tkinter as tk
from tkinter import messagebox, Toplevel, ttk
from database import Database

class Application(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Supermarket Management")
        self.geometry("800x400")
        self.db = None
        self.create_login_ui()

    def create_login_ui(self):
        self.login_frame = tk.Frame(self)
        self.login_frame.pack(pady=20)

        tk.Label(self.login_frame, text="Username:").grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        tk.Label(self.login_frame, text="Password:").grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        # tk.Label(self.login_frame, text="Database:").grid(row=2, column=0)
        # self.dbname_entry = tk.Entry(self.login_frame)
        # self.dbname_entry.grid(row=2, column=1)

        tk.Button(self.login_frame, text="Connect", command=self.connect_to_db).grid(row=3, columnspan=2, pady=10)

    def connect_to_db(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        # dbname = self.dbname_entry.get()
        
        self.db = Database(host="localhost", dbname="postgres", user=username, password=password)
        
        if self.db.connect():
            messagebox.showinfo("Success", "Kết nối dữ liệu thành công")
            self.login_frame.pack_forget()
            self.create_main_ui()
            self.select_all()
        else:
            messagebox.showerror("Error", "Có lỗi khi kết nối dữ liệu!")

    def create_main_ui(self):
        self.main_frame = tk.Frame(self)
        self.main_frame.pack(pady=20)

        button_frame = tk.Frame(self.main_frame)
        button_frame.pack(fill="x", pady=5)
        

        tk.Button(button_frame, text="Thêm sản phẩm mới", command=self.open_insert_modal).pack(side="right", padx=5)
        tk.Button(button_frame, text="Làm mới dữ liệu", command=self.select_all).pack(side="right", padx=5)

        self.product_tree = ttk.Treeview(self.main_frame, columns=("ID", "Name", "Price", "Quantity", "Action"), show="headings")
        self.product_tree.heading("ID", text="ID")
        self.product_tree.heading("Name", text="Sản phẩm")
        self.product_tree.heading("Price", text="Giá")
        self.product_tree.heading("Quantity", text="Số lượng")
        self.product_tree.heading("Action", text="Hành động")

        self.product_tree.column("ID", width=50)
        self.product_tree.column("Name", width=200)
        self.product_tree.column("Price", width=100)
        self.product_tree.column("Quantity", width=100)
        self.product_tree.column("Action", width=200)

        self.product_tree.pack()

        

    def open_insert_modal(self):
        
        modal = Toplevel(self)
        modal.title("Thêm sản phẩm")

        tk.Label(modal, text="Tên:").grid(row=0, column=0)
        entry_name = tk.Entry(modal)
        entry_name.grid(row=0, column=1)

        tk.Label(modal, text="Giá:").grid(row=1, column=0)
        entry_price = tk.Entry(modal)
        entry_price.grid(row=1, column=1)

        tk.Label(modal, text="Số lượng:").grid(row=2, column=0)
        entry_quantity = tk.Entry(modal)
        entry_quantity.grid(row=2, column=1)

        tk.Button(modal, text="Thêm sản phẩm", command=lambda: self.insert_product(modal, entry_name, entry_price, entry_quantity)).grid(row=3, columnspan=2, pady=10)

    def insert_product(self, modal, entry_name, entry_price, entry_quantity):
        name = entry_name.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        if not name:
            messagebox.showerror("Input Error", "Tên không được bỏ trống.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Giá và số lượng phải là số.")
            return

        self.db.insert(name, price, quantity)
        self.select_all()
        modal.destroy()

    def select_all(self):
        products = self.db.select_all()
        self.update_product_list(products)

    def open_update_modal(self, product_id, current_name, current_price, current_quantity):
        modal = Toplevel(self)
        modal.title("Cập nhật")

        tk.Label(modal, text="Tên:").grid(row=0, column=0)
        entry_name = tk.Entry(modal)
        entry_name.insert(0, current_name)
        entry_name.grid(row=0, column=1)

        tk.Label(modal, text="Giá:").grid(row=1, column=0)
        entry_price = tk.Entry(modal)
        entry_price.insert(0, current_price)
        entry_price.grid(row=1, column=1)

        tk.Label(modal, text="Số lượng:").grid(row=2, column=0)
        entry_quantity = tk.Entry(modal)
        entry_quantity.insert(0, current_quantity)
        entry_quantity.grid(row=2, column=1)

        tk.Button(modal, text="Cập nhật", command=lambda: self.update_product(modal, product_id, entry_name, entry_price, entry_quantity)).grid(row=3, columnspan=2, pady=10)

    def update_product(self, modal, product_id, entry_name, entry_price, entry_quantity):
        name = entry_name.get()
        price = entry_price.get()
        quantity = entry_quantity.get()

        if not name:
            messagebox.showerror("Input Error", "Tên không được bỏ trống.")
            return

        try:
            price = float(price)
            quantity = int(quantity)
        except ValueError:
            messagebox.showerror("Input Error", "Giá và số lương phải là số.")
            return

        self.db.update(product_id, name, price, quantity)
        self.select_all()
        modal.destroy()

    def confirm_delete(self, product_id):
        
        confirm = messagebox.askyesno("Xác nhận xóa?", "Bạn có chắc muốn xóa sản phẩm này??")
        if confirm:
            self.db.delete(product_id)
            self.select_all()

    def update_product_list(self, products):
       
        for row in self.product_tree.get_children():
            self.product_tree.delete(row)

       
        for product in products:
            product_id, name, price, quantity = product
            self.product_tree.insert("", tk.END, values=(product_id, name, price, quantity))

            
            self.product_tree.bind("<Double-1>", self.on_row_click)

    def on_row_click(self, event):
        selected_item = self.product_tree.selection()[0]
        values = self.product_tree.item(selected_item, "values")
        product_id = values[0]
        name = values[1]
        price = values[2]
        quantity = values[3]

       
        popup = Toplevel(self)
        popup.title(f"Actions for {name}")

        tk.Label(popup, text=f"Sản phẩm: {name}").pack()
        tk.Label(popup, text=f"Giá: {price}").pack()
        tk.Label(popup, text=f"Số lượng: {quantity}").pack()

        tk.Button(popup, text="Cập nhật", command=lambda: self.open_update_modal(product_id, name, price, quantity)).pack(pady=5)
        tk.Button(popup, text="Xóa", command=lambda: self.confirm_delete(product_id)).pack(pady=5)
