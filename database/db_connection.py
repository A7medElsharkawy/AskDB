from langchain_community.utilities import SQLDatabase
from database.db_init import Databaseinit


class DatabaseConnection(Databaseinit):
    def __init__(self,db_user,db_name,db_password,db_host,db_port,db_type):
        super().__init__(db_type, db_name, db_user, db_password, db_host, db_port)
    
    def create_engine_connection(self):
        db_url = self.get_connection_url()
        return SQLDatabase.from_uri(db_url)
    
    def get_schema(self)->str:
        db = self.create_engine_connection()
        return db.get_table_info()