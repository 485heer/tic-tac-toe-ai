import tkinter as tk
from tkinter import messagebox

# -----------------------------
# Game Configuration
# -----------------------------

HUMAN = "X"
AI = "O"

board = [""] * 9


# -----------------------------
# Check Winner
# -----------------------------

def check_winner(board):
    winning_combinations = [
        (0, 1, 2),
        (3, 4, 5),
        (6, 7, 8),
        (0, 3, 6),
        (1, 4, 7),
        (2, 5, 8),
        (0, 4, 8),
        (2, 4, 6)
    ]

    for a, b, c in winning_combinations:
        if board[a] == board[b] == board[c] and board[a] != "":
            return board[a]

    if "" not in board:
        return "Draw"

    return None


# -----------------------------
# Minimax Algorithm
# -----------------------------

def minimax(board, depth, is_maximizing):
    result = check_winner(board)

    # Terminal states
    if result == AI:
        return 10 - depth

    if result == HUMAN:
        return depth - 10

    if result == "Draw":
        return 0

    # AI's turn - maximize score
    if is_maximizing:
        best_score = -float("inf")

        for i in range(9):
            if board[i] == "":
                board[i] = AI

                score = minimax(
                    board,
                    depth + 1,
                    False
                )

                board[i] = ""

                best_score = max(best_score, score)

        return best_score

    # Human's turn - minimize score
    else:
        best_score = float("inf")

        for i in range(9):
            if board[i] == "":
                board[i] = HUMAN

                score = minimax(
                    board,
                    depth + 1,
                    True
                )

                board[i] = ""

                best_score = min(best_score, score)

        return best_score


# -----------------------------
# Find Best AI Move
# -----------------------------

def get_best_move():
    best_score = -float("inf")
    best_move = None

    for i in range(9):
        if board[i] == "":
            board[i] = AI

            score = minimax(
                board,
                0,
                False
            )

            board[i] = ""

            if score > best_score:
                best_score = score
                best_move = i

    return best_move


# -----------------------------
# Handle Human Move
# -----------------------------

def human_move(index):

    # Ignore already occupied cells
    if board[index] != "":
        return

    # Human makes move
    board[index] = HUMAN
    buttons[index].config(
        text=HUMAN,
        state="disabled"
    )

    result = check_winner(board)

    if result:
        end_game(result)
        return

    # AI's turn
    window.after(300, ai_move)


# -----------------------------
# AI Move
# -----------------------------

def ai_move():

    move = get_best_move()

    if move is not None:
        board[move] = AI

        buttons[move].config(
            text=AI,
            state="disabled"
        )

    result = check_winner(board)

    if result:
        end_game(result)


# -----------------------------
# End Game
# -----------------------------

def end_game(result):

    if result == HUMAN:
        messagebox.showinfo(
            "Game Over",
            "You Win! 🎉"
        )

    elif result == AI:
        messagebox.showinfo(
            "Game Over",
            "AI Wins! 🤖"
        )

    else:
        messagebox.showinfo(
            "Game Over",
            "It's a Draw!"
        )

    disable_buttons()


# -----------------------------
# Disable Board
# -----------------------------

def disable_buttons():

    for button in buttons:
        button.config(state="disabled")


# -----------------------------
# Restart Game
# -----------------------------

def restart_game():

    global board

    board = [""] * 9

    for button in buttons:
        button.config(
            text="",
            state="normal"
        )


# -----------------------------
# GUI
# -----------------------------

window = tk.Tk()

window.title("Tic-Tac-Toe AI")
window.geometry("400x500")
window.resizable(False, False)


# Title
title = tk.Label(
    window,
    text="Tic-Tac-Toe",
    font=("Arial", 28, "bold")
)

title.pack(pady=20)


# Information
info = tk.Label(
    window,
    text="You are X   |   AI is O",
    font=("Arial", 14)
)

info.pack(pady=5)


# Game Board
frame = tk.Frame(window)
frame.pack(pady=20)


buttons = []


for i in range(9):

    button = tk.Button(
        frame,
        text="",
        font=("Arial", 28, "bold"),
        width=5,
        height=2,
        command=lambda index=i: human_move(index)
    )

    button.grid(
        row=i // 3,
        column=i % 3,
        padx=3,
        pady=3
    )

    buttons.append(button)


# Restart Button
restart_button = tk.Button(
    window,
    text="Restart Game",
    font=("Arial", 14, "bold"),
    command=restart_game
)

restart_button.pack(pady=20)


# Start Application
window.mainloop()