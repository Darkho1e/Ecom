import tkinter as tk
from tkinter import simpledialog
import json
from PIL import Image, ImageTk
from game_gui import GameGUI

USERNAMES_FILE = "usernames.json"

def load_usernames():
    try:
        with open(USERNAMES_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            return data.get("name1", "Player 1"), data.get("name2", "Player 2")
    except Exception:
        return "Player 1", "Player 2"

def save_usernames(name1, name2=None):
    if name2 is None:
        _, old_name2 = load_usernames()
        name2 = old_name2
    with open(USERNAMES_FILE, "w", encoding="utf-8") as f:
        json.dump({"name1": name1, "name2": name2}, f)

class Menu:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.geometry("600x600")
        self.x_image = ImageTk.PhotoImage(Image.open("assets/X.png").resize((100, 100)))
        self.o_image = ImageTk.PhotoImage(Image.open("assets/O.png").resize((100, 100)))
        self.player1_name = None
        self.create_menu()

    def create_menu(self):
        self.clear_frame()
        name1, name2 = load_usernames()
        title_label = tk.Label(self.root, text="Tic Tac Toe", font=("Arial", 24))
        title_label.pack(pady=20)
        name1_label = tk.Label(self.root, text="Player 1 Name:")
        name1_label.pack()
        self.name1_entry = tk.Entry(self.root)
        self.name1_entry.insert(0, name1)
        self.name1_entry.pack(pady=(0, 20))
        vs_friend_btn = tk.Button(self.root, text="Play vs Friend", command=self.prompt_player2, width=20, height=2)
        vs_friend_btn.pack(pady=10)
        vs_bot_btn = tk.Button(self.root, text="Play vs Bot", command=self.show_bot_difficulty, width=20, height=2)
        vs_bot_btn.pack(pady=10)

    def prompt_player2(self):
        self.player1_name = self.name1_entry.get() or "Player 1"
        _, name2 = load_usernames()
        name2 = simpledialog.askstring("Player 2", "Enter name for Player 2:", initialvalue=name2, parent=self.root) or "Player 2"
        save_usernames(self.player1_name, name2)
        self.clear_frame()
        game = GameGUI(self.root, self.x_image, self.o_image, mode="friend", name1=self.player1_name, name2=name2)
        game.start_game()

    def show_bot_difficulty(self):
        if hasattr(self, 'name1_entry') and self.name1_entry.winfo_exists():
            self.player1_name = self.name1_entry.get() or "Player 1"
        elif not self.player1_name:
            self.player1_name, _ = load_usernames()
        save_usernames(self.player1_name)
        self.clear_frame()
        title_label = tk.Label(self.root, text="Choose Bot Difficulty", font=("Arial", 24))
        title_label.pack(pady=20)
        easy_btn = tk.Button(self.root, text="Easy", command=lambda: self.play_vs_bot("easy"), width=20, height=2)
        easy_btn.pack(pady=10)
        medium_btn = tk.Button(self.root, text="Medium", command=lambda: self.play_vs_bot("medium"), width=20, height=2)
        medium_btn.pack(pady=10)
        hard_btn = tk.Button(self.root, text="Hard", command=lambda: self.play_vs_bot("hard"), width=20, height=2)
        hard_btn.pack(pady=10)
        back_btn = tk.Button(self.root, text="Back to Menu", command=self.create_menu, width=20, height=2)
        back_btn.pack(pady=10)

    def play_vs_bot(self, difficulty):
        self.clear_frame()
        game = GameGUI(self.root, self.x_image, self.o_image, mode="bot", name1=self.player1_name or "Player 1", name2="BOT", difficulty=difficulty)
        game.start_game()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()
