import mysql.connector

class ProductDB:
    def __init__(self, username="root", password="1234"):
        try:
            self.cnx = mysql.connector.connect(user=username, password=password,
                              host='127.0.0.1', database='test',
                              auth_plugin='mysql_native_password')
            self.cursor = self.cnx.cursor()
        except Exception as e:
            raise
    
    def add_product(self, Product):
        name = Product.get_name()
        price = Product.get_price()
        query = f"insert into produto values(NULL, '{name}',{price})"
        self.cursor.execute(query)
        self.cnx.commit()
    
    def remove_product(self, id):
        query = f"delete from produto where idproduto = {id}"
        self.cursor.execute(query)
        self.cnx.commit()
    
    def get_all_products(self):
        query = "select * from produto"
        self.cursor.execute(query)
        return self.cursor
    
    def edit_product(self,id,name,price):     
        query = f"update produto set nome = '{name}', proco = {price} where idproduto = {id}"
        self.cursor.execute(query)
        self.cnx.commit()