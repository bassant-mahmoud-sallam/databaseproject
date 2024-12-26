import tkinter as tk
from tkinter import ttk, messagebox
import pyodbc

# connect to database(1)
def connect_db():
    try:
        conn = pyodbc.connect(
            driver='{ODBC Driver 17 for SQL Server}',
            server='DESKTOP-M9PK723',  
            database='E_commerce',   
            trusted_connection='yes'
        )
        return conn
    except pyodbc.Error as e:
        messagebox.showerror("Database Error", f"Error: {e}")
        return None

current_customer_id = None #varible to save the value of customer_id current
current_order_id = None  #varible to save the value of order_id current
selected_products = []  #array to save the tuples each tuple hava (productname , productprice) that selected

#(3)
def open_customer_window():
    def save_customer():
        global current_customer_id
        first_name = entry_first_name.get()
        middle_name = entry_middle_name.get()
        last_name = entry_last_name.get()
        phone = entry_phone.get()
        email = entry_email.get()
        address = entry_address.get()
        zip_code = entry_zip_code.get()

        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                #insert the values in row to customers table in database
                cursor.execute(
                    "INSERT INTO customers (customer_id, first_name, middle_name, last_name, phone, email, address, zip_code) "
                    "OUTPUT INSERTED.customer_id VALUES (NEXT VALUE FOR customer_id_seq, ?, ?, ?, ?, ?, ?, ?)",
                    (first_name, middle_name, last_name, phone, email, address, zip_code)
                )
                current_customer_id = cursor.fetchone()[0] # return the first row , [0] return the first value in that row = customer_id
                conn.commit()
                messagebox.showinfo("Success", f"Customer added successfully! ID: {current_customer_id}")
                window.destroy()
                open_category_window()
            except pyodbc.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                conn.close()

    window = tk.Toplevel(root)
    window.title("Add Customer")

    tk.Label(window, text="First Name").grid(row=0, column=0)
    entry_first_name = tk.Entry(window)
    entry_first_name.grid(row=0, column=1)

    tk.Label(window, text="Middle Name").grid(row=1, column=0)
    entry_middle_name = tk.Entry(window)
    entry_middle_name.grid(row=1, column=1)

    tk.Label(window, text="Last Name").grid(row=2, column=0)
    entry_last_name = tk.Entry(window)
    entry_last_name.grid(row=2, column=1)

    tk.Label(window, text="Phone").grid(row=3, column=0)
    entry_phone = tk.Entry(window)
    entry_phone.grid(row=3, column=1)

    tk.Label(window, text="Email").grid(row=4, column=0)
    entry_email = tk.Entry(window)
    entry_email.grid(row=4, column=1)

    tk.Label(window, text="Address").grid(row=5, column=0)
    entry_address = tk.Entry(window)
    entry_address.grid(row=5, column=1)

    tk.Label(window, text="Zip Code").grid(row=6, column=0)
    entry_zip_code = tk.Entry(window)
    entry_zip_code.grid(row=6, column=1)

    tk.Button(window, text="Save Customer", command=save_customer).grid(row=7, column=1)

#(4)
def open_category_window():
    def load_categories(): #insert the values in categories table from database to category_list in gui
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute("SELECT category_name FROM categories")
                categories = [row[0] for row in cursor.fetchall()] # categories = list of values of categories name 
                for category in categories:
                    category_list.insert(tk.END, category)
            except pyodbc.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                conn.close()

    def select_category():
        selected_category = category_list.get(category_list.curselection()) #category_list.curselection() = index of category name select , get(index) = name of category select 
        open_product_window(selected_category) #selected_category = category_name is selected

    window = tk.Toplevel(root)
    window.title("Select Category")

    tk.Label(window, text="Categories").pack()
    category_list = tk.Listbox(window)
    category_list.pack()

    tk.Button(window, text="Select Category", command=select_category).pack()
    tk.Button(window, text="Finalize Order", command=finalize_order).pack()

    load_categories()

#(5)
def open_product_window(selected_category):
    def load_products(): #load the (product_name and product_price) (include to category name that select(selected_category)) from products table in database to product_list
        conn = connect_db()
        if conn:
            cursor = conn.cursor()
            try:
                cursor.execute(
                    "SELECT product_name, product_price FROM products WHERE category_id = (SELECT category_id FROM categories WHERE category_name = ?)",
                    (selected_category,)
                )
                for row in cursor.fetchall():
                    product_list.insert(tk.END, f"{row[0]} - ${row[1]}")# row[0] = product_name , row[1] = product_price
            except pyodbc.Error as e:
                messagebox.showerror("Error", f"Error: {e}")
            finally:
                conn.close()

    def add_product():
        selected_product = product_list.get(product_list.curselection())
        ask_quantity(selected_product) # selected_product = product_name - $product_price that select

    window = tk.Toplevel(root)
    window.title(f"Products in {selected_category}")

    tk.Label(window, text="Products").pack()
    product_list = tk.Listbox(window)
    product_list.pack()

    tk.Button(window, text="Add Product", command=add_product).pack()

    load_products()


#(6)   
def ask_quantity(product):# product = product_name - $product_price that select
    def save_quantity():
        try:
            quantity = int(entry_quantity.get()) #int(entry_quantity.get()) = return the value in entry_quantity convert to intager
            if quantity <= 0:
                raise ValueError("Quantity must be positive")
            selected_products.append((product, quantity)) #append to array the tuple=(product_name - $product_price that select , quantity)
            messagebox.showinfo("Added", f"{product} with quantity {quantity} added to order!")
            window.destroy()  
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid positive number for quantity.")

    window = tk.Toplevel(root)
    window.title("Enter Quantity")

    tk.Label(window, text="Quantity:").pack()
    entry_quantity = tk.Entry(window)
    entry_quantity.pack()

    tk.Button(window, text="Save", command=save_quantity).pack()


#(7)
def finalize_order():
    global current_order_id
    if not selected_products:
        messagebox.showerror("Error", "No products selected!")
        return

    conn = connect_db()
    if conn:
        cursor = conn.cursor()
        try:
            #insert the order to orders table in database
            cursor.execute(
                "INSERT INTO orders (order_id, order_date, total_amount, order_shipping_status, customer_id) "
                "OUTPUT INSERTED.order_id VALUES (NEXT VALUE FOR order_id_seq, GETDATE(), 0, 'Pending', ?)",
                (current_customer_id,)
            )
            current_order_id = cursor.fetchone()[0] #the value of order_id

            # insert the values to order_product_details table in database   
            total_amount = 0
            for product, quantity in selected_products: #product=product_name - $product_price that select , quantity= number of quantity of product select
                product_name, product_price = product.split(" - $") #product_name = product_name , product_price = product_price
                product_price = float(product_price) # convert product_price to float number
                cursor.execute(
                    "SELECT product_id FROM products WHERE product_name = ?", #select product_id to insert in order_product_details table
                    (product_name,)
                )
                product_id = cursor.fetchone()[0] # product_id = product_id for product_name select
                total_price = product_price * quantity #total_price to insert in order_product_details table = (product_price for product *quantity (الكميه منها))
                total_amount += total_price # total_amount to insert in orders table
                cursor.execute(
                    "INSERT INTO order_product_details (quantity, total_price, order_id, product_id) "
                    "VALUES (?, ?, ?, ?)",
                    (quantity, total_price, current_order_id, product_id)
                )

            #updute the value of total_amount in orders table
            cursor.execute(
                "UPDATE orders SET total_amount = ? WHERE order_id = ?",
                (total_amount, current_order_id)
            )

            conn.commit()
            messagebox.showinfo("Success", "Order finalized successfully!")
            selected_products.clear()

             
            for window in root.winfo_children():
                if isinstance(window, tk.Toplevel):    
                    window.destroy()

        except pyodbc.Error as e:
            messagebox.showerror("Error", f"Error: {e}")
        finally:
            conn.close()


# main window(2)
root = tk.Tk()
root.title("E-commerce System")

tk.Button(root, text="Add Customer", command=open_customer_window).pack()

root.mainloop()
