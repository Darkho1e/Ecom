import tkinter as tk
from menu import Menu

def main():
    root = tk.Tk()
    root.title("Tic Tac Toe")
    root.geometry("600x600")
    Menu(root)
    root.mainloop()

if __name__ == "__main__":
    main()
