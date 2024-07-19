from random import choice
import pyray as pr
from func import Tablero, COLORES, Pieza, PIEZAS



class Game():
	def __init__(self):
		pr.init_window(600, 800, 'Tetrominos')
		pr.set_target_fps(120)
		pr.set_exit_key(0)

		self.tablero = Tablero()
		self.block_tam = 32
		self.tablero_posx = (pr.get_screen_width() - self.tablero.get_columnas() * self.block_tam) // 2
		self.tablero_posy = (pr.get_screen_height() - self.tablero.get_filas() * self.block_tam) // 2
		self.tablero_width = self.tablero.get_columnas() * self.block_tam
		self.tablero_height = self.tablero.get_filas() * self.block_tam

		self.tiempo = None
		self.pieza = None

		self.velocidad = .5

		self.puntaje = 0
		self.lineas = 0
		self.nivel = 0
		self.piezas_colocadas = 0
		self.info_pos_x = (pr.get_screen_width() // 2) - (pr.measure_text(self.get_info_string(), 20) // 2)

		self.pause_mode = False
		self.game_over = False


	def mainloop(self):
		while not pr.window_should_close():
			if self.pause_mode or self.game_over:
				self.update_pause()
			else:
				self.update()
			self.draw_frame()


	def draw_frame(self):
		pr.begin_drawing()
		pr.clear_background(COLORES[0])

		# Información de juego (puntaje, lineas...)
		self.draw_info()

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
		if self.pieza != None:
			for y in range(len(self.pieza.get_shape())):
				for x in range(len(self.pieza.get_shape()[0])):
					offset_x = self.pieza.get_pos()[0]
					offset_y = self.pieza.get_pos()[1]
					self.draw_block(offset_x + x, offset_y + y, self.pieza.get_block(x, y))

		# Mostrar Menu (Pausa | Game Over | Menú inicial)
		if self.pause_mode or self.game_over:
			pr.draw_rectangle(
				self.tablero_posx - self.block_tam//4,
				self.tablero_posy - self.block_tam//4,
				self.tablero_width + self.block_tam//4 * 2,
				self.tablero_height + self.block_tam//4 * 2,
				pr.Color(0, 0, 0, 128))

			pr.draw_text(
					self.msg_menu,
					(pr.get_screen_width() - pr.measure_text(self.msg_menu, 40)) // 2,
					pr.get_screen_height() // 4,
					40,
					pr.Color(255, 255, 255, 192))

		pr.draw_fps(10, 10)
		pr.end_drawing()


	def draw_info(self):
		pr.draw_text(self.get_info_string(), self.info_pos_x, self.tablero_posy + self.tablero_height + 15, 20, pr.GRAY)


	def get_info_string(self):
		# return f'[ {self.nivel:>2} : {self.puntaje:>8} : {self.lineas:>5} : {self.piezas_colocadas:>5} ]'
		return f'[ {self.nivel:>2} : {self.puntaje:>8} ]'


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
		tecla = pr.get_key_pressed()
		if tecla != 0:
			print(tecla)

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
		if pr.is_key_pressed(256): # Esc (pausa)
			self.pause_mode = not self.pause_mode


	def update_pause(self):
		if pr.is_key_pressed(256): # Esc (pausa)
			self.pause_mode = not self.pause_mode


	def cargar_pieza_nueva(self):
		self.tiempo = pr.get_time()
		self.pieza = Pieza(self, choice(PIEZAS))
		self.pieza.set_pos((self.tablero.get_columnas() - len(self.pieza.get_shape()[0])) // 2, 0)

		# GAME OVER (Si no hay espacio para mover una pieza nueva)
		self.game_over = not self.validar_mov(self.pieza.get_shape(), self.pieza.get_pos()[0], self.pieza.get_pos()[1])
		print(self.game_over)


	def fijar_pieza(self):
		for y in range(len(self.pieza.get_shape())):
			for x in range(len(self.pieza.get_shape()[0])):
				pos_x = x + self.pieza.get_pos()[0]
				pos_y = y + self.pieza.get_pos()[1]
				self.tablero.set_block(pos_x, pos_y, self.pieza.get_block(x, y) or self.tablero.get_block(pos_x, pos_y))

		self.pieza = None
		self.cargar_pieza_nueva()
		lineas = self.tablero.checkear_tablero()

		# Calculo de puntaje y nivel
		puntos = 10 * (self.nivel + 1) 
		puntos += len(lineas) * 100 * (self.nivel + 1)
		self.puntaje += puntos
		self.piezas_colocadas += 1
		self.lineas += len(lineas)
		self.nivel = self.lineas // 10
		# print(f'[{len(lineas)}]{lineas}')


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


	@property
	def msg_menu(self):
		if self.game_over:
			return 'Game Over!'
		if self.pause_mode:
			return 'En pausa'
		return 'TETROMINOS'
