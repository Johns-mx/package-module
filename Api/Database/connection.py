from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseManagement:
    def __init__(self, connection_url):
        self.connection_url = connection_url
        self.engine = None
    
    def connect(self):
        try:
            if not self.engine:
                self.engine = create_engine(self.connection_url, pool_recycle=3600, echo=True)
        except Exception as e:
            print(f"Error al conectar a la base de datos: {e}")
    
    def get_session(self):
        try:
            Session = sessionmaker(bind=self.engine)
            return Session()
        except Exception as e:
            print(f"Error al obtener la sesión de la base de datos: {e}")
            return None
    
    def close_session(self, session):
        try:
            if session:
                session.close()
        except Exception as e:
            print(f"Error al cerrar la sesión de la base de datos: {e}")
    
    def disconnect(self):
        try:
            if self.engine:
                self.engine.dispose()
                self.engine = None
        except Exception as e:
            print(f"Error al desconectar de la base de datos: {e}")
