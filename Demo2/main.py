from tkinter import *
from datetime import datetime
from scraper import scraper
from ClueGenerator import ClueGenerator

master = Tk()
master.title("ArcticFoxes")
now = datetime.now()
dt_string = now.strftime("%d/%m/%Y %H:%M:%S")

w = Canvas(master, width=1500, height=1000, bg="white")

sr= scraper()
letter_matrix, litle_num_matrix, clue_across, clue_down, across_match, down_match = sr.get_data()

cg = ClueGenerator()
new_clues_down, new_clues_across = cg.get_new_clues(across_match, down_match)

print("\nNew Clues (Across): ")
print(new_clues_across)
print("\nNew Clues (Down): ")
print(new_clues_down)

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
    if len(clue) > 35:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        len_line = 0
        while i < len(longClue):
            if len_line >= 30:
                clueToDraw = clueToDraw + "\n" + "   "
                len_line = 0
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
                len_line = len_line + len(longClue[i]) + 2
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
                len_line = len_line + len(longClue[i])+ 1
            i += 1
    else:
        clueToDraw = clue
    down = down + clueToDraw + "\n"

across =""
for clue in clue_across:
    if len(clue) > 35:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        len_line = 0
        while i < len(longClue):
            if len_line >= 30:
                clueToDraw = clueToDraw + "\n" + "   "
                len_line = 0
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
                len_line = len_line + len(longClue[i]) + 2
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
                len_line = len_line + len(longClue[i])+ 1
            i += 1
    else:
        clueToDraw = clue
    across = across + clueToDraw + "\n"

new_down =""
for clue in new_clues_down:
    if len(clue) > 35:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        len_line = 0
        while i < len(longClue):
            if len_line >= 30:
                clueToDraw = clueToDraw + "\n" + "   "
                len_line = 0
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
                len_line = len_line + len(longClue[i]) + 2
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
                len_line = len_line + len(longClue[i])+ 1
            i += 1
    else:
        clueToDraw = clue
    new_down = new_down + clueToDraw + "\n"


new_across =""
for clue in new_clues_across:
    if len(clue) > 35:
        longClue = clue.split()
        i = 0
        clueToDraw = ""
        len_line = 0
        while i < len(longClue):
            if len_line >= 30:
                clueToDraw = clueToDraw + "\n" + "   "
                len_line = 0
            if i == 0:
                clueToDraw = clueToDraw + longClue[i] + "  "
                len_line = len_line + len(longClue[i]) + 2
            else:
                clueToDraw = clueToDraw + longClue[i] + " "
                len_line = len_line + len(longClue[i])+ 1
            i += 1
    else:
        clueToDraw = clue
    new_across = new_across + clueToDraw + "\n"


w.create_text(570, 30,  text="Across", anchor="nw",font="Courier 20 bold" )
w.create_text(570, 80,  text=across, anchor="nw",font="Courier 12" )

w.create_text(1000, 30,  text="Down", anchor="nw",font="Courier 20 bold" )
w.create_text(1000, 80,  text=down, anchor="nw",font="Courier 12" )

w.create_text(570, 270,  text="New Across", anchor="nw",font="Courier 20 bold" )
w.create_text(570, 320,  text=new_across, anchor="nw",font="Courier 12" )

w.create_text(1000, 270,  text="New Down", anchor="nw",font="Courier 20 bold" )
w.create_text(1000, 320,  text=new_down, anchor="nw",font="Courier 12" )

w.create_text(300, 550,  text="ArcticFoxes", anchor="nw",font="Courier 15 bold")


w.pack()

def tick():
    w.delete("upd")
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    w.create_text(300, 580, text=dt_string, anchor="nw",font="Courier 15 bold", tag="upd")

    w.after(1000, tick)
w.after(1, tick)
master.mainloop()