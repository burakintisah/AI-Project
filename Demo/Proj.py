from tkinter import *
from datetime import datetime
from scraper import scraper

master = Tk()
master.title("ArcticFoxes")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")



w = Canvas(master, width=1500, height=1000, bg="white")

letter_matrix = []
litle_num_matrix = [[1,2,-1,1,3],
                    [1,2,-1,1,3],
                    [1,2,-1,1,3],
                    [4,4,4,4,4],
                    [-1,-1,-1,-1,-1]]

clue_down = []
clue_across = []

sr= scraper()

letter_matrix, litle_num_matrix, clue_across, clue_down, answer_across, answer_down, across_match, down_match= sr.get_data()

offset_x = 30
offset_y = 30
size = 100

for i in range(5):
    for j in range(5):
        x = 100*i + offset_x
        y = 100*j + offset_y

        letter = letter_matrix[j][i]
        if letter == "":
            w.create_rectangle(x, y, x + size, y + size, fill="black", outline='red', width=5)
        else:
            w.create_rectangle(x, y, x + size, y + size, outline='red', width=5)
            w.create_text(x + 50, y + 50, font="Times 40 bold", text=letter )
        num = litle_num_matrix[j][i]
        if num != "-1":
            w.create_text(x + 10, y + 10, text=str(num) )

        w.create_rectangle(x, y, x + size, y + size,  outline = 'red', width=5)

down =""
for clue in clue_across:
    print(len(clue))
    down = down + clue + "\n"

w.create_text(570, 30,  text="Across", anchor="nw",font="Courier 20 bold" )
w.create_text(570, 60,  text=down, anchor="nw",font="Courier 8" )

w.create_text(1000, 30,  text="Down", anchor="nw",font="Courier 20 bold" )

w.create_text(1100, 700,  text="ArcticFoxes", anchor="nw",font="Courier 15 bold")


w.pack()

def tick():
    w.delete("upd")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    w.create_text(1100, 750, text=dt_string, anchor="nw",font="Courier 15 bold", tag="upd")

    w.after(1000, tick)
w.after(1, tick)
master.mainloop()

