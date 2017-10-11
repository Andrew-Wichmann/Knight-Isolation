from database_utils import *
from isolation.isolation import Board
from game_agent import *
import sample_players
import sys

if len(sys.argv) >= 2:
    amount_of_games = int(sys.argv[1])
else:
    amount_of_games = 100

def run_benchmark(player1, player2, num_of_games):
    print('#### {} vs {} benchmark ####\n\n'.format(player1.__name__, player2.__name__))

    record = [0,0]
    reasons_p1_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
    reasons_p2_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
    for _ in range(num_of_games):
        game = Board(player1, player2)
        winner, _, reason = game.play()
        if winner == player1:
            record[0] = record[0]+1
            if reason == "timeout":
                reasons_p2_lost["timeout"] += 1
            elif reason == "forfeit":
                reasons_p2_lost["forfeit"] += 1
            elif reason == "illegal move":
                reasons_p2_lost["illegal move"] += 1
        else:
            record[1] = record[1]+1
            if reason == "timeout":
                reasons_p1_lost["timeout"] += 1
            elif reason == "forfeit":
                reasons_p1_lost["forfeit"] += 1
            elif reason == "illegal move":
                reasons_p1_lost["illegal move"] += 1

    print("{} wins: {} \n{} wins: {}\n\n".format(
        player1.__name__,
        record[0],
        player2.__name__,
        record[1])
    )
    print("{}\nLost because of timeout {} \nLost because of forfeit {} \nLost because of illegal move: {}\n".format(
            player1.__name__,
            reasons_p1_lost["timeout"],
            reasons_p1_lost["forfeit"],
            reasons_p1_lost["illegal move"])
        )
    print("{}\nLost because of timeout {} \nLost because of forfeit {} \nLost because of illegal move: {}\n".format(
            player2.__name__,
            reasons_p2_lost["timeout"],
            reasons_p2_lost["forfeit"],
            reasons_p2_lost["illegal move"])
        )

    # Save results in database
    match_history = select_match(player1.__name__, player2.__name__)
    if len(match_history):
        match_history = match_history[0][2:4]
    else:
        insert_into_table(values=(player1.__name__, player2.__name__, 0, 0))
        match_history = (0,0)
    new_match_history = (match_history[0]+record[0], match_history[1]+record[1])
    update_table(new_match_history[0], new_match_history[1], player1.__name__, player2.__name__)

    print("The historical match history between {} and {}: {}\n\n\n".format(player1.__name__, player2.__name__, new_match_history))

mm1 = MinimaxPlayer(score_fn = most_moves_for_player)
ab1 = AlphaBetaPlayer(score_fn = most_moves_for_player)

mm2 = MinimaxPlayer(score_fn = least_moves_for_other_player)
ab2 = AlphaBetaPlayer(score_fn = least_moves_for_other_player)

mm3 = MinimaxPlayer(score_fn = diff_in_moves)
ab3 = AlphaBetaPlayer(score_fn = diff_in_moves)

mm4 = MinimaxPlayer(score_fn = aggressive_diff_in_moves)
ab4 = AlphaBetaPlayer(score_fn = aggressive_diff_in_moves)

mm5 = MinimaxPlayer(score_fn = slightly_aggressive_diff_in_moves)
ab5 = AlphaBetaPlayer(score_fn = slightly_aggressive_diff_in_moves)

mm6 = MinimaxPlayer(score_fn = very_aggressive_diff_in_moves)
ab6 = AlphaBetaPlayer(score_fn = very_aggressive_diff_in_moves)

mm7 = MinimaxPlayer(score_fn = passive_diff_in_moves)
ab7 = AlphaBetaPlayer(score_fn = passive_diff_in_moves)

mm8 = MinimaxPlayer(score_fn = slightly_passive_diff_in_moves)
ab8 = AlphaBetaPlayer(score_fn = slightly_passive_diff_in_moves)

mm9 = MinimaxPlayer(score_fn = very_passive_diff_in_moves)
ab9 = AlphaBetaPlayer(score_fn = very_passive_diff_in_moves)

greedy = sample_players.GreedyPlayer()

run_benchmark(mm1, greedy, amount_of_games)
run_benchmark(mm2, greedy, amount_of_games)
run_benchmark(mm3, greedy, amount_of_games)
run_benchmark(mm4, greedy, amount_of_games)
run_benchmark(mm5, greedy, amount_of_games)
run_benchmark(mm6, greedy, amount_of_games)
run_benchmark(mm7, greedy, amount_of_games)
run_benchmark(mm8, greedy, amount_of_games)
run_benchmark(mm9, greedy, amount_of_games)

run_benchmark(ab1, greedy, amount_of_games)
run_benchmark(ab2, greedy, amount_of_games)
run_benchmark(ab3, greedy, amount_of_games)
run_benchmark(ab4, greedy, amount_of_games)
run_benchmark(ab5, greedy, amount_of_games)
run_benchmark(ab6, greedy, amount_of_games)
run_benchmark(ab7, greedy, amount_of_games)
run_benchmark(ab8, greedy, amount_of_games)
run_benchmark(ab9, greedy, amount_of_games)
