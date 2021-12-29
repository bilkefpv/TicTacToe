import tkinter as tk
from games.tictactoe import tictactoe
from games.snake import snake
from games.pong import pong
from agent import snake_agent
window = tk.Tk()

window.title("Bilke Window")
window.geometry('350x200')
lbl = tk.Label(window, text="Select a Game")
lbl.grid(column=0, row=0)

def snakestart():
    snake.start()
def snakeContinue():
    snake_agent.train(agent_model=True)
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
btn = tk.Button(window, text="Snake Continue Learning", command=snakeContinue)
btn.grid(column=3, row=1)
window.mainloop()

