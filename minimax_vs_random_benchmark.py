from isolation.isolation import Board
import game_agent
import sample_players
player1 = game_agent.MinimaxPlayer()
player2 = sample_players.RandomPlayer()
record = [0,0]
amount_of_games = 250
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
