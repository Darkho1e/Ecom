
def create_board():
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    print("\n")
    for i in range(3):
        row = " | ".join(board[i])
        print(row)
        if i < 2:
            print("-" * 9)
    print("\n")

def check_winner(board, symbol):
    for i in range(3):
        if all([cell == symbol for cell in board[i]]):
            return True
        if all([board[j][i] == symbol for j in range(3)]):
            return True
    if board[0][0] == board[1][1] == board[2][2] == symbol:
        return True
    if board[0][2] == board[1][1] == board[2][0] == symbol:
        return True
    return False

def check_draw(board):
    return all(cell in ['X', 'O'] for row in board for cell in row)
