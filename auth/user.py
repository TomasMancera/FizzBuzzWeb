import jwt
from data_storage.db_storage import DBStorage
from werkzeug.security import generate_password_hash, check_password_hash


class User:
    def SignUp(self, username, password):
        conn = DBStorage.get_db_connection()
        cursor = conn.cursor()
        
        try:
            # verify if user already exist
            cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
            user = cursor.fetchone()
            
            if user:
                return True 
            else:
            
                # generate password hash
                hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

                # Insert the new user to the DBD
                query = "INSERT INTO users (username, password) VALUES (?, ?)"
                cursor.execute(query, (username, hashed_password))
                
                conn.commit()

        except Exception as e:
            print(f"An error occurred: {e}")

        finally:
            conn.close()

    def login(self, username, password):
        conn = DBStorage.get_db_connection()
        cursor = conn.cursor()

        try:
             # verify if user already exist and get the hashed password
            query_password = cursor.execute("SELECT password FROM users WHERE username = ?", (username,)).fetchone()
            conn.close()
            
            if query_password is None:
                return False
            
            valid_password = query_password[0]
            
            # Verify hashed password
            if check_password_hash(valid_password, password):
                return True
            else:
                return False

        except Exception as e:
            print(f"Account could not be reached or does not exist: {e}")
            return False
    
    def is_admin(self, username):
        conn = DBStorage.get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT role FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        conn.close()
        if user and user[0] == 'admin':
            return True
        return False
    
    def add_admin(self):
        data = self.root_data("root.txt")
        if data is None:
            print("Failed to read root data")
            return

        username = data[0]
        password = data[1]
        hashed_password = generate_password_hash(password, method="pbkdf2:sha256")

        conn = DBStorage.get_db_connection()
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", 
                           (username, hashed_password, 'admin'))
            conn.commit()
            print("Admin user added successfully")
        except Exception as e:
            print(f"An error occurred: {e}")
        finally:
            conn.close()
    
    @staticmethod
    def root_data(filename):
        try:
            with open(filename, encoding="utf-8") as f:
                data = f.readlines()
                data = [line.strip() for line in data]
                if len(data) != 2:
                    raise ValueError("File should contain exactly two lines: username and password")
                return data
        except FileNotFoundError:
            print(f"Error: {filename} not found")
            return None
        except ValueError as e:
            print(f"Error: {e}")
            return None
         


    

