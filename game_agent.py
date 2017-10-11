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

def diff_in_moves(game, player):
    difference = float(len(game.get_legal_moves(game._player_1)) - len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def aggressive_diff_in_moves(game, player):
    difference = float(0.8*len(game.get_legal_moves(game._player_1)) - 1.2*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def passive_diff_in_moves(game, player):
    difference = float(1.2*len(game.get_legal_moves(game._player_1)) - 0.8*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def slightly_aggressive_diff_in_moves(game, player):
    difference = float(0.9*len(game.get_legal_moves(game._player_1)) - 1.1*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def slightly_passive_diff_in_moves(game, player):
    difference = float(1.1*len(game.get_legal_moves(game._player_1)) - 0.9*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def very_passive_diff_in_moves(game, player):
    difference = float(1.2*len(game.get_legal_moves(game._player_1)) - 0.8*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

def very_aggressive_diff_in_moves(game, player):
    difference = float(1.5*len(game.get_legal_moves(game._player_1)) - 0.5*len(game.get_legal_moves(game._player_2)))
    if player == game._player_1:
        return -difference
    else:
        return difference

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
    def __init__(self, search_depth=1, score_fn=custom_score, timeout=15.):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout


class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """

    def __init__(self, score_fn, search_depth=1, timeout=10.0):
        super().__init__(score_fn=score_fn, search_depth=search_depth, timeout=timeout)
        self.__name__ = 'Minimax with {}'.format(score_fn.__name__)

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

        best_move=None
        try:
            depth = self.search_depth # Initialize the starting depth
            while True:
                best_move = self.minimax(game, depth) # Calculate the best move
                depth += 1 # Search deeper
        except SearchTimeout:
            pass # when we're out of time, just return the move from the last interation of minimax
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
        
        max_value = -float('inf')
        best_move = (-1,-1)
        for move in game.get_legal_moves(): # Go through all the possible moves for this player
            prediction_board = game.forecast_move(move) # Generate a copy of the board with that move applied
            predicted_value = self.min_value(prediction_board, depth-1) # Calculate the likely return from an opponent minimizing our objective function
            # Check and keep track of the best move
            if predicted_value >= max_value:
                best_move = move
                max_value = predicted_value
        return best_move
        
    def min_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD: # Throw SearchTimeout if out of time
            raise SearchTimeout

        if game_over(game):
            return game.utility(self) # If the game pass is over, return whether we won or not

        if depth <= 0:
            return self.score(game, self) # If the depth is met, don't search any further
        
        minimum_value = float('inf')
        for move in game.get_legal_moves(): # Go through all the moves available to the minimizing player
            predicted_board = game.forecast_move(move) # Apply each move to a copy of the gameboard
            predicted_value = self.max_value(predicted_board, depth-1) # Calculate the likely return from a maximizing player
            minimum_value = min(predicted_value, minimum_value) # Save the minimum so far
        return minimum_value

    def max_value(self, game, depth):
        if self.time_left() < self.TIMER_THRESHOLD: # Throw SearchTimeout if out of time
            raise SearchTimeout
        
        if game_over(game):
            return game.utility(self) # If the game if over, return where we won or not

        if depth <= 0:
            return self.score(game, self) # If the depth is met, don't search any further

        maximum_value = -float('inf')
        for move in game.get_legal_moves(): # Go through all the moves available to the maximizing player
            predicted_board = game.forecast_move(move) # Apply each move to a copy of the gameboard
            predicted_value = self.min_value(predicted_board, depth-1) # Calculate the likely return from a minimizing player
            maximum_value = max(predicted_value, maximum_value) # Save the maimum found so far
        return maximum_value

def game_over(game):
    if len(game.get_legal_moves())==0:
        return True
    else:
        return False

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """
    def __init__(self, score_fn, search_depth=1, timeout=10.0):
        super().__init__(score_fn=score_fn, search_depth=search_depth, timeout=timeout)
        self.__name__ = 'Alphabeta pruner with {}'.format(score_fn.__name__)

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

        best_move = None
        try:
            depth = self.search_depth # Start the search at search_depth
            while True:
                _, best_move = self.max_value(game, time_left, depth) # Get the max value from the current gameboard
                depth = depth + 1 # Search deeper
        except SearchTimeout:
            pass # when we timeout, just return the move found on the last iteration
        return best_move

    def max_value(self, game, time_left, depth, alpha=-float('inf'), beta=float('inf')):
        if time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout # raise timeout if out out time

        if game_over(game):
            return game.utility(self), None # If the game is over, return whether we won on this branch or not

        if depth <= 0:
            return self.score(game, self), None  # If the depth is met, return the score of the current board

        best_move = (-1,-1)
        max_utility = -float('inf')
        for move in game.get_legal_moves(): # Iterate over all the possible moves for the maximizing player
            game_copy = game.forecast_move(move) # Apply each move to a copy of the gameboard
            predicted_value, _ = self.min_value(game_copy, time_left, depth-1, alpha, beta) # Calculate the likely value from a player minimizing our objective function after applying this move
            
            # Save the best move so far
            if predicted_value >= max_utility:
                max_utility = predicted_value
                best_move = move

            # Prune this branch if the max_utility is more that the upper limit (ie: beta)
            if max_utility >= beta:
                return max_utility, best_move

            # Set the lower bound for sibling and child branches ("You branches better be at least this good, or I'm not choosing you" - max_value)
            alpha = max(predicted_value, alpha)
        return max_utility, best_move

    def min_value(self, game, time_left, depth, alpha=-float('inf'), beta=float('inf')):
        if time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout # raise a timeout if we're out of time
        
        if game_over(game):
            return game.utility(self), None # If the game is over, return whether we won or not

        if depth <= 0:
            return self.score(game, self), None # If the depth is met, return the objective function applied to the game board

        best_move = (-1,-1)
        min_utility = float('inf')
        for move in game.get_legal_moves(): # Iterate through all the moves avaiable to the minimizing player
            game_copy = game.forecast_move(move) # Apply each move to a copy of the game board
            predicted_value, _ = self.max_value(game_copy, time_left, depth-1, alpha, beta) # Caluculate the likely value from a player maximizing our objecttive function after applying this move
            
            # Keep track of the least value found so far
            if predicted_value <= min_utility:
                min_utility = predicted_value
                best_move = move

            # Prune this branch if the min_value is lower than our lower bound
            if min_utility <= alpha:
                return min_utility, best_move

            # Set the upper bound for sibling and child branches ("You branches can't be better than this because I'll never pick you" - min_value)
            beta = min(predicted_value, beta)
        return min_utility, best_move
