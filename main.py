import tkinter as tk
from tkinter import massagebox

root = tk.Tk() 

root.columconfigure(0, weight=1) 
root.rowconfigure(0, weight=1) 
btns = []
counter = 0
coords = [(-1, 2), (-2, -1), (-2, 1), (-1, 2), (1, 2), (2, 1), (2, -1), (1, -2) ]

def horse_run(x, y):
  global counter
  may_press = 0

  if buns[x][y]['text'] == "    ":
    counter += 1
    btns[x][y]['text'] = str(counter).rjust(3, ' ') 

    for i in range(10):
      for j in range(10):
        if btns[i][j]['text'] != "    ":
          btns[i][j].config(state='disabled', bg="#404040") 
        else:
          btns[i][j].config(state='disabled', bg="#808080") 

    for coord in coords:
      cx,cy = coord
      cx,cy = cx + x, cy + y

      try:
        if cx < 0 or cy < 0 or btns[cx][cy]['text'] != "    ":
          continue
      except IndexError:
        continue

    btns[cx][cy].config(state='active', bg="#000000") 
    may_press += 1

  if may_press == 0:
    messagebox.showinfo('MESSAGE', f" Game over, you're score: {counter}") 

for i in range(10):
  s = []
  for j in range(10):
    btn = tk.Button(root, text="    ", command=lambda x=i, y=j: horse_run(x, y)) 
    btn.grid(row=i, column=j) 
    s.append(btn) 

  btns.append(s) 

root.mainloop() 


  
