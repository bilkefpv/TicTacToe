import tkinter as tk
from games.tictactoe import tictactoe
from games.snake import snake
from games.pong import pong
from agent import snake_agent
window = tk.Tk()

window.title("Bilke Window")
window.geometry('450x200')  # Adjusted for more space
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


btn_ttt = tk.Button(window, text="Tic Tac Toe (Normal game)", command=tictacstart)
btn_ttt.grid(column=0, row=1)

btn_pong = tk.Button(window, text="Pong (Vs player or NPC)", command=pong_start)
btn_pong.grid(column=1, row=1)

btn_snake = tk.Button(window, text="Snake (Normal game)", command=snakestart)
btn_snake.grid(column=2, row=1)

btn_snake_ai = tk.Button(window, text="Snake AI (Continue Learning)", command=snakeContinue, bg="yellow", fg="black", font=("Arial", 12, "bold"))

btn_snake_ai.grid(column=0, row=2, columnspan=4, pady=20) 

window.mainloop()

