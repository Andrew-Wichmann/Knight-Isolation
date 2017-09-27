"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random
import time


class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def most_moves_for_player(game, player):
    return float(len(game.get_legal_moves(player)))

def least_moves_for_other_player(game, player):
    if player == game._player_1:
        return -float(len(game.get_legal_moves(game._player_2)))
    else:
        return -float(len(game.get_legal_moves(game._player_1)))

def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.
    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    return float(len(game.get_legal_moves(player)))


def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    if player == game._player_1:
        return -float(len(game.get_legal_moves(game._player_2)))
    else:
        return -float(len(game.get_legal_moves(game._player_1)))

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    # TODO: finish this function!
    raise NotImplementedError


class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        time_left()

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)
        try:
            while True:
                best_move = self.minimax(game, self.search_depth)
                self.search_depth = self.search_depth + 1
        except SearchTimeout:
            pass
        # Return the best move from the last completed search iteration
        return best_move

    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        max_utility = -float('inf')
        best_move = (-1, -1)
        for move in game.get_legal_moves():         # test all available moves one by one
            prediction = game.forecast_move(move)   # apply the move to a copy of the game state
            predicted_value = self.min_value(prediction, depth-1)   # search the copied game state with the move applied 
            if predicted_value > max_utility:
                # keep track of the best option
                max_utility = predicted_value
                best_move = move
        return best_move

    def min_value(self, game, depth):
        """ Return the minimal utility for the game going no further than depth(?)
        
        Parameters
        ----------
        game : isolation.GameBoard
            An instance of GameBoard representing the current state of the game

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        
        Returns
        -------
        min_utility : int
            Utility represents the best option available at the current game state for the minimizing player

        """

        # Raise exception if we're out of time
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        if depth <= 0:
            return self.score(game, self)

        min_utility = float('inf')
        for move in game.get_legal_moves():
            try:
                prediction = game.forecast_move(move)
                min_utility = min(min_utility, self.max_value(prediction, depth-1))
            except SearchTimeout:
                return min_utility

        return min_utility
    
    def max_value(self, game, depth):
        """ Return the maximum utility for the game going no further than depth(?)
        
        Parameters
        ----------
        game : isolation.GameBoard
            An instance of GameBoard representing the current state of the game

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        
        Returns
        -------
        max_utility : int
            Utility represents the best option available at the current game state for the maximizing player

        """
        
        # Raise exception if we're out of time
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        if depth <= 0:
            return self.score(game, self)

        max_utility = -float('inf')
        for move in game.get_legal_moves():
            try:
                prediction = game.forecast_move(move)
                max_utility = max(max_utility, self.min_value(prediction, depth-1))
            except SearchTimeout:
                return max_utility
            
        return max_utility

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        Modify the get_move() method from the MinimaxPlayer class to implement
        iterative deepening search instead of fixed-depth search.

        **********************************************************************
        NOTE: If time_left() < 0 when this function returns, the agent will
              forfeit the game due to timeout. You must return _before_ the
              timer reaches 0.
        **********************************************************************

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left
        best_move = (-1, -1)
        try:
            while True:
                best_move = self.alphabeta(game, depth=self.search_depth)
                self.search_depth = self.search_depth + 1
        except SearchTimeout:
            pass
        # Return the best move from the last completed search iteration
        return best_move

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()

        if depth <= 0:
            return self.score(game, self)

        max_utility = -float('inf')
        best_move = (-1, -1)
        for move in game.get_legal_moves():         # test all available moves one by one
            prediction = game.forecast_move(move)   # apply the move to a copy of the game state
            predicted_value = self.min_value(prediction, depth-1, alpha, beta)   # search the copied game state with the move applied 
            if predicted_value > max_utility:
                # keep track of the best option
                max_utility = predicted_value
                best_move = move
            alpha = max(max_utility, alpha)
        return best_move
        
    def min_value(self, game, depth, alpha, beta):
        """ Return the minimal utility for the game going no further than depth(?)
        
        Parameters
        ----------
        game : isolation.GameBoard
            An instance of GameBoard representing the current state of the game

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        
        Returns
        -------
        min_utility : int
            Utility represents the best option available at the current game state for the minimizing player

        """

        # Raise exception if we're out of time
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        # if game_over(game):
        #     return game.utility(self)

        if depth <= 0:
            return self.score(game, self)

        min_utility = float('inf')
        for move in game.get_legal_moves():
            try:
                prediction = game.forecast_move(move)
                min_utility = min(min_utility, self.max_value(prediction, depth-1, alpha, beta))
                if min_utility <= alpha:
                    return min_utility
                beta = min(min_utility, beta)
            except SearchTimeout:
                return min_utility

        return min_utility
    
    def max_value(self, game, depth, alpha, beta):
        """ Return the maximum utility for the game going no further than depth(?)
        
        Parameters
        ----------
        game : isolation.GameBoard
            An instance of GameBoard representing the current state of the game

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        
        Returns
        -------
        max_utility : int
            Utility represents the best option available at the current game state for the maximizing player

        """
        
        # Raise exception if we're out of time
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        # if game_over(game):
        #     return game.utility(self)

        if depth <= 0:
            return self.score(game, self)

        max_utility = -float('inf')
        for move in game.get_legal_moves():
            try:
                prediction = game.forecast_move(move)
                max_utility = max(max_utility, self.min_value(prediction, depth-1, alpha, beta))
                if max_utility >= beta:
                    return max_utility
                beta = max(max_utility, alpha)
            except SearchTimeout:
                return max_utility
            
        return max_utility

class MinimaxPlayerBastard(MinimaxPlayer):
    """ This bastard player returns the worst move for itself.
    In a 3x3 board, it's trivial to see the Bastard would pick the middle
    square. Alt name: MinimaxPlayerTroll
    """
    def minimax(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout

        min_utility = float('inf')
        worst_move = (-1, -1)
        for move in game.get_legal_moves():         # test all available moves one by one
            prediction = game.forecast_move(move)   # apply the move to a copy of the game state
            try:
                predicted_value = self.min_value(prediction, depth-1)   # search the game state
                if predicted_value < min_utility:
                    # keep track of the best option
                    min_utility = predicted_value
                    worst_move = move
            except SearchTimeout:
                return worst_move
        return worst_move

class MinimaxPlayerTroll(MinimaxPlayerBastard):
    pass


def game_over(game):
    if not game.get_legal_moves(game._active_player):
        return True
    else:
        return False