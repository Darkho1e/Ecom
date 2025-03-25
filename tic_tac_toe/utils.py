def get_move(player_name):
    while True:
        try:
            pos = int(input(f"{player_name}, בחר מספר בין 1 ל-9: "))
            if 1 <= pos <= 9:
                row = (pos - 1) // 3
                col = (pos - 1) % 3
                return row, col
            else:
                print("מספר לא תקין. נסה שוב.")
        except ValueError:
            print("יש להזין מספר בלבד.")

