from board import create_board, print_board, check_winner, check_draw
from player import get_player_info
from utils import get_move

def play_game():
    print("\nברוכים הבאים למשחק איקס עיגול!\n")

    name1, symbol1 = get_player_info()
    while True:
        name2, symbol2 = get_player_info()
        if symbol2 != symbol1:
            break
        print("הסימן תפוס. בחר סימן אחר.")

    board = create_board()
    current_player, current_symbol = name1, symbol1

    while True:
        print_board(board)
        row, col = get_move(current_player)

        if board[row][col] != " ":
            print("המקום תפוס! נסה שוב.")
            continue

        board[row][col] = current_symbol

        if check_winner(board, current_symbol):
            print_board(board)
            print(f"\n🎉 {current_player} ניצח!\n")
            break

        if check_draw(board):
            print_board(board)
            print("\n🔁 המשחק נגמר בתיקו.\n")
            break

        current_player, current_symbol = (
            (name2, symbol2) if current_player == name1 else (name1, symbol1)
        )

def main():
    while True:
        play_game()
        again = input("\nהאם לשחק שוב? (y/n): ").lower()
        if again != 'y':
            print("\nלהתראות! 👋")
            break

if __name__ == "__main__":
    main()
