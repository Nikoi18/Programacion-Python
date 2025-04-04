from sqlalchemy import Column, Integer, String, Boolean
import db

class Tarea(db.Base):
    __tablename__ = "tarea"
    __table_args__ = {"sqlite_autoincrement": True}
    id = Column(Integer, primary_key=True)
    contenido = Column(String(200), nullable=False)
    hecha = Column(Boolean)

    def __init__(self, contenido, hecha):
        self.contenido = contenido
        self.hecha = hecha

    def __str__(self):
        return "Tarea {}:{} ({})".format(self.id, self.contenido, self.hecha)