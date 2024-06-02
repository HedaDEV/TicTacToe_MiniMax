def print_board(board):
    for row in board:
        print(" | ".join(row))
    print()

def is_winner(board, player):
    win_conditions = [
        [board[0][0], board[0][1], board[0][2]],
        [board[1][0], board[1][1], board[1][2]],
        [board[2][0], board[2][1], board[2][2]],
        [board[0][0], board[1][0], board[2][0]],
        [board[0][1], board[1][1], board[2][1]],
        [board[0][2], board[1][2], board[2][2]],
        [board[0][0], board[1][1], board[2][2]],
        [board[0][2], board[1][1], board[2][0]]
    ]
    return [player, player, player] in win_conditions

def get_available_moves(board):
    return [(r, c) for r in range(3) for c in range(3) if board[r][c] == " "]

def minimax(board, depth, is_maximizing, player, opponent):
    if is_winner(board, player):
        return 1
    if is_winner(board, opponent):
        return -1
    if not get_available_moves(board):
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = player
            score = minimax(board, depth + 1, False, player, opponent)
            board[move[0]][move[1]] = " "
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_available_moves(board):
            board[move[0]][move[1]] = opponent
            score = minimax(board, depth + 1, True, player, opponent)
            board[move[0]][move[1]] = " "
            best_score = min(score, best_score)
        return best_score

def best_move(board, player, opponent):
    move_found = None
    best_score = float('-inf')
    for move in get_available_moves(board):
        board[move[0]][move[1]] = player
        score = minimax(board, 0, False, player, opponent)
        board[move[0]][move[1]] = " "
        if score > best_score:
            best_score = score
            move_found = move
    return move_found

# Main game loop for AI vs AI
def ai_vs_ai():
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player, opponent = "X", "O"
    while get_available_moves(board):
        move = best_move(board, current_player, opponent)
        if not move:
            print("Draw!")
            break
        board[move[0]][move[1]] = current_player
        print_board(board)
        if is_winner(board, current_player):
            print(f"{current_player} Wins!")
            break
        current_player, opponent = opponent, current_player
    else:
        print("It's a draw!")

ai_vs_ai()
