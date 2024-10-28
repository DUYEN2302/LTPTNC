import psycopg2

class Database:
    def __init__(self, host, dbname, user, password):
        self.host = host
        self.dbname = dbname
        self.user = user
        self.password = password
        self.conn = None

    def connect(self):
        try:
            self.conn = psycopg2.connect(
                host=self.host,
                dbname=self.dbname,
                user=self.user,
                password=self.password
            )
            self.cursor = self.conn.cursor()
        except Exception as e:
            print(f"Error connecting to database: {e}")
            return False
        return True

    def select_all(self):
        try:
            self.cursor.execute("SELECT * FROM products")
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error fetching data: {e}")
            return []

    def search_by_name(self, name):
        try:
            query = "SELECT * FROM products WHERE name LIKE %s"
            self.cursor.execute(query, (f'%{name}%',))
            return self.cursor.fetchall()
        except Exception as e:
            print(f"Error searching data: {e}")
            return []

    def insert(self, name, price, quantity):
        try:
            query = "INSERT INTO products (name, price, quantity) VALUES (%s, %s, %s)"
            self.cursor.execute(query, (name, price, quantity))
            self.conn.commit()
        except Exception as e:
            print(f"Error inserting data: {e}")

    def update(self, product_id, name, price, quantity):
        try:
            query = "UPDATE products SET name=%s, price=%s, quantity=%s WHERE id=%s"
            self.cursor.execute(query, (name, price, quantity, product_id))
            self.conn.commit()
        except Exception as e:
            print(f"Error updating data: {e}")

    def delete(self, product_id):
        try:
            query = "DELETE FROM products WHERE id=%s"
            self.cursor.execute(query, (product_id,))
            self.conn.commit()
        except Exception as e:
            print(f"Error deleting data: {e}")

    def close(self):
        if self.conn:
            self.cursor.close()
            self.conn.close()
