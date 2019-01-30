"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the player class hierarchy.
"""

import random
from typing import Optional
import pygame
from renderer import Renderer
from block import Block
from goal import Goal

TIME_DELAY = 600


class Player:
    """A player in the Blocky game.

    This is an abstract class. Only child classes should be instantiated.

    === Public Attributes ===
    renderer:
        The object that draws our Blocky board on the screen
        and tracks user interactions with the Blocky board.
    id:
        This player's number.  Used by the renderer to refer to the player,
        for example as "Player 2"
    goal:
        This player's assigned goal for the game.
    """
    renderer: Renderer
    id: int
    goal: Goal

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """ Initialize this Player.
        """
        self.goal = goal
        self.renderer = renderer
        self.id = player_id

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.
        """
        raise NotImplementedError


class SmartPlayer(Player):
    """ A smart player that searches through many random moves and picks the
    best scoring scenario. This player is runned by the computer.
    The amount of ramdom scenarios that this player will look through depends
    on the difficulty attributed to itself.
    These are the amount of moves that this player will consider, according to
    it's difficulty level:
    level | scenarios
    0     |  5
    1     |  10
    2     |  25
    3     |  50
    4     |  100
    >=5   |  150
    """
    difficulty: int
    _number_of_scenarios: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal,
                 difficulty: int) -> None:
        """ Initialize this SmartPlayer.
        """

        # We also call on the abstract parent class to initialize common
        # attributes.
        super().__init__(renderer, player_id, goal)

        # Set the difficulty level.
        self.difficulty = difficulty

        # Set the number of scenarios this player uses do make its decision
        # (look to the class docstring for more details).
        if difficulty > 5:
            difficulty = 5
        self._number_of_scenarios = {0: 5, 1: 10, 2: 25, 3: 50, 4: 100,
                                     5: 150}[difficulty]

    def make_move(self, board: Block) -> int:
        """ Make a smart move, which is based on the difficulty level. The
        difficulty level is the amount of random scenarios this player will
        analyse before chosing the best of it.
        """

        # Generates the determined number of random scenarios and saves the
        # best case index.
        # scenarios list will store a tuple containing (<chosen block>,
        # <chosen move>, <points>)
        scenarios = []
        best_score = 0
        best_scenario_index = 0
        for scenario_number in range(self._number_of_scenarios):
            # Selects a random candidate block
            possible_block = random_block_choice(board)

            # Makes a random temporary move (no smash allowed)
            random_index = random.randint(1, 4)
            move_choice(possible_block, random_index)

            # Calculates the amount of points that this move would take to
            temporary_score = self.goal.score(board)
            if best_score < temporary_score:
                best_score = temporary_score
                best_scenario_index = scenario_number

            # Undo the temporary move
            move_choice(possible_block, -random_index)

            # Stores this move as a possible scenario
            scenarios.append((possible_block, random_index, temporary_score))

        # Makes the best move: highlight the selected block, take some delay,
        # makes the move and unhihlight the block.
        # - gets the best move information (corresp. block and move to be made)
        selected_block = scenarios[best_scenario_index][0]
        move_index = scenarios[best_scenario_index][1]
        # - visual changes (highlighting and updating on screen) + delay
        selected_block.highlighted = True
        self.renderer.draw(board, self.id)
        pygame.time.wait(TIME_DELAY)
        # - makes the move
        move_choice(selected_block, move_index)
        # - visual changes (unhighlighting and screen update)
        selected_block.highlighted = False
        self.renderer.draw(board, self.id)

        # Checks whether the user tried to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

        # Successful completion of the move
        return 0


class RandomPlayer(Player):
    """ A random player that is runned by the computer and does random moves.
    """

    def make_move(self, board: Block) -> int:
        """ Makes the random move to a random block.
        """

        # Selects a random block, highlight it and updates it on screen
        selected_block = random_block_choice(board)
        selected_block.highlighted = True
        self.renderer.draw(board, self.id)

        # Some delay so the user can perceive what is happening
        pygame.time.wait(TIME_DELAY)

        # Gets a random move
        random_index = random.randint(0, 4)
        move_choice(selected_block, random_index)

        # Unhighlight the selected block and updates it on screen
        selected_block.highlighted = False
        self.renderer.draw(board, self.id)

        # Checks whether the user tried to close the window
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return 1

        # Successful completion of the move
        return 0


class HumanPlayer(Player):
    """A human player.

    A HumanPlayer can do a limited number of smashes.

    === Public Attributes ===
    num_smashes:
        number of smashes which this HumanPlayer has performed
    === Representation Invariants ===
    num_smashes >= 0
    """
    # === Private Attributes ===
    # _selected_block
    #     The Block that the user has most recently selected for action;
    #     changes upon movement of the cursor and use of arrow keys
    #     to select desired level.
    # _level:
    #     The level of the Block that the user selected
    #
    # == Representation Invariants concerning the private attributes ==
    #     _level >= 0

    # The total number of 'smash' moves a HumanPlayer can make during a game.
    MAX_SMASHES = 1

    num_smashes: int
    _selected_block: Optional[Block]
    _level: int

    def __init__(self, renderer: Renderer, player_id: int, goal: Goal) -> None:
        """Initialize this HumanPlayer with the given <renderer>, <player_id>
        and <goal>.
        """
        super().__init__(renderer, player_id, goal)
        self.num_smashes = 0

        # This HumanPlayer has done no smashes yet.
        # This HumanPlayer has not yet selected a block, so set _level to 0
        # and _selected_block to None.
        self._level = 0
        self._selected_block = None

    def process_event(self, board: Block,
                      event: pygame.event.Event) -> Optional[int]:
        """Process the given pygame <event>.

        Identify the selected block and mark it as highlighted.  Then identify
        what it is that <event> indicates needs to happen to <board>
        and do it.

        Return
           - None if <event> was not a board-changing move (that is, if was
             a change in cursor position, or a change in _level made via
            the arrow keys),
           - 1 if <event> was a successful move, and
           - 0 if <event> was an unsuccessful move (for example in the case of
             trying to smash in an invalid location or when the player is not
             allowed further smashes).
        """
        # Get the new "selected" block from the position of the cursor
        block = board.get_selected_block(pygame.mouse.get_pos(), self._level)

        # Remove the highlighting from the old "_selected_block"
        # before highlighting the new one
        if self._selected_block is not None:
            self._selected_block.highlighted = False
        self._selected_block = block
        self._selected_block.highlighted = True

        # Since get_selected_block may have not returned the block at
        # the requested level (due to the level being too low in the tree),
        # set the _level attribute to reflect the level of the block which
        # was actually returned.
        self._level = block.level

        if event.type == pygame.MOUSEBUTTONDOWN:
            block.rotate(event.button)
            return 1
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if block.parent is not None:
                    self._level -= 1
                return None

            elif event.key == pygame.K_DOWN:
                if len(block.children) != 0:
                    self._level += 1
                return None

            elif event.key == pygame.K_h:
                block.swap(0)
                return 1

            elif event.key == pygame.K_v:
                block.swap(1)
                return 1

            elif event.key == pygame.K_s:
                if self.num_smashes >= self.MAX_SMASHES:
                    print('Can\'t smash again!')
                    return 0
                if block.smash():
                    self.num_smashes += 1
                    return 1
                else:
                    print('Tried to smash at an invalid depth!')
                    return 0

    def make_move(self, board: Block) -> int:
        """Choose a move to make on the given board, and apply it, mutating
        the Board as appropriate.

        Return 0 upon successful completion of a move, and 1 upon a QUIT event.

        This method will hold focus until a valid move is performed.
        """
        self._level = 0
        self._selected_block = board

        # Remove all previous events from the queue in case the other players
        # have added events to the queue accidentally.
        pygame.event.clear()

        # Keep checking the moves performed by the player until a valid move
        # has been completed. Draw the board on every loop to draw the
        # selected block properly on screen.
        while True:
            self.renderer.draw(board, self.id)
            # loop through all of the events within the event queue
            # (all pending events from the user input)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return 1

                result = self.process_event(board, event)
                self.renderer.draw(board, self.id)
                if result is not None and result > 0:
                    # un-highlight the selected block
                    self._selected_block.highlighted = False
                    return 0


def random_block_choice(board: Block) -> Block:
    """ A helper function for the SmartPlayer and RandomPlayer classes.
    It will randomly choose a block.
    """

    # We define the coordinates randomly
    x_random_coordinate = random.randint(0, board.size)
    y_random_coordinate = random.randint(0, board.size)
    random_coordinates = (x_random_coordinate, y_random_coordinate)
    # We also use a random level
    random_level = random.randint(0, board.max_depth)

    # With the random attributes, we can return a random block.
    return board.get_selected_block(random_coordinates, random_level)


def move_choice(block: Block, choice_index: int) -> None:
    """ A helper function for RandomPlayer and SmartPlayer. choice_index will
    vary from -4 to 4.
    Inputing a negative number will undo the corresponding move, accoring to
    its opposite. Possible moves are smash (0), rotate (clockwise and
    counterclockwise) (1 and 3), swap (vertically and horizontally) (3 and 4).
    """

    if choice_index == 0:
        block.smash()
    elif choice_index == 1 or choice_index == -2:
        block.rotate(1)
    elif choice_index == 2 or choice_index == -1:
        block.rotate(3)
    elif choice_index == 3 or choice_index == -3:
        block.swap(1)
    elif choice_index == 4 or choice_index == -4:
        block.swap(0)


if __name__ == '__main__':
    import python_ta
    python_ta.check_all(config={
        'allowed-io': ['process_event'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer',
            'pygame'
        ],
        'max-attributes': 10,
        'generated-members': 'pygame.*'
    })
