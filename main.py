from operaciones import (
    ErrorBiblioteca,
    crear_libro,
    listar_libros,
    buscar_libro,
    actualizar_libro,
    eliminar_libro,
    registrar_usuario,
    listar_usuarios,
    registrar_prestamo,
    listar_prestamos,
    buscar_prestamo,
    devolver_prestamo,
)


def pedir_entero(mensaje, opcional=False):
    while True:
        valor = input(mensaje).strip()
        if opcional and valor == "":
            return None
        try:
            return int(valor)
        except ValueError:
            print("Debes ingresar un número entero.")


def pedir_texto(mensaje, opcional=False):
    valor = input(mensaje).strip()
    if opcional and valor == "":
        return None
    return valor


def mostrar_libro(libro):
    print(
        f"[{libro.id}] {libro.titulo} - {libro.autor} "
        f"(disponibles: {libro.ejemplares_disponibles})"
    )


def mostrar_usuario(usuario):
    print(f"[{usuario.id}] {usuario.nombre} - {usuario.correo}")


def mostrar_prestamo(prestamo):
    print(
        f"[{prestamo.id}] libro {prestamo.libro_id} | usuario {prestamo.usuario_id} | "
        f"{prestamo.fecha} | cantidad {prestamo.cantidad} | {prestamo.estado}"
    )


def mostrar_lista(elementos, mostrar, vacio):
    if not elementos:
        print(vacio)
        return
    for elemento in elementos:
        mostrar(elemento)


def opcion_crear_libro():
    titulo = pedir_texto("Título: ")
    autor = pedir_texto("Autor: ")
    ejemplares = pedir_entero("Ejemplares disponibles: ")
    libro = crear_libro(titulo, autor, ejemplares)
    print("Libro creado con ID", libro.id)


def opcion_listar_libros():
    mostrar_lista(listar_libros(), mostrar_libro, "No hay libros registrados.")


def opcion_buscar_libro():
    libro_id = pedir_entero("ID del libro: ")
    mostrar_libro(buscar_libro(libro_id))


def opcion_actualizar_libro():
    libro_id = pedir_entero("ID del libro a actualizar: ")
    buscar_libro(libro_id)
    print("Deja vacío lo que no quieras cambiar.")
    titulo = pedir_texto("Nuevo título: ", opcional=True)
    autor = pedir_texto("Nuevo autor: ", opcional=True)
    ejemplares = pedir_entero("Nuevos ejemplares disponibles: ", opcional=True)
    libro = actualizar_libro(libro_id, titulo, autor, ejemplares)
    print("Libro actualizado:")
    mostrar_libro(libro)


def opcion_eliminar_libro():
    libro_id = pedir_entero("ID del libro a eliminar: ")
    eliminar_libro(libro_id)
    print("Libro eliminado.")


def opcion_registrar_usuario():
    nombre = pedir_texto("Nombre: ")
    correo = pedir_texto("Correo: ")
    usuario = registrar_usuario(nombre, correo)
    print("Usuario registrado con ID", usuario.id)


def opcion_listar_usuarios():
    mostrar_lista(listar_usuarios(), mostrar_usuario, "No hay usuarios registrados.")


def opcion_registrar_prestamo():
    libro_id = pedir_entero("ID del libro: ")
    usuario_id = pedir_entero("ID del usuario: ")
    fecha = pedir_texto("Fecha (AAAA-MM-DD): ")
    cantidad = pedir_entero("Cantidad: ")
    prestamo = registrar_prestamo(libro_id, usuario_id, fecha, cantidad)
    print("Préstamo registrado con ID", prestamo.id)


def opcion_listar_prestamos():
    mostrar_lista(listar_prestamos(), mostrar_prestamo, "No hay préstamos registrados.")


def opcion_buscar_prestamo():
    prestamo_id = pedir_entero("ID del préstamo: ")
    mostrar_prestamo(buscar_prestamo(prestamo_id))


def opcion_devolver_prestamo():
    prestamo_id = pedir_entero("ID del préstamo a devolver: ")
    devolver_prestamo(prestamo_id)
    print("Préstamo devuelto correctamente.")


OPCIONES = {
    1: opcion_crear_libro,
    2: opcion_listar_libros,
    3: opcion_buscar_libro,
    4: opcion_actualizar_libro,
    5: opcion_eliminar_libro,
    6: opcion_registrar_usuario,
    7: opcion_listar_usuarios,
    8: opcion_registrar_prestamo,
    9: opcion_listar_prestamos,
    10: opcion_buscar_prestamo,
    11: opcion_devolver_prestamo,
}


def mostrar_menu():
    print()
    print("===== BIBLIOTECA =====")
    print("1. Crear libro")
    print("2. Listar libros")
    print("3. Buscar libro por ID")
    print("4. Actualizar libro")
    print("5. Eliminar libro")
    print("6. Registrar usuario")
    print("7. Listar usuarios")
    print("8. Registrar préstamo")
    print("9. Listar préstamos")
    print("10. Buscar préstamo por ID")
    print("11. Devolver préstamo")
    print("0. Salir")


def main():
    while True:
        mostrar_menu()
        try:
            opcion = pedir_entero("Elige una opción: ")
            if opcion == 0:
                print("Hasta luego.")
                break
            accion = OPCIONES.get(opcion)
            if accion is None:
                print("Esa opción no existe.")
                continue
            accion()
        except ErrorBiblioteca as error:
            print("Error:", error)
        except (KeyboardInterrupt, EOFError):
            print("\nHasta luego.")
            break
        except Exception as error:
            print("Ocurrió un problema inesperado:", error)


if __name__ == "__main__":
    main()
