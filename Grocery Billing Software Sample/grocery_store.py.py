import pandas as pd   
from tkinter.constants import RIGHT
import tkinter as tk
from tkinter import ttk,PhotoImage

prod_xl = pd.read_excel("C:/Ashiq/user/OneDrive/Desktop/assignment/products.xlsx")
products = {}
for i in range(len(prod_xl)):
    products[prod_xl.iloc[i][0]] = {'Item': prod_xl.iloc[i][1], 'Q1': prod_xl.iloc[i]
                                    [2], 'Q2': prod_xl.iloc[i][3], 'Q3': prod_xl.iloc[i][4]}

cust_xl = pd.read_excel("C:/Ashiq/user/OneDrive/Desktop/assignment/customers.xlsx")
customers = {}
for i in range(len(cust_xl)):
    customers[cust_xl.iloc[i][0]] = {
        'Name': cust_xl.iloc[i][1], 'Phone': cust_xl.iloc[i][2]}

root = tk.Tk()
root.title("Grocery Store")

bg = PhotoImage(file= "C:/Ashiq/user/OneDrive/Desktop/assignment/bg.png")
label1 = tk.Label( root, image = bg)
label1.place(x = 0, y = 0)

W = 600
H = 650
ws = root.winfo_screenwidth()
hs = root.winfo_screenheight()
x = (ws/2) - (W/2)
y = (hs/2) - (H/2)
root.geometry('%dx%d+%d+%d' % (W, H, x, y))
root.resizable(False, False)

title = tk.Label(root, text="Grocery Store", font=("Times New Roman", 20),padx=20,bg='grey')
title.grid(row=0, column=1, columnspan=1, pady=10)

user_id = tk.StringVar()
user_id.set("Select User ID")
user_id_dropdown = tk.OptionMenu(root, user_id, *list(list(customers.keys())+['Not An User']))
user_id_dropdown.grid(row=1, column=0, padx=10, pady=10)

user_id_dropdown.bind("<Button-1>", lambda event: welcome(user_id.get()))
welcome_user = tk.Label(root, text="")
welcome_user.grid(row=1, column=1)

product_name = tk.StringVar(root)
product_name.set("Select the Products")
item_list = []
for i in products:
    item_list.append(products[i]['Item'])
product_dropdown = tk.OptionMenu(root, product_name, *item_list)
product_dropdown.config(width=20)
product_dropdown.grid(row=2, column=0, padx=10, pady=10)

quality_var = tk.IntVar()
quality_var.set(1)
quality_var_1 = tk.Radiobutton(root, text="Quality 1", variable=quality_var, value=1,bg="grey")
quality_var_1.grid(row=3, column=0, padx=12, pady=12 ,sticky='W')
quality_var_2 = tk.Radiobutton(root, text="Quality 2", variable=quality_var, value=2,bg="grey")
quality_var_2.grid(row=4, column=0, padx=12, pady=12,sticky='W')
quality_var_3 = tk.Radiobutton(root, text="Quality 3", variable=quality_var, value=3,bg="grey")
quality_var_3.grid(row=5, column=0, padx=12, pady=12,sticky="W")

quantity_var = tk.DoubleVar()
quantity_var.set(0.0)
quantity_spinbox = tk.Spinbox(root, from_=0.0, to=100.0, increment=0.50, width=5, textvariable=quantity_var,bg="grey")
quantity_spinbox.grid(row=2, column=1, padx=100, pady=10)
quantity_text = tk.Label(root, text="KG",bg="grey")
quantity_text.place(x=370, y=123)


def submit_order(productname, quality, quantity,user):
    global order_tree
    global order_count
    global total_order
    global total_quantity
    global total_price    

    if quantity != 0.0 and user=='Not An User':
        for i in products:
            if quality == 1:
                if products[i]['Item'] == productname:
                    price = products[i]['Q1']
            elif quality == 2:
                if products[i]['Item'] == productname:
                    price = products[i]['Q2']
            elif quality == 3:
                if products[i]['Item'] == productname:
                    price = products[i]['Q3']

        order_tree.insert("", "end", text=order_count, values=(productname, quantity, quality, price, price*quantity))
        order_count += 1
        product_name.set("Select Product")
        quantity_var.set(0.0)
        quality_var.set(1)
    
        total_order.config(text=str(order_count-1))
        
        quantity_list = []
        for i in range(len(order_tree.get_children())):
            quantity_list.append(float(order_tree.item(order_tree.get_children()[i])['values'][1]))
        total_quantity.config(text=str(sum(quantity_list)))
        
        price_list = []
        for i in range(len(order_tree.get_children())):
            price_list.append(float(order_tree.item(order_tree.get_children()[i])['values'][4]))
        total_price.config(text="₹"+str(sum(price_list)))
    
    elif quantity != 0.0 and user!='Not An User':
        for i in products:
            if quality == 1:
                if products[i]['Item'] == productname:
                    price = products[i]['Q1']
            elif quality == 2:
                if products[i]['Item'] == productname:
                    price = products[i]['Q2']
            elif quality == 3:
                if products[i]['Item'] == productname:
                    price = products[i]['Q3']

        order_tree.insert("", "end", text=order_count, values=(productname, quantity, quality, price,((price*quantity)-(0.012*(price*quantity)))))
        order_count += 1
        product_name.set("Select the Product")
        quantity_var.set(0.0)
        quality_var.set(1)
    
        total_order.config(text=str(order_count-1))
        
        quantity_list = []
        for i in range(len(order_tree.get_children())):
            quantity_list.append(float(order_tree.item(order_tree.get_children()[i])['values'][1]))
        total_quantity.config(text=str(sum(quantity_list)))
        
        price_list = []
        for i in range(len(order_tree.get_children())):
            price_list.append(float(order_tree.item(order_tree.get_children()[i])['values'][4]))
        total_price.config(text="₹"+str(sum(price_list)))


submit_button = tk.Button(root, text="ADD",bg="red", command=lambda: submit_order(product_name.get(), quality_var.get(), quantity_var.get(),user_id.get()), relief=tk.RAISED)
submit_button.grid(row=5, column=1, columnspan=2, pady=10)

finish_button = tk.Button(root, text="EXIT", relief=tk.RAISED,bg="red",command=root.destroy)
finish_button.place(x=430, y=261)

order_tree = ttk.Treeview(root, columns=("Product", "Quantity (kg)", "Quality", "Rate", "Price"), height=7)
order_count = 1
order_tree.heading("#0", text="Order")
order_tree.heading("#1", text="Product")
order_tree.heading("#2", text="Quantity in kg")
order_tree.heading("#3", text="Quality (1,2,3)")
order_tree.heading("#4", text="Rate")
order_tree.heading("#5", text="Price in ₹")
order_tree.column("#0", width=50)
order_tree.column("#1", width=165)
order_tree.column("#2", width=120)
order_tree.column("#3", width=100)
order_tree.column("#4", width=80)
order_tree.column("#5", width=80)
order_tree.grid(row=6, column=0, columnspan=20, pady=10)

tk.Label(root, text="Total Products", font=("Times New Roman", 15),bg="white").place(x=0, y=470)
total_order = tk.Label(root, text="0", font=("Arial", 15),bg="grey")
total_order.place(x=30, y=515)

tk.Label(root, text="Total Quantity (kg)", font=("Arial", 15),bg="white").place(x=200, y=470)
total_quantity = tk.Label(root, text="0.0 Kg", font=("Arial", 15),bg="grey")
total_quantity.place(x=230, y=515)

tk.Label(root, text="Total Amount", font=("Times new Roman", 15),bg="white").place(x=490, y=470)
total_price = tk.Label(root, text="₹0.00", font=("Arial", 15),bg="grey")
total_price.place(x=500, y=515)

root.mainloop()
