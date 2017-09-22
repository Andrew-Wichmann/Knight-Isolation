from isolation import *
import sample_players
player1 = sample_players.HumanPlayer()
player2 = sample_players.GreedyPlayer()
while True:
    game = Board(player1, player2)
    game.play(time_limit=99999)
    if game.is_winner(player1):
        print('You won!')
    else:
        print('The computer won. Get used to it.')