"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""
from datetime import datetime

import unittest

import isolation
from game_agent import SearchTimeout
import game_agent
from utils import *

from importlib import reload
import time

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayer(score_fn=game_agent.stupid_score)
        self.player2 = game_agent.MinimaxPlayer(score_fn=game_agent.stupid_score)

        self.game = isolation.Board(self.player1, self.player2)
    
    def tearDown(self):
        time_left(True)

    def test_time_left_start_and_stop(self):
        self.assertLessEqual(time_left(), 150)
        
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49.5)
        self.assertEqual(time_left(True), None)

    def test_time_left_start_and_stop_and_start(self):
        self.assertLessEqual(time_left(), 150)
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49.5)
        self.assertEqual(time_left(True), None)

        self.assertLessEqual(time_left(), 150)
        time.sleep(.1)
        stamp = time_left()
        self.assertLessEqual(stamp, 50)
        self.assertGreater(stamp, 49.5)

    def test_stupid_scoring(self):
        self.assertEqual(self.player1.score(self.game, self.player1), 49)
        self.assertEqual(self.player2.score(self.game, self.player2), 49)
    
    def test_depth_of_one(self):
        self.player1.search_depth=1
        self.player2.search_depth=1

        move = self.player1.get_move(game=self.game, time_left=time_left)
        self.assertEqual(move, (2,2))

        self.game.apply_move(move)

        move = self.player2.get_move(game=self.game, time_left=time_left)
        self.assertEqual(move, (3,2))
    
    def test_timer_stops_after_get_move(self):
        self.player1.get_move(game=self.game, time_left=time_left)
        self.assertAlmostEqual(time_left(), 150, 1)

class BastardTest(unittest.TestCase):
    def setUp(self):
        reload(game_agent)
        self.player1 = game_agent.MinimaxPlayerTroll(score_fn=game_agent.stupid_score)
        self.player2 = game_agent.MinimaxPlayerTroll(score_fn=game_agent.stupid_score)

        self.game = isolation.Board(self.player1,self.player2, 3, 3)
    
    def test_best_move_is_middle(self):
        self.assertEqual(self.player1.get_move(self.game, time_left), (1,1))

        
if __name__ == '__main__':
    unittest.main()
