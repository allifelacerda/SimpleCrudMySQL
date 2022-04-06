from tkinter import ttk
from tkinter import *
from functools import partial
from tkinter import messagebox
from turtle import title
from Product import Product
from ProductDB import ProductDB

class App():
    def __init__(self, window, prodDB):
        self.build_window(window)
        self.get_products()
    
    def build_edit_window(self, id, name, old_price):
        self.edit_wind = Toplevel()
        self.edit_wind.geometry('250x140')
        self.edit_wind.resizable(0,0)

        # Old Name
        Label(self.edit_wind, text = 'Old Name:').grid(row = 0, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = name), state = 'readonly').grid(row = 0, column = 2)
        # New Name
        Label(self.edit_wind, text = 'New Name:').grid(row = 1, column = 1)
        new_name = Entry(self.edit_wind)
        new_name.grid(row = 1, column = 2)

        # Old Price 
        Label(self.edit_wind, text = 'Old Price:').grid(row = 2, column = 1)
        Entry(self.edit_wind, textvariable = StringVar(self.edit_wind, value = old_price), state = 'readonly').grid(row = 2, column = 2)
        # New Price
        Label(self.edit_wind, text = 'New Price:').grid(row = 3, column = 1)
        new_price= Entry(self.edit_wind)
        new_price.grid(row = 3, column = 2)

        Button(self.edit_wind, text = 'Update', command = lambda: self.edit_records(id, new_name.get(), new_price.get())).grid(row = 4, column = 2, sticky = W)
        self.edit_wind.mainloop()
    
    def build_window(self, window):
        self.wind = window
        self.wind.title('Products Application')        
        
        # Creating a Frame Container 
        frame = LabelFrame(self.wind, text = 'Register new Product')
        frame.grid(row = 0, column = 0, columnspan = 3, pady = 20)
        
        # Name Input
        Label(frame, text = 'Name: ').grid(row = 1, column = 0)
        self.name = Entry(frame)
        self.name.focus()
        self.name.grid(row = 1, column = 1)

        # Price Input
        Label(frame, text = 'Price: ').grid(row = 2, column = 0)
        self.price = Entry(frame)
        self.price.grid(row = 2, column = 1)
        
        # Button Add Product 
        self.save_button = ttk.Button(frame, text = 'Save Product')
        self.save_button["command"] = partial(self.save_product)
        self.save_button.grid(row = 3, columnspan = 2, sticky = W + E)

        # Output Messages 
        self.message = Label(text = '', fg = 'red')
        self.message.grid(row = 3, column = 0, columnspan = 2, sticky = W + E)

        # Table
        columns = ('ID','Name','Price')
        self.tree = ttk.Treeview(root, columns=columns, show='headings')
        self.tree.grid(row=4, column=0, columnspan = 2, sticky='nsew')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Name', text='Name')
        self.tree.heading('Price', text='Price')

         # Buttons
        self.delete_button = ttk.Button(text = 'DELETE')
        self.delete_button["command"] = partial(self.delete_product)
        self.delete_button.grid(row = 5, column = 0, sticky = W + E)
        
        self.edit_button = ttk.Button(text = 'EDIT')
        self.edit_button["command"] = partial(self.edit_product)
        self.edit_button.grid(row = 5, column = 1, sticky = W + E)
    
    def get_products(self):
        #cleaning table
        records = self.tree.get_children()
        for element in records:
            self.tree.delete(element)

        #getting all data
        all = prodDB.get_all_products()
        all_products = []
        for item in all:
            all_products.append(item)
        
        for prod in all_products:
            self.tree.insert('',0, values=prod)
    
    def validation(self, name, price):
        try:            
            if '.' in price:
                price = float(price)
            else:
                price = int(price)
        except:
            return False        
        return len(name) != 0
        
    def save_product(self):
        name = self.name.get()
        price = self.price.get()
        if self.validation(name, price):
            prod = Product(name,price)
            prodDB.add_product(prod)
            self.message['text'] = f'Product {name} added Successfully!'
            self.name.delete(0, 'end')
            self.price.delete(0, 'end')
            del prod            
        else:
            self.message['text'] = 'Error'
        self.get_products()
            
    def delete_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['values'][0]           
        except IndexError as e:
            self.message['text'] = 'Please select a Product'
            return        
        id = self.tree.item(self.tree.selection())['values'][0]
        prodDB.remove_product(id)
        self.get_products()
    
    def edit_product(self):
        self.message['text'] = ''
        try:
           self.tree.item(self.tree.selection())['values'][0]           
        except IndexError as e:
            self.message['text'] = 'Please select a Product'
            return
        id = self.tree.item(self.tree.selection())['values'][0]
        name = self.tree.item(self.tree.selection())['values'][1]
        old_price = self.tree.item(self.tree.selection())['values'][2]
        self.build_edit_window(id, name, old_price)
    
    def edit_records(self, id, new_name, new_price):
        if self.validation(new_name, new_price):              
            prodDB.edit_product(id, new_name, new_price)
            self.get_products()
            self.edit_wind.destroy()
        else:
            messagebox.showinfo(message = "invalid input")        
            
def on_closing():
    if messagebox.askokcancel("Quit", "Do you want to quit?"):
        prodDB.close_connection()
        root.destroy()
        

if __name__ == '__main__':
    prodDB = ProductDB()
    if prodDB:   
        root = Tk()
        root.resizable(0,0)
        app = App(root, prodDB)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.mainloop()
    else:
        print("Error db")
        