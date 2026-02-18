import tkinter as tk
from tkinter import messagebox
from random import randint
from time import sleep
from threading import Thread

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
btns = []
move_btn = 'right'
FIELD_SIZE = 15
SPEED = 5
snake_size = 1

def set_up(_):
	global move_btn
	move_btn = 'up'

def set_down(_):
	global move_btn
	move_btn = 'down'

def set_left(_):
	global move_btn
	move_btn = 'left'

def set_right(_):
	global move_btn
	move_btn = 'right'

root.bind("<Up>", set_up)
root.bind("<Down>", set_down)
root.bind("<Left>", set_left)
root.bind("<Right>", set_right)

for i in range(FIELD_SIZE):
	s = []

	for j in range(FIELD_SIZE):
		btn = tk.Button(root, text="", width=2, height=1)
		btn.grid(row=i, column=j)
		s.append(btn)

	btns.append(s)

def apple():
	return (randint(0, FIELD_SIZE - 1), randint(0, FIELD_SIZE - 1))

def process():
	global move_btn, snake_size
	last_btn = None
	x, y = 0, 0
	a = apple()

	while True:
		btns[a[0]][a[1]].config(bg="#00ff00")
		
		if last_btn is not None:
			last_btn.config(bg="#f0f0f0")
		
		try:

			for j in range(FIELD_SIZE):
				for k in range(FIELD_SIZE):
					if (j, k) != a:
						btns[j][k].config(bg="#f0f0f0")
					
			for i in range(snake_size):
				btns[x][y].config(bg="#ff0000")
				last_btn = btns[x][y]
				sleep(1/SPEED)

				if (x, y) == a:
					btns[a[0]][a[1]].config(bg="#f0f0f0")
					a = apple()
					snake_size += 1

				if move_btn == 'right':
					y += 1
				elif move_btn == 'left':
					y -= 1
				elif move_btn == 'up':
					x -= 1
				elif move_btn == 'down':
					x += 1

				if x < 0 or y < 0:
					messagebox.showinfo('MESSAGE', f"YOU LOSE!!!")
					root.destroy()
					break

		except IndexError:
			print(x, y, a)
			messagebox.showinfo('MESSAGE', f"YOU LOSE!!!")
			root.destroy()
			break

Thread(target=process, daemon=True).start()
root.mainloop()