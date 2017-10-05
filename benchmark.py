from database_utils import *
from isolation.isolation import Board
from game_agent import *
import sample_players
import sys

if len(sys.argv) >= 2:
    amount_of_games = int(sys.argv[1])
else:
    amount_of_games = 100

def run_benchmark(num_of_games=100, score=most_moves_for_player, algorithm='mm'):
    print('#### {}_{} benchmark ####\n\n'.format(score.__name__, algorithm))

    if algorithm == 'mm':
        player1 = MinimaxPlayer(score_fn=score)
    elif algorithm == 'ab':
        player1 = AlphaBetaPlayer(score_fn=score)
    player2 = sample_players.GreedyPlayer()
    record = [0,0]
    reasons_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
    for _ in range(num_of_games):
        game = Board(player1, player2)
        winner, _, reason = game.play()
        if winner == player1:
            record[0] = record[0]+1
        else:
            record[1] = record[1]+1
            if reason == "timeout":
                reasons_lost["timeout"] += 1
            elif reason == "forfeit":
                reasons_lost["forfeit"] += 1
            elif reason == "illegal move":
                reasons_lost["illegal move"] += 1
            else:
                print('ya don\' fucked up')
                raise Exception
    print("Wins: {} \nLosses: {}\nW/L Ratio: {}\n\n".format(record[0],record[1],record[0]/amount_of_games))
    print("Lost because of timeout {} \nLost because of forfeit {} \nLost because of illegal move: {}".format(
            reasons_lost["timeout"],
            reasons_lost["forfeit"],
            reasons_lost["illegal move"])
        )

    # Save results in database
    match_history = select_match("{}_{}".format(score.__name__, algorithm), "greedy")
    if len(match_history):
        match_history = match_history[0][2:4]
    else:
        insert_into_table(values=("{}_{}".format(score.__name__, algorithm), "greedy", 0, 0))
        match_history = (0,0)
    new_match_history = (match_history[0]+record[0], match_history[1]+record[1])
    update_table(new_match_history[0], new_match_history[1], "{}_{}".format(score.__name__, algorithm), "greedy")

    print("The historical match history between {}_{} and greedy: {}\n\n\n".format(score.__name__, algorithm, new_match_history))

run_benchmark(score=most_moves_for_player, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=least_moves_for_other_player, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=aggressive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=passive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=slightly_passive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=very_passive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=slightly_aggressive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)
run_benchmark(score=very_aggressive_diff_in_moves, algorithm='mm', num_of_games=amount_of_games)

run_benchmark(score=most_moves_for_player, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=least_moves_for_other_player, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=aggressive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=passive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=slightly_passive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=very_passive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=slightly_aggressive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)
run_benchmark(score=very_aggressive_diff_in_moves, algorithm='ab', num_of_games=amount_of_games)

def run_benchmark2(player1, player2, num_of_games):
    print('#### {} vs {} benchmark ####\n\n'.format(player1.__name__, player2.__name__))

    record = [0,0]
    reasons_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
    for _ in range(num_of_games):
        game = Board(player1, player2)
        winner, _, reason = game.play()
        if winner == player1:
            record[0] = record[0]+1
        else:
            record[1] = record[1]+1
            if reason == "timeout":
                reasons_lost["timeout"] += 1
            elif reason == "forfeit":
                reasons_lost["forfeit"] += 1
            elif reason == "illegal move":
                reasons_lost["illegal move"] += 1
            else:
                print('ya don\' fucked up')
                raise Exception
    print("Wins: {} \nLosses: {}\nW/L Ratio: {}\n\n".format(record[0],record[1],record[0]/amount_of_games))
    print("Lost because of timeout {} \nLost because of forfeit {} \nLost because of illegal move: {}".format(
            reasons_lost["timeout"],
            reasons_lost["forfeit"],
            reasons_lost["illegal move"])
        )

    # Save results in database
    match_history = select_match("{}_{}".format(player1.__name__, player2.__name__), "greedy")
    if len(match_history):
        match_history = match_history[0][2:4]
    else:
        insert_into_table(values=(player1.__name__, player2.__name__, 0, 0))
        match_history = (0,0)
    new_match_history = (match_history[0]+record[0], match_history[1]+record[1])
    update_table(new_match_history[0], new_match_history[1], player1.__name__, player2.__name__)

    print("The historical match history between {}_{} and greedy: {}\n\n\n".format(player1.__name__, player2.__name__, new_match_history))

# mm = MinimaxPlayer(score_fn = diff_in_moves)
# ab = AlphaBetaPlayer(score_fn = diff_in_moves)
# run_benchmark2(mm, ab, amount_of_games)
