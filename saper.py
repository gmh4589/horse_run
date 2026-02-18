import tkinter as tk
from tkinter import messagebox
from random import randint

root = tk.Tk()

root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)
clicks = 0
btns = []
mines = []
mines_count = 10

def get_coord(x, y, i):
	return [(x - i, y - i), (x - i, y), (x - i, y + i), (x, y - i), (x, y + i), (x + i, y - i), (x + i, y), (x + i, y + i)]

def mine_detect(x, y):
	global clicks
	close_min = 10

	if (x, y) in mines:
		print("BOOM!!!")
		btns[x][y]['text'] = "💥" 
		messagebox.showinfo('MESSAGE', f"YOU LOSE!!!")
		root.destroy()
		return

	for i in range(10):
		for c in get_coord(x, y, i):
			if c in mines and close_min > i:
				close_min = i
				break

	if btns[x][y]['text'] == "":
		btns[x][y]['text'] = str(close_min)
		clicks += 1

	for mine in mines:
		detected = 0

		for c in get_coord(mine[0], mine[1], 1):

			try:
				if c in mines or btns[c[0]][c[1]]['text'] == "1" or c[0] < 0 or c[1] < 0:
					detected += 1
			except IndexError:
				detected += 1

		if detected == 8:
			btns[mine[0]][mine[1]]['text'] = "💣"
	
	if clicks == 100 - mines_count:
		messagebox.showinfo('MESSAGE', f"YOU WIN!!!")


for i in range(mines_count):
	
	while True:
		r = (randint(0, 9), randint(0, 9))
		if r not in mines:
			mines.append(r)
			break

for i in range(10):
	s = []

	for j in range(10):
		btn = tk.Button(root, text="", width=4, height=2,
			command=lambda x=i, y=j: mine_detect(x, y)
		)
		btn.grid(row=i, column=j)
		s.append(btn)

	btns.append(s)

root.mainloop()
