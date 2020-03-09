from tkinter import *
from datetime import datetime
from scraper import scraper

master = Tk()
master.title("ArcticFoxes")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")



w = Canvas(master, width=1500, height=1000, bg="white")

sr= scraper()
letter_matrix, litle_num_matrix, clue_across, clue_down, across_match, down_match= sr.get_data()

offset_x = 30
offset_y = 30
size = 100

for i in range(5):
    for j in range(5):
        x = 100*i + offset_x
        y = 100*j + offset_y

        letter = letter_matrix[j][i]
        if letter == "":
            w.create_rectangle(x, y, x + size, y + size, fill="black", outline="black", width   =2)
        else:
            w.create_rectangle(x, y, x + size, y + size, outline="black", width=2)
            w.create_text(x + 50, y + 50, font="Times 40 bold", text=letter, fill = "blue" )
        num = litle_num_matrix[j][i]
        if num != "-1":
            w.create_text(x + 13, y + 15, text=str(num) , font= "Times 20 bold")

w.create_rectangle(30, 30, 530, 530,  outline = 'black', width=5)

down =""
for clue in clue_down:
    if len(clue) > 40:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        while i <= len(longClue)/2 +  1 :
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
            i += 1
        clueToDraw = clueToDraw + "\n" + "   "
        while i < len(longClue):
            clueToDraw = clueToDraw + longClue[i] + " "
            i += 1
    else:
        clueToDraw = clue
    down = down + clueToDraw + "\n"

across =""
print("across")
for clue in clue_across:
    if len(clue) > 40:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        while i <= len(longClue)/2 + 1:
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
            i += 1
        clueToDraw = clueToDraw + "\n" + "   "
        while i < len(longClue):
            clueToDraw = clueToDraw + longClue[i] + " "
            i += 1
    else:
        clueToDraw = clue
    across = across + clueToDraw + "\n"



w.create_text(570, 30,  text="Across", anchor="nw",font="Courier 20 bold" )
w.create_text(570, 80,  text=across, anchor="nw",font="Courier 12" )

w.create_text(1000, 30,  text="Down", anchor="nw",font="Courier 20 bold" )
w.create_text(1000, 80,  text=down, anchor="nw",font="Courier 12" )

w.create_text(540, 550,  text="ArcticFoxes", anchor="nw",font="Courier 15 bold")


w.pack()

def tick():
    w.delete("upd")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    w.create_text(540, 580, text=dt_string, anchor="nw",font="Courier 15 bold", tag="upd")

    w.after(1000, tick)
w.after(1, tick)
master.mainloop()

