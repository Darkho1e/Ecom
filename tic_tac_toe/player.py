import random

def get_player_info():
    name = input("הכנס שם שחקן: ")
    symbol = input(f"{name}, בחר X או O (או השאר ריק לקבלה אקראית): ").upper()
    if symbol not in ['X', 'O']:
        symbol = random.choice(['X', 'O'])
        print(f"נבחר עבורך: {symbol}")
    return name, symbol
