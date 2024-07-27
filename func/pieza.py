class Pieza():
	def __init__(self, master, shape):
		self.__pos = [0, 0]
		self.__shape = shape
		# self.__shape = [[0, 5, 0],
		# 				[5, 5, 5]]

		self.bloquear = False
		self.__master = master


	def mover(self, x, y):
		if not self.__master.validar_mov(self.__shape, self.__pos[0]+x, self.__pos[1]+y):
			if y > 0:
				self.__master.fijar_pieza()
			return False

		self.__pos[0] += x
		self.__pos[1] += y
		return True


	def rotar(self, invert=False):
		if invert:
			nshape = list(zip(*[i[::-1] for i in self.__shape]))
		else:
			nshape = list(zip(*self.__shape[::-1]))

		if not self.__master.validar_mov(nshape, self.__pos[0], self.__pos[1]):
			return
		self.__shape = nshape


	def get_pos(self):
		return self.__pos


	def set_pos(self, x, y):
		self.__pos = [x, y]


	def get_block(self, x, y):
		return self.__shape[y][x]


	def get_shape(self):
		return self.__shape
