from sqlalchemy import create_engine, String, ForeignKey, CheckConstraint
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship, sessionmaker

engine = create_engine("sqlite:///biblioteca.db")


class Base(DeclarativeBase):
    pass


class Libro(Base):
    __tablename__ = "libros"
    __table_args__ = (
        CheckConstraint("ejemplares_disponibles >= 0", name="check_ejemplares"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(100), nullable=False)
    autor: Mapped[str] = mapped_column(String(100), nullable=False)
    ejemplares_disponibles: Mapped[int] = mapped_column(default=0, server_default="0")
    prestamos: Mapped[list["Prestamo"]] = relationship(back_populates="libro")


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    correo: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    prestamos: Mapped[list["Prestamo"]] = relationship(back_populates="usuario")


class Prestamo(Base):
    __tablename__ = "prestamos"
    __table_args__ = (
        CheckConstraint("cantidad >= 0", name="check_cantidad"),
        CheckConstraint("estado IN ('activo', 'devuelto')", name="check_estado"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    libro_id: Mapped[int] = mapped_column(ForeignKey("libros.id"), nullable=False)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"), nullable=False)
    fecha: Mapped[str] = mapped_column(String(10), nullable=False)
    cantidad: Mapped[int] = mapped_column(default=0, server_default="0")
    estado: Mapped[str] = mapped_column(String(10), default="activo", server_default="activo")
    libro: Mapped["Libro"] = relationship(back_populates="prestamos")
    usuario: Mapped["Usuario"] = relationship(back_populates="prestamos")


Session = sessionmaker(bind=engine, expire_on_commit=False)

Base.metadata.create_all(engine)
