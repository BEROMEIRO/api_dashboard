from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import models  # Importa o arquivo de modelos

DATABASE_URL = "sqlite:///./database.db"  # URL do banco de dados SQLite

# Criar o engine de conexão com o banco de dados
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Função para excluir a tabela e criar a nova tabela
def reset_database():
    """
    Essa função vai apagar a tabela atual (se existir) e criar uma nova com a definição do modelo.
    """
    Base.metadata.drop_all(bind=engine)  # Apaga a tabela 'items' (e outras, se houver)
    Base.metadata.create_all(bind=engine)  # Cria novamente a tabela com a nova estrutura
