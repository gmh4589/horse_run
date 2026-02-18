
import tkinter as tk
from tkinter import messagebox
from random import choice, randint
from time import sleep
from threading import Thread

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

speed = 5
btns = []
FIELD_SIZE = 15
FIELD_SCALE = 1
y = 7
rot = False
block = False
collide = []
stop = False
scores = 0
line_calc = False

class Figure:
	
	def __init__(self, *coord, name):
		self.coord = coord
		cords_len = len(coord)
		self.position = randint(0, cords_len - 1)
		self.show = self.coord[self.position]
		self.width = max([x for x in list(map(int, self.show[1::2]))]) + 1
		self.height = max([x for x in list(map(int, self.show[::2]))]) + 1
		self.name = name

	def __str__(self):
		return self.name

	def __int__(self):
		return self.position

	def rotate(self):
		self.position += 1

		try:
			self.show = self.coord[self.position]
		except IndexError:
			self.position = 0
			self.show = self.coord[self.position]

		self.width = max([x for x in list(map(int, self.show[1::2]))]) + 1
		self.height = max([x for x in list(map(int, self.show[::2]))]) + 1

	@staticmethod
	def clear_field():
		global collide

		for m in range(FIELD_SIZE):
			for n in range(FIELD_SIZE):

				if (m, n) not in collide:
					btns[m][n].config(bg='#f0f0f0')
				else:
					btns[m][n].config(bg='#ff0000')

	@staticmethod
	def collision(coordinates, x, y):
		collide.append((coordinates[0] + x, coordinates[1] + y))
		collide.append((coordinates[2] + x, coordinates[3] + y))
		collide.append((coordinates[4] + x, coordinates[5] + y))
		collide.append((coordinates[6] + x, coordinates[7] + y))

	@staticmethod
	def show_figure(coordinates, x, y):
		btns[coordinates[0] + x][coordinates[1] + y].config(bg="#ff0000")
		btns[coordinates[2] + x][coordinates[3] + y].config(bg="#ff0000")
		btns[coordinates[4] + x][coordinates[5] + y].config(bg="#ff0000")
		btns[coordinates[6] + x][coordinates[7] + y].config(bg="#ff0000")

	@staticmethod
	def is_collide(coordinates, x, y):
		coll = False

		for c in range(0, len(coordinates), 2):

			if btns[coordinates[c] + x][coordinates[c + 1] + y].config()['background'][-1] == "#ff0000":
				coll = True
				break

		return coll

	def move(self, x):
		global rot, y, collide, block, stop

		for _ in range(5):

			if rot:
				self.rotate()
				rot = False

			coordinates = list(map(int, self.show))
			sleep(speed/50)
			self.clear_field()

			if y > FIELD_SIZE - self.width:
				y -= 1
			elif y < 0:
				y = 0

			if x > FIELD_SIZE - self.height:
				x = FIELD_SIZE - self.height
				self.collision(coordinates, x, y)
				block = True
				break

			try:
				collision = self.is_collide(coordinates, x, y)

				if collision:
					stop = True
					block = True
					self.collision(coordinates, x - 1, y)
					break
				else:
					self.show_figure(coordinates, x, y)

			except IndexError:
				pass

def rotate(fig):
	global rot
	rot = True

root.bind("<Return>", rotate)

def move_y_left(fig):
	global y
	y -= 1

root.bind("<Left>", move_y_left)

def move_y_right(fig):
	global y
	y += 1

root.bind("<Right>", move_y_right)

spawn_list = [
	Figure('00010203', '00102030', name='Line'),
	Figure('01101112', '00101120', '00010211', '01101121', name='Triangle'),
	Figure('00102021', '00010210', '00011121', '02101112', name='L-Shape'),
	Figure('01112021', '00101112', '00011020', '00010212', name='L-Shape (Mirror)'),
	Figure('00101121', '01021011', name='Z-Shape'),
	Figure('01101120', '00011112', name='Z-Shape (Mirror)'),
	Figure('00011011', name='Cube'),
]

def process():
	global rot, y, stop, line_calc

	while True:

		if line_calc:
			sleep(0.1)

		item = choice(spawn_list)
		y = 7

		for _ in range(FIELD_SIZE):

			if not stop:
				item.move(_)

		stop = False

def full_line():
	global collide, block, scores, line_calc

	while True:
		sleep(speed/10)

		if not block:
			continue
		
		lines = 0

		for x in range(FIELD_SIZE):
			rdy = 0
			previous_scores = scores
			line_calc = True

			for y in range(FIELD_SIZE):
				if btns[x][y].config()['background'][-1] == "#ff0000":
					rdy += 1

			if rdy == FIELD_SIZE:
				# scores += 10
				# print(f'СЧЁт: {scores}')
				lines += 1

				for a, col in enumerate(collide):
					if col[0] == x:
						collide[a] = 'to_remove'
					try:
						if col[0] < x:
							collide[a] = (col[0] + 1, col[1])
					except TypeError:
						pass

		if lines == 1:
			scores += 10
		elif lines == 2:
			scores += 25
		elif lines == 3:
			scores += 50
		elif lines >= 4:
			scores += 100

		if scores > previous_scores:
			print(f'СЧЁт: {scores}')

		block = False
		line_calc = False

for i in range(FIELD_SIZE):
	s = []

	for j in range(FIELD_SIZE):
		btn = tk.Button(root, text="", width = 2 * FIELD_SCALE, height = 1 * FIELD_SCALE)
		btn.grid(row=i, column=j)
		s.append(btn)

	btns.append(s)

Thread(target=process, daemon=True).start()
Thread(target=full_line, daemon=True).start()
root.mainloop()
