import tkinter as tk
import tictactoe , pong, snake
window = tk.Tk()

window.title("Bilke Window")
window.geometry('350x200')
lbl = tk.Label(window, text="Select a Game")
lbl.grid(column=0, row=0)

def snakestart():
    snake.start()
def tictacstart():
    tictactoe.start()
def pong_start():
    pong.start()

btn = tk.Button(window, text="Tic Tac Toe", command=tictacstart)
btn.grid(column=0, row=1)
btn = tk.Button(window, text="Pong", command=pong_start)
btn.grid(column=1, row=1)
btn = tk.Button(window, text="Snake", command=snakestart)
btn.grid(column=2, row=1)
window.mainloop()

