from database_utils import *
from isolation.isolation import Board
import game_agent
from game_agent import *
import sample_players
import sys

if len(sys.argv) >= 2:
    amount_of_games = int(sys.argv[1])
else:
    amount_of_games = 100

print('#### custom_score_1 benchmark ####')

player1 = game_agent.AlphaBetaPlayer(score_fn=most_moves_for_player)
player2 = game_agent.MinimaxPlayer(score_fn=most_moves_for_player)
record = [0,0]
reasons_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
for _ in range(amount_of_games):
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
print("Lost because of timeout {} \nLost because of forfeit {} \nLost because of illegal move: {}\n".format(
        reasons_lost["timeout"],
        reasons_lost["forfeit"],
        reasons_lost["illegal move"])
    )

# Save results in database
match_history = select_match("most_moves_for_player_score_ab", "least_moves_for_ther_player_mm")
if len(match_history):
    match_history = match_history[0][2:4]
else:
    insert_into_table(values=("most_moves_for_player_score_ab", "least_moves_for_ther_player_mm", 0, 0))
    match_history = (0,0)
new_match_history = (match_history[0]+record[0], match_history[1]+record[1])
update_table(new_match_history[0], new_match_history[1], "most_moves_for_player_score_ab", "least_moves_for_ther_player_mm")

DEBUG = False
if DEBUG:
    print("DEBUG:\t\told record pulled from db {}\n\t\tnew record pulled from db {}\n".format(match_history, select_match("most_moves_for_player_score_ab", "least_moves_for_ther_player_mm")[0][2:4]))
print("The historical match history between most_moves_for_player_score_ab and least_moves_for_ther_player_mm: {}\n\n\n".format(new_match_history))

print('#### least_moves_for_other_player_score_ab benchmark ####\n\n')

player1 = game_agent.AlphaBetaPlayer(score_fn=least_moves_for_other_player)
player2 = game_agent.MinimaxPlayer(score_fn=least_moves_for_other_player)
record = [0,0]
reasons_lost = {"timeout": 0, "forfeit": 0, "illegal move": 0}
for _ in range(amount_of_games):
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
match_history = select_match("least_moves_for_other_player_ab", "least_moves_for_ther_player_mm")
if len(match_history):
    match_history = match_history[0][2:4]
else:
    insert_into_table(values=("least_moves_for_other_player_ab", "least_moves_for_ther_player_mm", 0, 0))
    match_history = (0,0)
new_match_history = (match_history[0]+record[0], match_history[1]+record[1])
update_table(new_match_history[0], new_match_history[1], "least_moves_for_other_player_ab", "least_moves_for_ther_player_mm")

if DEBUG:
    print("DEBUG:\t\told record pulled from db {}\n\t\tnew record pulled from db {}\n".format(match_history, select_match("least_moves_for_other_player_ab", "least_moves_for_ther_player_mm")[0][2:4]))
print("The historical match history between least_moves_for_other_player_ab and least_moves_for_ther_player_mm: {}\n\n\n".format(new_match_history))