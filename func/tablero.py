class Tablero():
	def __init__(self, columnas=10, filas=20):
		self.__columnas = columnas
		self.__filas = filas
		self.__tablero = [[0 for _ in range(columnas)] for _ in range(filas)]


	def get_columnas(self):
		return self.__columnas


	def get_filas(self):
		return self.__filas


	def get_tablero(self):
		return self.__tablero


	def get_block(self, x, y):
		return self.__tablero[y][x]


	def set_block(self, x, y, valor):
		self.__tablero[y][x] = valor


	def checkear_tablero(self):
		lineas = []
		for y in range(self.get_filas()):
			if not 0 in self.get_tablero()[y]:
				lineas.append(y)
				self.quitar_linea(y)
		return lineas


	def quitar_linea(self, linea):
		while linea > 0:
			self.__tablero[linea] = self.__tablero[linea - 1]
			linea -= 1
		self.__tablero[0] = [0 for _ in range(self.get_columnas())]
