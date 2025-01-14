# Django App

## Descripción
Este es un proyecto desarrollado en Django que incluye varias funcionalidades relacionadas con la gestión de tareas, metas, rutinas y más.

## Requisitos previos
Antes de comenzar, asegúrate de tener instalado lo siguiente:
- Python 3.8 o superior
- Pip (el gestor de paquetes de Python)
- Un entorno virtual como `venv` (opcional pero recomendado)

## Instalación y configuración

Sigue estos pasos para configurar y correr la aplicación:

### 1. Clonar el repositorio
Clona este repositorio en tu máquina local:
$ git clone https://github.com/jimmyac57/django_app.git 

$ cd django_app

### 2. Crear un entorno virtual
Es recomendable usar un entorno virtual para gestionar las dependencias:
$ python -m venv venv

Activa el entorno virtual:
- En Windows:
  $ venv\Scripts\activate
- En macOS/Linux:
  $ source venv/bin/activate

### 3. Instalar las dependencias
Instala las dependencias del proyecto listadas en el archivo `requirements.txt`:
$ pip install -r requirements.txt

### 4. Configurar la base de datos
Realiza las migraciones para configurar la base de datos:
$ python manage.py migrate

### 5. Crear un superusuario (opcional)
Si necesitas acceso al panel de administración, crea un superusuario:
$ python manage.py createsuperuser

### 6. Correr el servidor
Inicia el servidor de desarrollo de Django:
$ python manage.py runserver

Luego, abre tu navegador y visita [http://127.0.0.1:8000](http://127.0.0.1:8000) para ver la aplicación en funcionamiento.

---

## Uso
1. Accede al sitio principal en `http://127.0.0.1:8000`.
2. Inicia sesión con el superusuario que creaste o registra una nueva cuenta.
3. Explora las funcionalidades de la aplicación.

## Funcionalidades en desarrollo
Actualmente, algunas funcionalidades no están completamente implementadas, pero se están trabajando y se añadirán en el futuro. Aquí están las funcionalidades planificadas:

- **[Tareas]**: Servirá como un sistema de To-Do, donde los usuarios podrán listar tareas por hacer, marcar su importancia y añadir descripciones.

  - _Estado actual_: Funciona para realizar tareas básicas, pero aún no se ha añadido CSS para mejorar la visualización.
  - Plan para añadir: Se incluirán más opciones, como diferentes niveles de importancia, y las tareas se listarán en base a su orden de importancia. Además, se agregarán estilos visuales para mostrarlas como tarjetas.
- **[Rutinas]**: Servirá para guardar rutinas relacionadas con el entrenamiento físico, incluyendo series, repeticiones y peso utilizado.

  - _Estado actual_: Por implementar. Actualmente, los ejercicios solo se pueden añadir a través del panel de administrador (disponible en http://127.0.0.1:8000/admin/ después de crear y loguearse con un superusuario). Aún no se han implementado las series ni detalles adicionales, solo la creación de rutinas y los ejercicios que contienen.
  - Plan para añadir: Se integrarán opciones para gestionar series, repeticiones y peso desde la interfaz de usuario.
- **[Metas]**: Permitirán añadir metas con fechas de término, resultados deseados e identidades objetivo. Cada meta podrá tener objetivos asociados, y será posible registrar progreso para visualizarlo en un gráfico de avance durante el tiempo establecido.

  - _Estado actual_: Por implementar. Es posible crear metas y objetivos, pero aún no se ha implementado la funcionalidad para registrar el progreso ni la visualización de gráficos.
  - Plan para añadir: Implementar la funcionalidad de registrar el progreso y generar gráficos interactivos que muestren el avance de la meta.

### Notas
Si tienes ideas o quieres contribuir a estas funcionalidades, ¡no dudes en abrir un issue o enviar un pull request!

## Contribuciones
Si deseas contribuir a este proyecto, por favor, abre un issue o envía un pull request.

