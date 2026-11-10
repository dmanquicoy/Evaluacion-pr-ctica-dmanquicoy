from datetime import datetime
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from models import Session, Libro, Usuario, Prestamo


class ErrorBiblioteca(Exception):
    pass


def validar_texto(valor, campo):
    valor = (valor or "").strip()
    if not valor:
        raise ErrorBiblioteca(f"El campo {campo} no puede estar vacío.")
    return valor
                       

def validar_ejemplares(cantidad):
    if cantidad < 0:
        raise ErrorBiblioteca("Los ejemplares disponibles no pueden ser negativos.")
    return cantidad


def validar_fecha(fecha):
    fecha = (fecha or "").strip()
    try:
        valida = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d") == fecha
    except ValueError:
        valida = False
    if not valida:
        raise ErrorBiblioteca("La fecha debe tener el formato AAAA-MM-DD y ser real.")
    return fecha


def obtener_libro(sesion, libro_id):
    libro = sesion.get(Libro, libro_id)
    if libro is None:
        raise ErrorBiblioteca(f"No existe un libro con ID {libro_id}.")
    return libro


def obtener_usuario(sesion, usuario_id):
    usuario = sesion.get(Usuario, usuario_id)
    if usuario is None:
        raise ErrorBiblioteca(f"No existe un usuario con ID {usuario_id}.")
    return usuario


def obtener_prestamo(sesion, prestamo_id):
    prestamo = sesion.get(Prestamo, prestamo_id)
    if prestamo is None:
        raise ErrorBiblioteca(f"No existe un préstamo con ID {prestamo_id}.")
    return prestamo


def crear_libro(titulo, autor, ejemplares):
    titulo = validar_texto(titulo, "título")
    autor = validar_texto(autor, "autor")
    validar_ejemplares(ejemplares)
    with Session() as sesion:
        libro = Libro(titulo=titulo, autor=autor, ejemplares_disponibles=ejemplares)
        sesion.add(libro)
        sesion.commit()
        return libro


def listar_libros():
    with Session() as sesion:
        return sesion.scalars(select(Libro).order_by(Libro.id)).all()


def buscar_libro(libro_id):
    with Session() as sesion:
        return obtener_libro(sesion, libro_id)


def actualizar_libro(libro_id, titulo=None, autor=None, ejemplares=None):
    with Session() as sesion:
        libro = obtener_libro(sesion, libro_id)
        if titulo is not None:
            libro.titulo = validar_texto(titulo, "título")
        if autor is not None:
            libro.autor = validar_texto(autor, "autor")
        if ejemplares is not None:
            libro.ejemplares_disponibles = validar_ejemplares(ejemplares)
        sesion.commit()
        return libro


def eliminar_libro(libro_id):
    with Session() as sesion:
        libro = obtener_libro(sesion, libro_id)
        tiene_prestamos = sesion.scalar(
            select(Prestamo.id).where(Prestamo.libro_id == libro_id).limit(1)
        )
        if tiene_prestamos is not None:
            raise ErrorBiblioteca(
                "No se puede eliminar el libro porque tiene préstamos asociados."
            )
        sesion.delete(libro)
        sesion.commit()


def registrar_usuario(nombre, correo):
    nombre = validar_texto(nombre, "nombre")
    correo = validar_texto(correo, "correo").lower()
    with Session() as sesion:
        repetido = sesion.scalar(select(Usuario.id).where(Usuario.correo == correo))
        if repetido is not None:
            raise ErrorBiblioteca("Ya existe un usuario registrado con ese correo.")
        usuario = Usuario(nombre=nombre, correo=correo)
        sesion.add(usuario)
        try:
            sesion.commit()
        except IntegrityError:
            sesion.rollback()
            raise ErrorBiblioteca("Ya existe un usuario registrado con ese correo.")
        return usuario


def listar_usuarios():
    with Session() as sesion:
        return sesion.scalars(select(Usuario).order_by(Usuario.id)).all()


def registrar_prestamo(libro_id, usuario_id, fecha, cantidad):
    fecha = validar_fecha(fecha)
    if cantidad <= 0:
        raise ErrorBiblioteca("La cantidad debe ser un número positivo.")
    with Session() as sesion:
        libro = obtener_libro(sesion, libro_id)
        obtener_usuario(sesion, usuario_id)
        if libro.ejemplares_disponibles < cantidad:
            raise ErrorBiblioteca(
                f"Stock insuficiente: quedan {libro.ejemplares_disponibles} ejemplares "
                f"y se pidieron {cantidad}."
            )
        libro.ejemplares_disponibles -= cantidad
        prestamo = Prestamo(
            libro_id=libro_id,
            usuario_id=usuario_id,
            fecha=fecha,
            cantidad=cantidad,
            estado="activo",
        )
        sesion.add(prestamo)
        sesion.commit()
        return prestamo


def listar_prestamos():
    with Session() as sesion:
        return sesion.scalars(select(Prestamo).order_by(Prestamo.id)).all()


def buscar_prestamo(prestamo_id):
    with Session() as sesion:
        return obtener_prestamo(sesion, prestamo_id)


def devolver_prestamo(prestamo_id):
    with Session() as sesion:
        prestamo = obtener_prestamo(sesion, prestamo_id)
        if prestamo.estado != "activo":
            raise ErrorBiblioteca("Este préstamo ya fue devuelto.")
        prestamo.estado = "devuelto"
        libro = obtener_libro(sesion, prestamo.libro_id)
        libro.ejemplares_disponibles += prestamo.cantidad
        sesion.commit()
        return prestamo

def listar_libros_disponibles():
    with Session() as sesion:
        return sesion.scalars(
            select(Libro).where(Libro.ejemplares_disponibles > 0)
        ).all()
        
