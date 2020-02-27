import sys

d = {1: '_', 2: '_', 3: '_', 4: '_', 5: '_', 6: '_', 7: '_', 8: '_', 9: '_'}


def board():
    for i in range(1, 10):
        print(i, d[i], end=" ")
        if i == 3 or i == 6:
            print(' ')
    print()
    print('type number between 1 and nine')


def winnerwinnerchickendinner(y, player):
    if d[1] == y and d[2] == y and d[3] == y:
        print(player, "Wins!")
        sys.exit()
    elif d[4] == y and d[5] == y and d[6] == y:
        print(player, "Wins!!")
        sys.exit()
    elif d[7] == y and d[8] == y and d[9] == y:
        print(player, "Wins!!!")
        sys.exit()
    elif d[1] == y and d[4] == y and d[7] == y:
        print(player, "Wins!!!!")
        sys.exit()
    elif d[2] == y and d[5] == y and d[8] == y:
        print(player, 'Wins!!!!!')
        sys.exit()
    elif d[3] == y and d[6] == y and d[9] == y:
        print(player, 'Wins!!!!!!')
        sys.exit()
    elif d[1] == y and d[5] == y and d[9] == y:
        print(player, 'Wins!!!!!!!')
        sys.exit()
    elif d[3] == y and d[5] == y and d[7] == y:
        print(player, 'Wins!!!!!!!!!')
        sys.exit()


player = 1
board()
counter = 0
print('This is a 2 play er ga me')
while counter <= 9:
    if player == 1:
        rar = int(input())
        while d[rar] == 'x' or d[rar] == 'o':
            rar = int(input('Try Again'))
        d[rar] = 'x'
        board()
        player = 2
        counter = counter + 1
        winnerwinnerchickendinner('x', 'Player 1')

    if counter == 9:
        break
    print(counter)

    if player == 2:
        rar = int(input())
        while d[rar] == 'x' or d[rar] == 'o':
            rar = int(input('Try Again'))
        d[rar] = 'o'
        board()
        player = 1
        counter = counter + 1
        winnerwinnerchickendinner('o', 'Player 2')

print('tic tac toe game is over')


