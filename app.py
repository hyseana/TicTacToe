from flask import Flask, render_template, jsonify, request, session
import os
import random

app = Flask(__name__)
app.secret_key = os.urandom(24)

@app.route('/')
def index():
    # Initialize game state if not exists
    if 'board' not in session:
        session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
        session['current_player'] = 'X'
        session['game_over'] = False
        session['game_mode'] = None  # 'ai' or 'duo'
    return render_template('index.html')

@app.route('/set_mode', methods=['POST'])
def set_mode():
    data = request.get_json()
    mode = data.get('mode')
    if mode not in ['ai', 'duo']:
        return jsonify({'error': 'Modalità non valida'}), 400
    
    session['game_mode'] = mode
    session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
    session['current_player'] = 'X'
    session['game_over'] = False
    
    return jsonify({
        'board': session['board'],
        'current_player': 'X',
        'game_mode': mode
    })

@app.route('/make_move', methods=['POST'])
def make_move():
    data = request.get_json()
    row = data.get('row')
    col = data.get('col')
    
    # Get current game state
    board = session.get('board', [[' ' for _ in range(3)] for _ in range(3)])
    current_player = session.get('current_player', 'X')
    game_over = session.get('game_over', False)
    game_mode = session.get('game_mode')
    
    if not game_mode:
        return jsonify({'error': 'Seleziona prima una modalità di gioco'}), 400
    
    # Check if move is valid
    if game_over or board[row][col] != ' ':
        return jsonify({'error': 'Mossa non valida'}), 400
    
    # In AI mode, only allow player (X) to make moves
    if game_mode == 'ai' and current_player != 'X':
        return jsonify({'error': 'Non è il tuo turno'}), 400
    
    # Make player move
    board[row][col] = current_player
    session['board'] = board
    
    # Check for winner after player move
    winner = check_winner(board)
    if winner:
        session['game_over'] = True
        return jsonify({
            'board': board,
            'winner': winner,
            'game_over': True
        })
    
    # Check for draw after player move
    if is_board_full(board):
        session['game_over'] = True
        return jsonify({
            'board': board,
            'draw': True,
            'game_over': True
        })
    
    # If in AI mode and game is not over, make AI move
    if game_mode == 'ai' and not game_over:
        # Make AI move (always as O)
        ai_row, ai_col = make_ai_move(board)
        board[ai_row][ai_col] = 'O'
        session['board'] = board
        
        # Check for winner after AI move
        winner = check_winner(board)
        if winner:
            session['game_over'] = True
            return jsonify({
                'board': board,
                'winner': winner,
                'game_over': True,
                'ai_move': {'row': ai_row, 'col': ai_col}
            })
        
        # Check for draw after AI move
        if is_board_full(board):
            session['game_over'] = True
            return jsonify({
                'board': board,
                'draw': True,
                'game_over': True,
                'ai_move': {'row': ai_row, 'col': ai_col}
            })
        
        return jsonify({
            'board': board,
            'current_player': 'X',  # Always return to player's turn
            'ai_move': {'row': ai_row, 'col': ai_col}
        })
    
    # If in duo mode, switch player
    next_player = 'O' if current_player == 'X' else 'X'
    session['current_player'] = next_player
    
    return jsonify({
        'board': board,
        'current_player': next_player
    })

def make_ai_move(board):
    """Make a random valid move for the AI."""
    empty_cells = [(i, j) for i in range(3) for j in range(3) if board[i][j] == ' ']
    return random.choice(empty_cells)

@app.route('/reset', methods=['POST'])
def reset_game():
    session['board'] = [[' ' for _ in range(3)] for _ in range(3)]
    session['current_player'] = 'X'
    session['game_over'] = False
    return jsonify({
        'board': session['board'],
        'current_player': 'X',
        'game_over': False
    })

def check_winner(board):
    # Check rows
    for row in board:
        if row[0] == row[1] == row[2] != ' ':
            return row[0]
    
    # Check columns
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != ' ':
            return board[0][col]
    
    # Check diagonals
    if board[0][0] == board[1][1] == board[2][2] != ' ':
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != ' ':
        return board[0][2]
    
    return None

def is_board_full(board):
    return all(cell != ' ' for row in board for cell in row)

if __name__ == '__main__':
    app.run(debug=True) 