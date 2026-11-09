# Classe base de onde toda tabela do banco (em app/models/*.py) herda.
# O Alembic usa `Base.metadata` pra descobrir automaticamente quais tabelas existem
# e gerar as migrations (ver migrations/env.py).
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass
