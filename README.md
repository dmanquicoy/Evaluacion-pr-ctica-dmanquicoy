# Sistema de Gestión de Biblioteca 🏫

Un programa de consola (CLI) sencillo y eficiente para gestionar el préstamo de libros, construido con **Python** y **SQLAlchemy**. Los datos se almacenan de forma local mediante SQLite.

## 🚀 Características

- **Gestión de Libros:** Registra nuevos libros y define sus caracteristicas.
- **Control de Disponibilidad:** Revisa qué libros están disponibles y los que se encuentran prestados.
- **Sistema de Prestamos:** Registra prestamos a los usuarios con una fecha específica de entrega guardando la informacion del usuario al cual se le es prestado y el tipo de libro el cual se le presta, al igual el sistema de prestamos tiene un estado (Activo o Devuelto) el cual se actualiza al ser pedido o entregado

## 🛠️ Tecnologías utilizadas

- Python 3
- SQLAlchemy 2.0 (ORM)
- SQLite (Base de datos)

## 📦 Instalación y Ejecución

1. Clona este repositorio o abre el proyecto en tu entorno (como GitHub Codespaces).
2. Instala las dependencias requeridas usando el archivo `requirements.txt`:
   ```bash
   pip install -r requirements.txt

3. luego de tener esto instalado ejecuta este comando
   ```bash
   python main.py