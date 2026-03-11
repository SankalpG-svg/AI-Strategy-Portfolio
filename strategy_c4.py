import copy
import random
import hashlib

class Strategy:
    @staticmethod
    def random_strategy(game, letter):
        return random.choice(game.available_moves())

    @staticmethod
    def first_available_strategy(game, letter):
        return game.available_moves()[0]

    @staticmethod
    def medium_strategy(game, letter):
        for move in game.available_moves():
            board = copy.deepcopy(game)
            if board.make_move(move, letter):
                if board.current_winner == letter:
                    return move
        return random.choice(game.available_moves())

    @staticmethod
    def hard_strategy(game, letter):
        opponent = 'O' if letter == 'X' else 'X'
        for move in game.available_moves():
            board = copy.deepcopy(game)
            if board.make_move(move, letter):
                if board.current_winner == letter:
                    return move
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            f = True
            for move in board.available_moves():
                board1 = copy.deepcopy(board)
                if board1.make_move(move, opponent):
                    if board1.current_winner == opponent:
                        f =False
                        break
            if f:
                return move    
        return random.choice(game.available_moves())
    @staticmethod
    def sankalp_2(game, letter):
        opponent = 'O' if letter == 'X' else 'X'
        move=0
        l=len(game.available_moves())
        t=0
        if l==9:
            return 0
        if l==1:
            return random.choice(game.available_moves())
        k=0
        if l==8:
            p=True
            
            for move in game.available_moves():
                if move ==4:
                    p=False
                    break
            if p==False:
                return 4 
            else:    
               return random.choice([0,2,6,8])


            
        if l==7:
            for move in game.available_moves():
                if move%4==0 or move%8==0:
                    return move            

        for move in game.available_moves():
                    board3 = copy.deepcopy(game)
                    if board3.make_move(move, letter):
                        if board3.current_winner == letter:
                           return move

        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            f = True
            for move in board.available_moves():
                board1 = copy.deepcopy(board)
                if board1.make_move(move, opponent):
                    if board1.current_winner == opponent:
                        return move
                        f =False
                        break
        if f:

                for move1 in game.available_moves():
                    board = copy.deepcopy(game)
                    board.make_move(move1, letter)
                    for move in board.available_moves():
                        board2 = copy.deepcopy(board)
                        if board2.make_move(move, letter):
                            if board2.current_winner == letter:
                                
                            
                               return move1
                               break
                            else:
                                pass
                               
        return random.choice(game.available_moves())
       
        if not opponent_can_win:
            return move1
    
        return random.choice(game.available_moves())
    @staticmethod
    def sankalp_3(game, letter):
        losing_moves = set()
        def play_and_learn(game, letter, num_games=1000):
            opponent = 'O' if letter == 'X' else 'X'
            for _ in range(num_games):
               game_copy = copy.deepcopy(game)
               play_game(game_copy, letter, opponent)
        def play_game( game, letter, opponent):
            move_history = []
            while game.empty_squares():
                move = choose_move(game, letter)
                move_history.append((move, letter))
                game.make_move(move, letter)
                if game.current_winner:
                    if game.current_winner == opponent:
                       record_losing_moves(move_history, opponent)
                    break
                letter = opponent if letter == 'X' else 'X'
        def choose_move(game, letter):
            for move in game.available_moves():
                if (move, letter) not in losing_moves:
                   return move
            return random.choice(game.available_moves())
        def record_losing_moves( move_history, losing_letter):
            for move, letter in move_history:
                if letter == losing_letter:
                    losing_moves.add((move, letter))
        play_and_learn(game, letter)
        return choose_move(game, letter)
    @staticmethod
    def manual_strategy(game, letter):
        game.print_board()
        print("\n")        
        while True:
            try:
                move = int(input("Enter your move (0-6): "))
                if move in game.available_moves():
                    return move
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Enter a number between 0 and 6.")
    @staticmethod
    def get_board_id(board):
        board_str = ''.join([''.join(row) for row in board])
        return hashlib.md5(board_str.encode()).hexdigest()
    
    score = dict()
    @staticmethod
    def best_move(game,letter,max_depth):
        def calculate(game,letter,depth):
            if Strategy.score.get(tuple(Strategy.get_board_id(game.board))) is not None:
                return Strategy.score[tuple(Strategy.get_board_id(game.board))]
            if game.current_winner == 'X':
                Strategy.score[tuple(Strategy.get_board_id(game.board))] = 1
                return 1
            if game.current_winner=='O':
                Strategy.score[tuple(Strategy.get_board_id(game.board))] = -1
                return -1
            if len(game.available_moves())==0:
                Strategy.score[tuple(Strategy.get_board_id(game.board))] = 0
                return 0
            if max_depth == depth:
                return 0
            board_t = tuple(Strategy.get_board_id(game.board))
            Strategy.score[board_t] = 0
            if letter == 'X':
                Strategy.score[board_t] = -2
            else:
                Strategy.score[board_t] = 2
            for move in game.available_moves():
                board = copy.deepcopy(game)
                board.make_move(move,letter)
                if letter == 'X':
                    if calculate(board,'O',depth+1) > Strategy.score[board_t]:
                        Strategy.score[board_t] = calculate(board,'O',depth+1)
                else:
                    if calculate(board,'X',depth+1) < Strategy.score[board_t]:
                        Strategy.score[board_t] = calculate(board,'X',depth+1)
            return Strategy.score[board_t]
        
        calculate(game,letter,0)
        
    @staticmethod
    def get_move(game,letter):
        depth = 7
        opponent = 'O' if letter == 'X' else 'X'
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move,letter)
            Strategy.best_move(board,opponent,depth)
        Strategy.best_move(game,letter,depth)
        best_moves = []
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move,letter)
            Strategy.best_move(board,opponent,depth)
            if Strategy.score[tuple(Strategy.get_board_id(board.board))] == Strategy.score[tuple(Strategy.get_board_id(game.board))]:
                best_moves.append(move)
        if len(best_moves) == 0:
            return random.choice(game.available_moves())
        return random.choice(best_moves)
    
    score_cpu = dict()

    @staticmethod
    def best_move_cpu(game, letter):
        def minimax(game, depth, alpha, beta, maximizing_player):
            board_id = Strategy.get_board_id(game.board)
            if board_id in Strategy.score_cpu:
                return Strategy.score_cpu[board_id]

            if game.current_winner == letter:
                return 1
            elif game.current_winner == ('O' if letter == 'X' else 'X'):
                return -1
            elif not game.available_moves() or depth == 0:
                return 0

            if maximizing_player:
                max_eval = float('-inf')
                for move in game.available_moves():
                    board = copy.deepcopy(game)
                    board.make_move(move, letter)
                    eval = minimax(board, depth - 1, alpha, beta, False)
                    max_eval = max(max_eval, eval)
                    alpha = max(alpha, eval)
                    if beta <= alpha:
                        break
                Strategy.score_cpu[board_id] = max_eval
                return max_eval
            else:
                min_eval = float('inf')
                for move in game.available_moves():
                    board = copy.deepcopy(game)
                    board.make_move(move, 'O' if letter == 'X' else 'X')
                    eval = minimax(board, depth - 1, alpha, beta, True)
                    min_eval = min(min_eval, eval)
                    beta = min(beta, eval)
                    if beta <= alpha:
                        break
                Strategy.score_cpu[board_id] = min_eval
                return min_eval

        best_score_cpu = float('-inf')
        best_move = None
        for move in game.available_moves():
            board = copy.deepcopy(game)
            board.make_move(move, letter)
            move_score_cpu = minimax(board, 5, float('-inf'), float('inf'), False)
            if move_score_cpu > best_score_cpu:
                best_score_cpu = move_score_cpu
                best_move = move
        return best_move