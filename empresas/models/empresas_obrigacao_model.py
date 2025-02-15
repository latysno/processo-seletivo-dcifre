from enum import unique
from symtable import Class

from sqlalchemy import Column, Integer, String, ForeignKey

from shared.database import Base

class Empresa(Base):

    __tablename__ = "empresa"

    id = Column(Integer, primary_key=True,autoincrement=True)
    nome = Column(String)
    cnpj = Column(String(14), unique=True)
    endereco = Column(String)
    email = Column(String, unique=True)
    telefone = Column(String(11))

class ObrigacaoAcessoria(Base):

    __tablename__ = "obrigacao_acessoria"

    id = Column(Integer, primary_key=True, autoincrement=True)
    nome = Column(String)
    periocidade = Column(String)
    empresa_id = Column(Integer, ForeignKey("empresa.id"))
