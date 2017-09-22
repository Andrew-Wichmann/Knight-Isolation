"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""
from datetime import datetime

import unittest

import isolation
import game_agent

from importlib import reload
import time

start_time = None
def time_left(stop=False):
    global start_time
    if stop:
        start_time = None
        return

    if start_time is None:
        start_time = datetime.now().microsecond/1000 +  1000*datetime.now().second
    current_time = datetime.now().microsecond/1000 +  1000*datetime.now().second
    return isolation.isolation.TIME_LIMIT_MILLIS - (current_time - start_time)

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer()
        self.player2 = game_agent.MinimaxPlayer()

        self.game = isolation.Board(self.player1, self.player2)
    
    def tearDown(self):
        time_left(True)

    def test_time_left_start_and_stop(self):
        self.assertLessEqual(time_left(), 150)
        
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49)
        self.assertEqual(time_left(True), None)

    def test_time_left_start_and_stop_and_start(self):
        self.assertLessEqual(time_left(), 150)
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49)
        self.assertEqual(time_left(True), None)


        self.assertLessEqual(time_left(), 150)
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49)

    def test_stupid_scoring(self):
        self.player1.score = game_agent.stupid_score
        self.player2.score = game_agent.stupid_score
        self.assertEqual(self.player1.score(self.game, self.player1), 49)
        self.assertEqual(self.player2.score(self.game, self.player2), 49)
    
    def test_depth_of_one(self):
        self.player1.score = game_agent.stupid_score
        self.player2.score = game_agent.stupid_score
        self.player1.search_depth=1
        self.player2.search_depth=1

        move = self.player1.get_move(game=self.game, time_left=time_left)
        self.assertEqual(move, self.game.get_legal_moves(self.player1)[0])

        move = self.player2.get_move(game=self.game, time_left=time_left)
        self.assertEqual(move, self.game.get_legal_moves(self.player1)[0])

        
if __name__ == '__main__':
    unittest.main()
