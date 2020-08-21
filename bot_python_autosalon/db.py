import sqlite3

class SQLighter:

    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()
    
    def insert_client(self, user):
        with self.connection:
            self.cursor.execute('INSERT INTO Client(user_ip) VALUES(?)  ', (str(user),))
            self.connection.commit()
    
    #admin
    def select_all_clients(self):
        with self.connection:
            temp = self.cursor.execute('SELECT * FROM Client').fetchall()
            return temp
    
    def select_all_orders(self):
        with self.connection:
            temp = self.cursor.execute('SELECT user_ip,title,duration,cost FROM Orders,Client,Service WHERE Orders.client_id=Client.id AND Orders.service_id=Service.id').fetchall()
            return temp
            
    def insert_service(self,title,duration,cost):
        with self.connection:
            self.cursor.execute('INSERT INTO Service(title,duration,cost) VALUES(?,?,?)  ', (str(title),float(duration),float(cost),))
            self.connection.commit()
    
    #user     
    def select_all_services(self):
        with self.connection:
            temp = self.cursor.execute('SELECT * FROM Service').fetchall()
            return temp
    
    def select_user_orders(self, user):
        with self.connection:
            user_id = self.cursor.execute('SELECT id FROM Client WHERE user_ip=?',(str(user),)).fetchone()[0]
            temp = self.cursor.execute('SELECT title,duration,cost FROM Orders,Service WHERE client_id = ? AND Orders.service_id=Service.id', (int(user_id),)).fetchall()
            return temp

    def insert_order(self, user, service):
        with self.connection:
            user_id = self.cursor.execute('SELECT id FROM Client WHERE user_ip=?',(str(user),)).fetchone()[0]
            self.cursor.execute('INSERT INTO Orders(client_id,service_id) VALUES(?,?) ', (int(user_id),int(service),))
            self.connection.commit()
    
    def close(self):
        """ Закрываем текущее соединение с БД """
        self.connection.close()