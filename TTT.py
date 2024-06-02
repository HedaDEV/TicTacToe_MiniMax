import matplotlib.pyplot as plt
import networkx as nx

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
        score = minimax(board, 9, False, player, opponent)
        board[move[0]][move[1]] = " "
        if score > best_score:
            best_score = score
            move_found = move
    return move_found

# Game loop for AI vs AI
def ai_vs_ai():
    """Simulate a game of Tic Tac Toe between two AI players using the Minimax algorithm."""
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

def minimax_graph(board, depth, is_maximizing, player, opponent, graph, parent_node=None, move_made=None, max_depth=1):
    """
    This function recursively generates a decision tree for the Minimax algorithm,
    visualizing each game state up to a specified maximum depth.

    Parameters:
    - board: Current state of the Tic Tac Toe board
    - depth: Current depth in the recursion
    - is_maximizing: Boolean flag indicating if the current move is maximizing or minimizing
    - player: Symbol representing the current player ('X' or 'O')
    - opponent: Symbol representing the opponent
    - graph: NetworkX graph object to which nodes and edges are added
    - parent_node: Label of the parent node in the graph
    - move_made: Tuple representing the move made to reach the current board state
    - max_depth: Maximum depth of the tree to visualize (default is 2)
    """
    node_label = board_to_string(board)
    if move_made is not None:
        node_label += f"\nMove: {move_made}"
    graph.add_node(node_label)
    if parent_node:
        graph.add_edge(parent_node, node_label)
    
    if depth >= max_depth:
        return 0, node_label  # Stop going deeper

    if is_winner(board, player):
        return 1, node_label
    if is_winner(board, opponent):
        return -1, node_label
    if not get_available_moves(board):
        return 0, node_label

    best_score = float('-inf') if is_maximizing else float('inf')
    for move in get_available_moves(board):
        board[move[0]][move[1]] = player if is_maximizing else opponent
        score, child_node = minimax_graph(board, depth + 1, not is_maximizing, player, opponent, graph, node_label, move, max_depth)
        board[move[0]][move[1]] = " "
        if is_maximizing and score > best_score or not is_maximizing and score < best_score:
            best_score = score
    return best_score, node_label

def board_to_string(board):
    return "\n".join(" | ".join(row) for row in board)

def hierarchy_pos(G, root=None, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5):
    if root is None:
        root = next(iter(G.nodes))  # This gets the first node if root is unspecified

    def _hierarchy_pos(G, root, width=1.0, vert_gap=0.2, vert_loc=0, xcenter=0.5, pos=None, parent=None):
        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))  # This lists all children from the graph directed outward from root
        if parent is not None and parent in children:
            children.remove(parent)  # Only remove parent if it is actually in the list
        if children:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width=width, vert_gap=vert_gap, vert_loc=vert_loc, xcenter=xcenter)

def draw_minimax_tree():
    """Visualize the Minimax decision tree for Tic Tac Toe using matplotlib and networkx."""
    board = [[" " for _ in range(3)] for _ in range(3)]
    G = nx.DiGraph()
    root_node = board_to_string(board)  # Capture the root node for positioning
    minimax_graph(board, 0, True, "X", "O", G, root_node)
    pos = hierarchy_pos(G, root=root_node)  # Use custom hierarchical positioning
    plt.figure(figsize=(12, 12))
    nx.draw(G, pos, with_labels=True, node_size=2500, node_color='lightblue', font_size=8, arrows=True)
    plt.title('Minimax Decision Tree')
    plt.show()

#AI vs AI play with MiniMax algorithm
ai_vs_ai()

# This function calls `minimax_graph`, a function that generates a visualization of the decision tree for Tic Tac Toe using the Minimax algorithm.
# It includes a `max_depth` parameter that limits the depth of recursion to control the complexity and computational load. 
# Note: The number of nodes grows quickly with increasing depth. For a depth `d`, the number of possible nodes can be approximated as 9! / (9-d)!.
# This growth indicates that even small increases in depth can lead to a large increase in the number of nodes, affecting performance.
draw_minimax_tree()
