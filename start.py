import tkinter as tk
import tictactoe
import pong
window = tk.Tk()

window.title("Bilkke Window")
window.geometry('350x200')
lbl = tk.Label(window, text="Select Games")
lbl.grid(column=0, row=0)


def tictacstart():
    tictactoe.start()
def pong_start():
    pong.start()

btn = tk.Button(window, text="Tic Tac Toe", command=tictacstart)
btn.grid(column=0, row=1)
btn = tk.Button(window, text="Ping Pong", command=pong_start)
btn.grid(column=1, row=1)
window.mainloop()

