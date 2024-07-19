# Tetrominos

Simple clon de tetris hecho con Python y Raylib.

## ToDo

- [x] Estado de Game Over
- [x] Añadir Pausa al juego
- [ ] Menú de inicio
- [ ] Mostrar siguiente pieza
- [x] Puntaje
- [ ] Base de datos de puntajes
- [ ] Sistema de "bolsas" para la selección de piezas
- [ ] Mejorar gráficos
	- [ ] Mejorar interfaz gráfica (fondos, colores, etc)
	- [ ] Efectos gráficos (particulas, transiciones, destellos, etc)
- [ ] Audio
	- [ ] Efectos de sonido
	- [ ] Música de fondo
- [ ] Modos de juego
	- [ ] Moderno
		- [ ] Piezas fantasma
		- [ ] TSpin
	- [ ] Clásico
	- [ ] Multijugador

## Sugerencias

- [ ] Paletas de colores
- [ ] Paletas de colores por nivel
- [ ] Modos de colores aleatorio
- [ ] Modos de colores animado

## Ejecutar

Para ejecutar el juego deberemos dirigirnos a la carpeta raiz del mismo y seguir las instrucciones que detalladas a continuación.

> En este proyecto yo utilizé virtualenv y virtualenv-wrapper para manejar los entornos virtuales.

1. Crear un entorno virtual con virtualenv y virtualenv-wrapper (si no se creo uno anteriormente para el proyecto):

~~~bash
mkvirtualenv tetris
~~~

2. Activar el entorno virtual (por si no lo está):

~~~bash
workon tetris
~~~

3. Instalar las dependencias:

~~~bash
pip install -r requirements.txt
~~~

4. Ejecutar:

~~~bash
python main.py
~~~
