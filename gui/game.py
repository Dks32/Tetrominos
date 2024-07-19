from random import choice
import pyray as pr
from func import Tablero, COLORES, Pieza, PIEZAS



class Game():
	def __init__(self):
		pr.init_window(600, 800, 'Tetrominos')
		self.tablero = Tablero()
		self.block_tam = 24
		self.tablero_posx = (pr.get_screen_width() - self.tablero.get_columnas() * self.block_tam) // 2
		self.tablero_posy = (pr.get_screen_height() - self.tablero.get_filas() * self.block_tam) // 2
		self.tablero_width = self.tablero.get_columnas() * self.block_tam
		self.tablero_height = self.tablero.get_filas() * self.block_tam

		self.tiempo = None
		self.pieza = None

		self.velocidad = .5


	def mainloop(self):
		while not pr.window_should_close():
			self.update()
			self.draw_frame()


	def draw_frame(self):
		pr.begin_drawing()
		pr.clear_background(COLORES[0])

		# Dibujar borde del tablero
		pr.draw_rectangle_lines(
			self.tablero_posx - self.block_tam//4,
			self.tablero_posy - self.block_tam//4,
			self.tablero_width + self.block_tam//4 * 2,
			self.tablero_height + self.block_tam//4 * 2,
			pr.GRAY)

		# Dibujar tablero
		for y in range(self.tablero.get_filas()):
			for x in range(self.tablero.get_columnas()):
				self.draw_block(x, y, self.tablero.get_block(x, y))

		# Dibujar pieza actual
		for y in range(len(self.pieza.get_shape())):
			for x in range(len(self.pieza.get_shape()[0])):
				offset_x = self.pieza.get_pos()[0]
				offset_y = self.pieza.get_pos()[1]
				self.draw_block(offset_x + x, offset_y + y, self.pieza.get_block(x, y))

		pr.end_drawing()


	def draw_block(self, x, y, color):
		px = x * self.block_tam + self.tablero_posx
		py = y * self.block_tam + self.tablero_posy

		if color > 0:
			pr.draw_rectangle(px, py, self.block_tam, self.block_tam, COLORES[color])
		else:
			# pr.draw_rectangle_lines(px, py, self.block_tam, self.block_tam, COLORES[color])
			pass


	def update(self):
		if self.pieza == None:
			self.cargar_pieza_nueva()

		tiempo = pr.get_time()
		self.mover_abajo = False
		if (tiempo - self.tiempo) > self.velocidad:
			self.tiempo = tiempo
			self.mover_abajo = True

		# Entradas por teclado
		# tecla = pr.get_key_pressed()
		# if tecla != 0:
		# 	print(tecla)

		if pr.is_key_pressed(263): # Izquierda
			mov = self.pieza.mover(-1, 0)
			self.pieza.bloquear = False
		if pr.is_key_pressed(262): # Derecha
			mov = self.pieza.mover(1, 0)
			self.pieza.bloquear = False
		if pr.is_key_pressed(264) or self.mover_abajo: # Abajo
			if self.pieza.bloquear == False and self.pieza.mover(0, 1) == False:
				self.fijar_pieza()
			else:
				self.pieza.bloquear = False
		if pr.is_key_pressed(265): # Arriba (rotación)
			self.pieza.bloquear = False
			mov = self.pieza.rotar()


	def cargar_pieza_nueva(self):
		self.tiempo = pr.get_time()
		self.pieza = Pieza(self, choice(PIEZAS))
		self.pieza.set_pos((self.tablero.get_columnas() - len(self.pieza.get_shape()[0])) // 2, 0)


	def fijar_pieza(self):
		for y in range(len(self.pieza.get_shape())):
			for x in range(len(self.pieza.get_shape()[0])):
				pos_x = x + self.pieza.get_pos()[0]
				pos_y = y + self.pieza.get_pos()[1]
				self.tablero.set_block(pos_x, pos_y, self.pieza.get_block(x, y) or self.tablero.get_block(pos_x, pos_y))

		self.pieza = None
		self.cargar_pieza_nueva()
		self.tablero.checkear_tablero()


	def validar_mov(self, shape, pos_x, pos_y):
		if pos_x < 0 or pos_x > (self.tablero.get_columnas() - len(shape[0])):
			return False
		if pos_y > (self.tablero.get_filas() - len(shape)):
			return False

		for y in range(len(shape)):
			for x in range(len(shape[0])):
				if self.tablero.get_block(x + pos_x, y + pos_y) and shape[y][x]:
					return False

		return True
