
class Databaseinit:
    def __init__(self, db_type,db_name:str, db_user:str, db_password, db_host:int, db_port:int):
        self.db_user = db_user
        self.db_name = db_name
        self.db_password = db_password
        self.db_host = db_host
        self.db_port = db_port
        self.db_type = db_type
    def get_url_formater(self,db_user, db_name, db_password, db_host, db_port, db_type):

        if self.db_type == "postgresql":
            return f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        elif self.db_type == "mysql":
            return f"mysql+pymysql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        
        elif self.db_type == "sqlite":
            return f"sqlite:///{db_name}"  # SQLite only needs a file path
        
        else:
            raise ValueError(f"Unsupported database type: {self.db_type}")

    def get_connection_url(self):
        url =  self.get_url_formater(self.db_user, self.db_name, self.db_password, self.db_host, self.db_port, self.db_type) 

        return url