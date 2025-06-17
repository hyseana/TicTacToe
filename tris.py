def create_board():
    """Create an empty 3x3 game board."""
    return [[" " for _ in range(3)] for _ in range(3)]

def print_board(board):
    """Print the game board in a readable format."""
    print("\n")
    for i in range(3):
        print(f" {board[i][0]} | {board[i][1]} | {board[i][2]} ")
        if i < 2:
            print("-----------")
    print("\n")

def is_valid_move(board, row, col):
    """Check if the move is valid (within bounds and empty cell)."""
    if 0 <= row <= 2 and 0 <= col <= 2:
        return board[row][col] == " "
    return False

def check_winner(board):
    """Check if there's a winner."""
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != " ":
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != " ":
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != " ":
        return board[0][2]
    
    return None

def is_board_full(board):
    """Check if the board is full (draw)."""
    return all(cell != " " for row in board for cell in row)

def main():
    print("Benvenuto al gioco del Tris!")
    print("Le posizioni sono indicate da numeri da 0 a 2 per riga e colonna.")
    print("Esempio: per la casella centrale, inserisci riga 1 e colonna 1")
    
    board = create_board()
    current_player = "X"
    
    while True:
        print_board(board)
        print(f"Turno del giocatore {current_player}")
        
        try:
            row = int(input("Inserisci il numero della riga (0-2): "))
            col = int(input("Inserisci il numero della colonna (0-2): "))
        except ValueError:
            print("Errore: Inserisci solo numeri!")
            continue
        
        if not is_valid_move(board, row, col):
            print("Mossa non valida! Riprova.")
            continue
        
        board[row][col] = current_player
        
        winner = check_winner(board)
        if winner:
            print_board(board)
            print(f"Il giocatore {winner} ha vinto!")
            break
        
        if is_board_full(board):
            print_board(board)
            print("Pareggio!")
            break
        
        current_player = "O" if current_player == "X" else "X"

if __name__ == "__main__":
    main() 