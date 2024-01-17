class CellAlreadyFilled(ValueError):
    pass

class NoInputError(ValueError):
    pass


class PlayGame:
    game_board = [["", "", ""], ["", "", ""], ["", "", ""]]
    player_1 = "O"
    player_2 = "X"
    active_player = player_1

    # Displays the game intructions
    def game_instructions(self):
        print("HOW TO PLAY:")
        print("Input 2 numbers both between 1-3 with a space in between")
        print("Each number corresponds to the row and column of the board")
        print("--------------------------------------------------------------------------------")
        print("For example: 1 3")
        print("This would be the top right cell of the board. 1 = first row, 3 = last column")
        print("--------------------------------------------------------------------------------")
    
    # Function to start the game if Enter is pressed 
    def start_game(self):
        print("Press Enter to start the game!")
        return input()

    # Displays which player is currently active
    def which_player(self):
        if self.active_player == self.player_1:
            active_player = "Player 1"
        else:
            active_player = "Player 2"

        return active_player

    # Function that switches each player
    def switch_player(self):
        if self.active_player == self.player_1:
            self.active_player = self.player_2
        else:
            self.active_player = self.player_1

    # Displays the board after each turn
    def show_board(self):
        for row in self.game_board:
            formatted_row = [f"{cell:^3}" for cell in row]
            game_board = " | ".join(formatted_row)
            print(game_board)

    # Source of truth whether the board is full or not 
    def check_board_full(self):
        for row in self.game_board:
            for cell in row:
                if cell == "":
                    return False
        return True
    
    # Asks each player to enter a move
    # This function is redundant - player input is now validated in the forms.py
    def get_valid_player_input(self):
        which_player = self.which_player()
        print(f"{which_player} - enter your move.")
        
        while True: 
            player_input = input()

            try:
                if player_input == "":
                    raise NoInputError
                
                row, col = tuple(int(i) for i in player_input.split())
                if row < 1 or col < 1:
                    raise ValueError

                formatted_row = row - 1
                formatted_col = col - 1
                
                if self.game_board[formatted_row][formatted_col] != "":
                    raise CellAlreadyFilled

                return formatted_row, formatted_col
                
            except NoInputError:
                print("There was no input.")
                print("Please input two numbers :)")

            except CellAlreadyFilled:
                print("Cell already filled. Please try again :)")
                
            except (ValueError, IndexError):
                print("Unable to process your input.")
                print("Please input two valid numbers that are between 1-3 :)")

    # Accepts a player input parameter and updates the board data 
    def update_board(self, player_input):
        row = player_input[0]
        col = player_input[1]

        if self.game_board[row][col] != "":
            raise CellAlreadyFilled
    
        self.game_board[row][col] = self.active_player

    # Source of truth to determine who the winner is 
    def check_winner(self):
        which_player = self.which_player()
        # Check rows
        for row in self.game_board:
            if all(cell == self.active_player for cell in row):
                print(f"{which_player} Wins!")
                return True
    
        # Check columns
        for col in range(3):
            if all(self.game_board[row][col] == self.active_player for row in range(3)):
                print(f"{which_player} Wins!")
                return True
            
        # Check diagonal 
        if all(self.game_board[i][i] == self.active_player for i in range(3)):
            print(f"{which_player} Wins!")
            return True
        
        # Check opposite diagonal
        if all(self.game_board[i][2 - i] == self.active_player for i in range(3)):
            print(f"{which_player} Wins!")
            return True
        
        return False
    
    def get_display_board(self):
        return self.game_board
        
    def run(self):
        self.game_instructions()

        if self.start_game() == "":
            while True:
                player_input = self.get_valid_player_input()
                self.update_board(player_input)
                self.show_board()

                if self.check_winner():
                    break

                if self.check_board_full():
                    print("It's a Draw!")
                    break

                self.switch_player()


if __name__ == "__main__":
    PlayGame().run()
