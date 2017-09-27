from isolation.isolation import HackedBoard
import sample_players
player1 = sample_players.HumanPlayer()
player2 = sample_players.GreedyPlayer()
while True:
    game = HackedBoard(player1, player2)
    winner, _, reason = game.play()
    if winner == player1:
        print('You won! Because: ' + reason)
    else:
        print('The computer won because ' + reason + '. Get used to it.')