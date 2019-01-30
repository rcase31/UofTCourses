"""Assignment 2 - Blocky

=== CSC148 Fall 2017 ===
Diane Horton and David Liu
Department of Computer Science,
University of Toronto


=== Module Description ===

This file contains the Block class, the main data structure used in the game.
"""
from typing import Optional, Tuple, List
import random
import math
from renderer import COLOUR_LIST, TEMPTING_TURQUOISE, BLACK, colour_name

HIGHLIGHT_COLOUR = TEMPTING_TURQUOISE
FRAME_COLOUR = BLACK

# Constants to better identify the children's position
UP_RIGHT = 0
UP_LEFT = 1
LOW_LEFT = 2
LOW_RIGHT = 3
# Other constantans
BIGGEST_SIZE = 750


class Block:
    """A square block in the Blocky game.

    === Public Attributes ===
    position:
        The (x, y) coordinates of the upper left corner of this Block.
        Note that (0, 0) is the top left corner of the window.
    size:
        The height and width of this Block.  Since all blocks are square,
        we needn't represent height and width separately.
    colour:
        If this block is not subdivided, <colour> stores its colour.
        Otherwise, <colour> is None and this block's sublocks store their
        individual colours.
    level:
        The level of this block within the overall block structure.
        The outermost block, corresponding to the root of the tree,
        is at level zero.  If a block is at level i, its children are at
        level i+1.
    max_depth:
        The deepest level allowed in the overall block structure.
    highlighted:
        True iff the user has selected this block for action.
    children:
        The blocks into which this block is subdivided.  The children are
        stored in this order: upper-right child, upper-left child,
        lower-left child, lower-right child.
    parent:
        The block that this block is directly within.

    === Representation Invariations ===
    - len(children) == 0 or len(children) == 4
    - If this Block has children,
        - their max_depth is the same as that of this Block,
        - their size is half that of this Block,
        - their level is one greater than that of this Block,
        - their position is determined by the position and size of this Block,
          as defined in the Assignment 2 handout, and
        - this Block's colour is None
    - If this Block has no children,
        - its colour is not None
    - level <= max_depth
    """
    position: Tuple[int, int]
    size: int
    colour: Optional[Tuple[int, int, int]]
    level: int
    max_depth: int
    highlighted: bool
    children: List['Block']
    parent: Optional['Block']

    def __init__(self, level: int,
                 colour: Optional[Tuple[int, int, int]] = None,
                 children: Optional[List['Block']] = None) -> None:
        """Initialize this Block to be an unhighlighted root block with
        no parent.

        If <children> is None, give this block no children.  Otherwise
        give it the provided children.  Use the provided level and colour,
        and set everything else (x and y coordinates, size,
        and max_depth) to 0.  (All attributes can be updated later, as
        appropriate.)
        """
        self.highlighted = False
        self.parent = None
        self.level = level
        self.colour = colour
        self.max_depth = 5
        self.position = (0, 0)
        self.size = BIGGEST_SIZE
        if children is None:
            self.children = []
        else:
            self.children = [child for child in children]
            self.update_block_locations(self.position, BIGGEST_SIZE)

    def rectangles_to_draw(self) -> List[Tuple[Tuple[int, int, int],
                                               Tuple[int, int],
                                               Tuple[int, int],
                                               int]]:
        """
        Return a list of tuples describing all of the rectangles to be drawn
        in order to render this Block.

        This includes (1) for every undivided Block:
            - one rectangle in the Block's colour
            - one rectangle in the FRAME_COLOUR to frame it at the same
              dimensions, but with a specified thickness of 3
        and (2) one additional rectangle to frame this Block in the
        HIGHLIGHT_COLOUR at a thickness of 5 if this block has been
        selected for action, that is, if its highlighted attribute is True.

        The rectangles are in the format required by method Renderer.draw.
        Each tuple contains:
        - the colour of the rectangle
        - the (x, y) coordinates of the top left corner of the rectangle
        - the (height, width) of the rectangle, which for our Blocky game
          will always be the same
        - an int indicating how to render this rectangle. If 0 is specified
          the rectangle will be filled with its colour. If > 0 is specified,
          the rectangle will not be filled, but instead will be outlined in
          the FRAME_COLOUR, and the value will determine the thickness of
          the outline.

        The order of the rectangles does not matter.
        """

        rectangles_list = []

        if len(self.children) != 0:
            # This generates all blocks from the children and their children.
            for child_block in self.children:
                rectangles_list.extend(child_block.rectangles_to_draw())
        else:
            # Now we are dealing with a block that has no children, so we may
            # proceed generating rectangles.
            # (1) one rectangle in the Block's colour (thickness of 0)
            rectangles_list.append((self.colour, self.position,
                                    (self.size, self.size), 0))
            # (1) one rectangle in the FRAME_COLOUR to frame it at the same
            # dimensions, but with a specified thickness of 3
            rectangles_list.append((FRAME_COLOUR, self.position,
                                    (self.size, self.size), 3))

        # (2) Highlighted block (need to verify whether it is selected)
        if self.highlighted:
            rectangles_list.append((HIGHLIGHT_COLOUR, self.position,
                                    (self.size, self.size), 5))

        return rectangles_list

    def swap(self, direction: int) -> None:
        """Swap the child Blocks of this Block.

        If <direction> is 1, swap vertically.  If <direction> is 0, swap
        horizontally. If this Block has no children, do nothing.
        """

        self.update_block_locations(self.position, self.size)

        # When there is no children, do nothing.
        if len(self.children) == 0:
            return

        # Swaps horizontally.
        if direction == 0:
            self.children = [
                self.children[UP_LEFT],
                self.children[UP_RIGHT],
                self.children[LOW_RIGHT],
                self.children[LOW_LEFT]
            ]
        # Swap vertically.
        else:
            self.children = [
                self.children[LOW_RIGHT],
                self.children[LOW_LEFT],
                self.children[UP_LEFT],
                self.children[UP_RIGHT]
            ]

        self.update_block_locations(self.position, self.size)

    def rotate(self, direction: int) -> None:
        """Rotate this Block and all its descendants.

        If <direction> is 1, rotate clockwise.  If <direction> is 3, rotate
        counterclockwise. If this Block has no children, do nothing.
        """

        self.update_block_locations(self.position, self.size)

        # If there is no childre, do nothing.
        if len(self.children) == 0:
            return

        # Sets the offset to be clockwise.
        if direction == 1:
            self.children = [
                self.children[3],
                self.children[0],
                self.children[1],
                self.children[2]
            ]
        # Sets the offset to be counterclockwise.
        elif direction == 3:
            self.children = [
                self.children[1],
                self.children[2],
                self.children[3],
                self.children[0]
            ]

        # We must also rotate the children's children.
        for child in self.children:
            child.rotate(direction)

        self.update_block_locations(self.position, self.size)

    def smash(self) -> bool:
        """Smash this block.

        If this Block can be smashed,
        randomly generating four new child Blocks for it.  (If it already
        had child Blocks, discard them.)
        Ensure that the RI's of the Blocks remain satisfied.

        A Block can be smashed iff it is not the top-level Block and it
        is not already at the level of the maximum depth.

        Return True if this Block was smashed and False otherwise.
        """

        # We check whether the block is at maximum depth or it is at 0 level
        # before proceeding.
        if self.level != self.max_depth and self.level != 0:
            # This block will have new children (all old ones will be lost).
            child_list = []
            for _ in range(4):
                new_child = random_init(self.level + 1, self.max_depth)
                child_list.append(new_child)
            self.children = child_list
            # We shall update their location.
            self.update_block_locations(self.position, self.size)
            # Smash was successful.
            return True
        else:
            # Smash not successful.
            return False

    def update_block_locations(self, top_left: Tuple[int, int],
                               size: int) -> None:
        """
        Update the position and size of each of the Blocks within this Block.

        Ensure that each is consistent with the position and size of its
        parent Block.

        <top_left> is the (x, y) coordinates of the top left corner of
        this Block.  <size> is the height and width of this Block.
        """
        self.position = top_left
        self.size = size
        for child_index in range(len(self.children)):
            child = self.children[child_index]
            # we decided to leave an assignment to the parent attribute also
            # on this method, since it would cover cases where the child block
            # is initialized without random_init().
            child.parent = self
            x_position = self.position[0]
            y_position = self.position[1]
            # When it is the second and fourth child, there shall be a
            # horizontal offset (indexes 0 and 3)
            if child_index == 3 or child_index == 0:
                x_position += round(size / 2)
            # vert. offset. (indexes 3 and 2)
            if child_index & 2:
                y_position += round(size / 2)
            child.position = (x_position, y_position)
            # Call to update child blocks' locations.
            child.update_block_locations(child.position, round(self.size / 2))

    def get_selected_block(self, location: Tuple[int, int], level: int) \
            -> 'Block':
        """Return the Block within this Block that includes the given location
        and is at the given level. If the level specified is lower than
        the lowest block at the specified location, then return the block
        at the location with the closest level value.

        <location> is the (x, y) coordinates of the location on the window
        whose corresponding block is to be returned.
        <level> is the level of the desired Block.  Note that
        if a Block includes the location (x, y), and that Block is subdivided,
        then one of its four children will contain the location (x, y) also;
        this is why <level> is needed.

        Preconditions:
        - 0 <= level <= max_depth
        """

        if self.level == level:
            # Base case, because the location match, and so does the level.
            return self
        else:
            # When the block has no children
            if len(self.children) == 0:
                return self

            # We use center location, provided by the position of the lower
            # right child block, in order to know to which child block to go.
            center_location = self.children[LOW_RIGHT].position
            if location[0] >= center_location[0]:
                if location[1] >= center_location[1]:
                    return self.children[LOW_RIGHT].get_selected_block(location,
                                                                       level)
                else:
                    return self.children[UP_RIGHT].get_selected_block(location,
                                                                      level)
            else:
                if location[1] >= center_location[1]:
                    return self.children[LOW_LEFT].get_selected_block(location,
                                                                      level)
                else:
                    return self.children[UP_LEFT].get_selected_block(location,
                                                                     level)

    def flatten(self) -> List[List[Tuple[int, int, int]]]:
        """Return a two-dimensional list representing this Block as rows
        and columns of unit cells.

        Return a list of lists L, where, for 0 <= i, j < 2^{self.level}
            - L[i] represents column i and
            - L[i][j] represents the unit cell at column i and row j.
        Each unit cell is represented by 3 ints for the colour
        of the block at the cell location[i][j]

        L[0][0] represents the unit cell in the upper left corner of the Block.
        """

        if len(self.children) == 0:
            # This is a situation where we have an undivisible block (base case)

            smallest_block_size = round(BIGGEST_SIZE / (2 ** self.max_depth))
            # small_squares reffer to the number of small squares in one
            # dimension (e.g. how many divisions are on the left side of a
            # block).
            small_blocks = round(self.size / smallest_block_size)
            # Now we create a table containing the colour of this
            # undivided block.
            flatten_table = [[self.colour for _i in range(small_blocks)]
                             for _j in range(small_blocks)]
            return flatten_table

        else:
            # We first assemble the upper part from the child blocks
            flatten_top_left = self.children[UP_LEFT].flatten()
            flatten_top_right = self.children[UP_RIGHT].flatten()

            flatten_table_top = []
            # flatten_table_top_left and flatten_table_top_right must have
            # same length. This loop will assemble the top part of the parent
            # block.
            for line_number in range(len(flatten_top_left)):
                flatten_table_top.append(flatten_top_left[line_number] +
                                         flatten_top_right[line_number])

            # Then we assemble the bottom half part of the block
            flatten_bottom_left = self.children[LOW_LEFT].flatten()
            flatten_bottom_right = self.children[LOW_RIGHT].flatten()

            flatten_table_bottom = []
            # flatten_bottom_left and flatten_bottom_right must have same
            # length. This loop will assemble the bottom part of the parent
            # block.
            for line_number in range(len(flatten_bottom_left)):
                flatten_table_bottom.append(flatten_bottom_left[line_number] +
                                            flatten_bottom_right[line_number])

            # Hence we assemble both halves (top and bottom)
            flatten_table = flatten_table_top + flatten_table_bottom

            # returns the flatten block
            return flatten_table


def random_init(level: int, max_depth: int) -> 'Block':
    """Return a randomly-generated Block with level <level> and subdivided
    to a maximum depth of <max_depth>.

    Throughout the generated Block, set appropriate values for all attributes
    except position and size.  They can be set by the client, using method
    update_block_locations.

    Precondition:
        level <= max_depth
    """
    # If this Block is not already at the maximum allowed depth, it can
    # be subdivided. Use a random number to decide whether or not to
    # subdivide it further.

    # Random decisory process based on level:
    random_number = random.random()
    if level < max_depth and random_number < math.exp(-0.25 * level):
        # Since we decided to subdivide this block, we shall make 4 random
        # children blocks for it.
        random_block = Block(level, None, None)
        for child_index in range(4):
            random_block.children.append(random_init(level + 1, max_depth))
            random_block.children[child_index].parent = random_block
    else:
        # Now we use a random number to pick up a colour for this block
        random_number = random.randint(0, len(COLOUR_LIST) - 1)
        random_block = Block(level, COLOUR_LIST[random_number], None)

    return random_block


def attributes_str(b: Block, verbose) -> str:
    """Return a str that is a concise representation of the attributes of <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Note: These are attributes that every Block has.
    """
    answer = f'pos={b.position}, size={b.size}, level={b.level}, '
    if verbose:
        answer += f'highlighted={b.highlighted}, max_depth={b.max_depth}'
    return answer


def print_block(b: Block, verbose=False) -> None:
    """Print a text representation of Block <b>.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    print_block_indented(b, 0, verbose)


def print_block_indented(b: Block, indent: int, verbose) -> None:
    """Print a text representation of Block <b>, indented <indent> steps.

    Include attributes position, size, and level.  If <verbose> is True,
    also include highlighted, and max_depth.

    Precondition: b is not None.
    """
    if len(b.children) == 0:
        # b a leaf.  Print its colour and other attributes
        print(f'{"  " * indent}{colour_name(b.colour)}: ' +
              f'{attributes_str(b, verbose)}')
    else:
        # b is not a leaf, so it doesn't have a colour.  Print its
        # other attributes.  Then print its children.
        print(f'{"  " * indent}{attributes_str(b, verbose)}')
        for child in b.children:
            print_block_indented(child, indent + 1, verbose)


if __name__ == '__main__':
    import python_ta

    python_ta.check_all(config={
        'allowed-io': ['print_block_indented'],
        'allowed-import-modules': [
            'doctest', 'python_ta', 'random', 'typing',
            'block', 'goal', 'player', 'renderer', 'math'
        ],
        'max-attributes': 15
    })

    # This tiny tree with one node will have no children, highlighted False,
    # and will have the provided values for level and colour; the initializer
    # sets all else (position, size, and max_depth) to 0.
    b0 = Block(0, COLOUR_LIST[2])
    # Now we update position and size throughout the tree.
    b0.update_block_locations((0, 0), 750)
    print("=== tiny tree ===")
    # We have not set max_depth to anything meaningful, so it still has the
    # value given by the initializer (0 and False).
    print_block(b0, True)

    b1 = Block(0, children=[
        Block(1, children=[
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, COLOUR_LIST[2]),
        Block(1, children=[
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[1]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[0])
        ]),
        Block(1, children=[
            Block(2, COLOUR_LIST[0]),
            Block(2, COLOUR_LIST[2]),
            Block(2, COLOUR_LIST[3]),
            Block(2, COLOUR_LIST[1])
        ])
    ])
    b1.update_block_locations((0, 0), 750)
    print("\n=== handmade tree ===")
    # Similarly, max_depth is still 0 in this tree.  This violates the
    # representation invariants of the class, so we shouldn't use such a
    # tree in our real code, but we can use it to see what print_block
    # does with a slightly bigger tree.
    print_block(b1, True)

    # Now let's make a random tree.
    # random_init has the job of setting all attributes except position and
    # size, so this time max_depth is set throughout the tree to the provided
    # value (3 in this case).
    b2 = random_init(0, 3)
    # Now we update position and size throughout the tree.
    b2.update_block_locations((0, 0), 750)
    print("\n=== random tree ===")
    # All attributes should have sensible values when we print this tree.
    print_block(b2, True)
