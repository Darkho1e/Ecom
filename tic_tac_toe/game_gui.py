import tkinter as tk
from tkinter import messagebox
import random
from board import create_board, check_winner, check_draw
from PIL import Image, ImageTk

BUTTON_SIZE = 100  # pixels
BOARD_SIZE = BUTTON_SIZE * 3

class GameGUI:
    def __init__(self, root, x_image, o_image, mode="friend", name1="Player 1", name2="Player 2", difficulty=None):
        self.root = root
        self.mode = mode
        self.name1 = name1
        self.name2 = name2
        self.difficulty = difficulty
        self.current_player = "X"
        self.board = create_board()
        self.buttons = [[None for _ in range(3)] for _ in range(3)]
        self.board_frame = None
        self.symbol_to_name = {"X": self.name1, "O": self.name2}
        self.x_image = ImageTk.PhotoImage(x_image._PhotoImage__photo.zoom(BUTTON_SIZE // x_image.width(), BUTTON_SIZE // x_image.height())) if x_image.width() != BUTTON_SIZE else x_image
        self.o_image = ImageTk.PhotoImage(o_image._PhotoImage__photo.zoom(BUTTON_SIZE // o_image.width(), BUTTON_SIZE // o_image.height())) if o_image.width() != BUTTON_SIZE else o_image

    def start_game(self):
        self.clear_window()
        self.create_game_board()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_game_board(self):
        self.board_frame = tk.Frame(self.root, width=BOARD_SIZE, height=BOARD_SIZE)
        self.board_frame.pack(expand=True)
        self.board_frame.pack_propagate(False)

        for i in range(3):
            for j in range(3):
                btn = tk.Button(
                    self.board_frame,
                    width=BUTTON_SIZE, height=BUTTON_SIZE,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    relief="solid",
                    bd=2,
                    highlightbackground="black",
                    highlightcolor="black",
                    highlightthickness=2,
                    bg="white"
                )
                btn.place(x=j*BUTTON_SIZE, y=i*BUTTON_SIZE, width=BUTTON_SIZE, height=BUTTON_SIZE)
                self.buttons[i][j] = btn

        self.board_frame.config(width=BOARD_SIZE, height=BOARD_SIZE)
        self.board_frame.pack(expand=True)

        back_btn = tk.Button(self.root, text="Back to Menu",
                             command=self.return_to_menu, width=20)
        back_btn.pack(pady=10)

    def make_move(self, row, col):
        if self.board[row][col] != " " or self.buttons[row][col] is None:
            return

        self.board[row][col] = self.current_player
        img = self.x_image if self.current_player == "X" else self.o_image
        self.buttons[row][col].config(image=img, text="")
        self.buttons[row][col].image = img

        if check_winner(self.board, self.current_player):
            messagebox.showinfo("Game Over", f"{self.symbol_to_name[self.current_player]} wins!")
            self.return_to_menu()
            return

        if check_draw(self.board):
            messagebox.showinfo("Game Over", "It's a draw!")
            self.return_to_menu()
            return

        self.current_player = "O" if self.current_player == "X" else "X"

        if self.mode == "bot" and self.current_player == "O":
            self.bot_move()

    def bot_move(self):
        empty_cells = [(i, j) for i in range(3) for j in range(3)
                       if self.board[i][j] == " " and self.buttons[i][j] is not None]
        if not empty_cells:
            return
        if self.difficulty == "hard":
            self.hard_bot_move()
        else:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)

    def hard_bot_move(self):
        best_score = float('-inf')
        best_move = None
        for i in range(3):
            for j in range(3):
                if self.board[i][j] == " ":
                    self.board[i][j] = "O"
                    score = self.minimax(False)
                    self.board[i][j] = " "
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        if best_move:
            self.make_move(best_move[0], best_move[1])

    def minimax(self, is_maximizing):
        if check_winner(self.board, "O"):
            return 1
        if check_winner(self.board, "X"):
            return -1
        if check_draw(self.board):
            return 0
        if is_maximizing:
            best_score = float('-inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "O"
                        score = self.minimax(False)
                        self.board[i][j] = " "
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(3):
                for j in range(3):
                    if self.board[i][j] == " ":
                        self.board[i][j] = "X"
                        score = self.minimax(True)
                        self.board[i][j] = " "
                        best_score = min(score, best_score)
            return best_score

    def return_to_menu(self):
        import main_gui
        self.root.destroy()
        main_gui.main()
