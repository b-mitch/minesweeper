# Implement a functioning command line game of minesweeper using object-oriented design principles

import random
yes = ['y','yes','yeah','ya','ys','yesh','yep','yurp','yeppers','yessir','yes!']
class Card:
    def __init__(self, data):
        self.data = data
        self.flipped = False
        self.flagged = False

    def __repr__(self):
        if self.data is None:
            return 'None'
        return self.data
    
    def flip(self): 
        self.flipped = True
        
    def flag(self):
        self.flagged = not self.flagged
    
class Board:
    def __init__(self, n, level):
        # Initialize an nxn matrix for the cards
        cards = [[Card(None) for _ in range(n)] for _ in range(n)]

        # Assign number of bombs based on selected difficulty level
        bombs = 0
        if level == 'easy':
            bombs = n * n // 7
        elif level == 'medium':
            bombs = n * n // 5
        elif level == 'hard':
            bombs = n * n // 3

        # Get random, non-repeated positions for each bomb
        bomb_positions = []
        for i in range(bombs):
            random_index = random.randrange((n * n))
            while random_index in bomb_positions:
                random_index = random.randrange((n * n))
            bomb_positions.append(random_index)

        # Insert each bomb into the cards matrix
        for position in bomb_positions:
            column_i = position // n
            row_i = position - (n * column_i)
            cards[column_i][row_i] = Card('*')

        # Insert card with value determined by number of adjacent bombs
        for i in range(len(cards)):
            for j in range(len(cards[i])):
                if cards[i][j].data == '*':
                    continue
                adj_bombs = 0
                if j - 1 >= 0 and cards[i][j-1].data == '*':
                    adj_bombs += 1
                if j + 1 < len(cards[i]) and cards[i][j+1].data == '*':
                    adj_bombs += 1
                if i - 1 >= 0:
                    if cards[i-1][j].data == '*':
                        adj_bombs += 1
                    if j - 1 >= 0 and cards[i-1][j-1].data == '*':
                        adj_bombs += 1
                    if j + 1 < len(cards[i]) and cards[i-1][j+1].data == '*':
                        adj_bombs += 1
                if i + 1 < len(cards):
                    if cards[i+1][j].data == '*':
                        adj_bombs += 1
                    if j - 1 >= 0 and cards[i+1][j-1].data == '*':
                        adj_bombs += 1
                    if j + 1 < len(cards[i]) and cards[i+1][j+1].data == '*':
                        adj_bombs += 1
                cards[i][j] = Card(str(adj_bombs))

        self.cards = cards

    def check_flipped(self, row, column):
        return self.cards[row][column].flipped

    def flip_card(self, row, col):
        value = self.cards[row][col].data
        # If not adjacent to a bomb check and flip any neighbords that are also not touching bombs
        if value == '0':
            self.flip_zeros(row, col)
        self.cards[row][col].flip()
        return value

    def flip_zeros(self, row, col):
        # Base case - if out of bounds or already flipped
        if row < 0 or row >= len(self.cards) or col < 0 or col >= len(self.cards[row]) or self.cards[row][col].flipped:
            return
        # If card has a value of 0, flip it and recurse neighbors
        if self.cards[row][col].data == '0':
            self.cards[row][col].flip()
            self.flip_zeros(row-1, col)
            self.flip_zeros(row+1, col)
            self.flip_zeros(row, col-1)
            self.flip_zeros(row, col+1)
            self.flip_zeros(row+1, col-1)
            self.flip_zeros(row+1, col+1)
            self.flip_zeros(row-1, col-1)
            self.flip_zeros(row-1, col+1)

    def check_flagged(self, row, column):
        return self.cards[row][column].flagged

    def flag_card(self, row, column):
        self.cards[row][column].flag()

    # Iterate cards. If all non-bombs have been flipped, flip all bombs and return true
    def check_winner(self):
        for row in self.cards:
            for card in row:
                if card.data != '*':
                    if not card.flipped:
                        return False
        for row in self.cards:
            for card in row:
                card.flagged = False
                card.flipped = True
        return True

    def view_board(self):
        for i in range(len(self.cards)):
            for j in range(len(self.cards[i])):
                if self.cards[i][j].flipped:
                    print(self.cards[i][j], end=' ')
                elif self.cards[i][j].flagged:
                    print('!', end=' ')
                else:
                    print('[]', end='')
            print()

class Game:
    def __init__(self):
        self.board = None

    def start_ng(self):
        print('\n')
        print('Welcome to Minesweeper!')
        print('\n')
        print('RULES')
        print('1. Flip over cards to reveal their value. Cards are selected based on their position in an nxn matrix. The first position is row 0, column 0.')
        print('2. The value of the card tells you how many bombs are located in adjacent positions.')
        print('3. Flip over a bomb card and you lose!')
        print('4. Flip over every card except bomb cards and you win!')
        print('5. Flag cards as potential bombs to avoid accidentally flipping them.')
        print('\n')
        print('Ready to begin?? y/n')
        begin = input('>> ')
        if not begin.lower() in yes:
            print('No problem! Feel free to start a new game when you are ready!')
            return
        else:
            print('Enter a number to create board of size number x number (must be 5-10).')
            while True:
                try:
                    n = input('>> ')
                    n = int(n)
                    if n < 5 or n > 10:
                        print('Invalid input. Must be an integer between 5 and 10, inclusive')
                    else:
                        break
                except ValueError:
                    print('Invalid input. Must be an integer between 5 and 10, inclusive')
            print('Select a difficulty: easy, medium or hard')
            difficulty = input('>> ').lower()
            while difficulty != 'easy' and difficulty != 'medium' and difficulty != 'hard':
                print('You can only select from the following difficulty levels: easy, medium or hard. Please choose one.')
                difficulty = input('>> ').lower() 
            self.start_game(n, difficulty)

    def start_game(self, n, level):
        self.board = Board(n, level)
        while True:
            print('\n')
            self.board.view_board()
            print('Please select a card to flip or flag')
            while True:
                try:
                    row = int(input('row >> '))
                    row = int(row)
                    if row < 0 or row >= n:
                        print(f'Please enter an integer between 0 and {n - 1}, inclusive')
                    else:
                        break
                except ValueError:
                    print(f'Please enter an integer between 0 and {n - 1}, inclusive')
            
            while True:
                try:
                    column = int(input('column >> '))
                    column = int(column)
                    if column < 0 or column >= n:
                        print(f'Please enter an integer between 0 and {n - 1}, inclusive')
                    else:
                        break
                except ValueError:
                    print(f'Please enter an integer between 0 and {n - 1}, inclusive')

            print('\n')
            print(f'You have selected the card at row: {row}, column: {column}')
            print('Would you like to: FLIP the card? FLAG the card? or Choose a NEW card?')
            card_action = input('>> ').lower()
            while card_action != 'flip' and card_action != 'flag' and card_action != 'new':
                print('You have one of three card action choices: 1. To flip the card, enter FLIP 2. To flag the card, enter FLAG 3. To choose a new card, enter NEW?')
                card_action = input('flip, flag or new? >> ')

            if card_action == 'new':
                continue
            elif self.board.check_flipped(row, column):
                print('\n')
                print('CARD ALREADY FLIPPED, please select another')
                continue
            elif card_action == 'flag':
                if self.board.check_flagged(row, column):
                    print('You previously flagged this card as a potential bomb. Would you like to unflag it? y/n')
                    flip_flagged = input('>> ')
                    if flip_flagged not in yes:
                        continue
                self.board.flag_card(row, column)
            elif card_action == 'flip':
                if self.board.check_flagged(row, column):
                    print('You previously flagged this card as a potential bomb. Would you still like to flip it? y/n')
                    flip_flagged = input('>> ')
                    if flip_flagged not in yes:
                        continue
                flipped_card = self.board.flip_card(row, column)
                loser = flipped_card == '*'
                winner = self.board.check_winner()
                if loser:
                    self.board.view_board()
                    print('You flipped a bomb! Game Over!')
                elif winner:
                    self.board.view_board()
                    print('You flipped over all cards besides the bombs! You win!')
                else:
                    continue

                print('\n')
                print('Play again with SAME board size and difficulty?? y/n')
                play_again = input('>> ')
                if play_again.lower() in yes:
                    self.board = Board(n, level)
                    continue
                else:
                    print('Play again with NEW board size or difficulty?? y/n')
                    play_again = input('>> ')
                    if play_again.lower() in yes:
                        self.start_ng()
                        return
                    else:
                        print('Thanks for playing!')
                        return


minesweeper = Game()
minesweeper.start_ng()

        

