import urllib.request
from gameboard import *
import collections

class MyPlayer:


    def __init__(self, w, h, method='simple'):
        """Initialize self"""
        self._shape=Shape(w,h)
        self._board=GameBoard(Shape(w,h))
        self._method=method

    def __str__(self):
        """prints the board"""
        #efficiency:O(w·h)
        return self._board.__str__()

    def __repr__(self):
        """prints the occupied locations of the board"""
        #efficiency:O(w·h)
        return self._board.__repr__()

    def full_rows(self):
        """Returns the occupied rows"""
        #efficiency:O(h)
        return self._board.full_rows()

    def full__columns(self):
        """returns the occupied columns"""
        #efficiency:O(w)
        return self._board.full_columns()

    def place_block(self, location, shape=Shape(1,1)):
        """Places a block in the given area of the gameboard and if it completes a row or a column it clears them"""
        #efficiecy:O(w·h)
        self._board.put(location, shape)
        rows=self._board.full_rows()
        columns=self._board.full_columns()
        self._board.clear_rows(rows)
        self._board.clear_columns(columns)


    def is_legal(self, shape=Shape(1,1)):
        """returns a boolean if the given area is bigger than the board itself
        after checking if the components are positive."""
        assert shape.width>0
        assert shape.height>0
        j=shape.width<=self._board.get_shape().width
        i=shape.height<=self._board.get_shape().height
        return j and i

    def play(self, block):
        if self._method=='expert':
            return self.play_expert(block)
        else:
            return self.play_simple(block)

    def play_simple(self, block):
        """From all the possible locations for a block, picks the one with the lowest row.
        In case several locations are possible in the same row, pick the one with the lowest column.
        Returns said location."""
        #Efficiency: O(w·h)
        for i in range(self._board.get_shape().height):
            for j in range(self._board.get_shape().width):
                    if self.is_legal(block):
                            if self._board.is_empty(Location(i,j),block):
                                return Location(i,j)
        return None


def play_game(player, blocks, show=True):
    """It plays the blocks puzzle using a pre-defined player. If show is asserted, the state of the player
is printed after placing each block. It returns the number of blocks that could be placed.
"""
#efficiency:O(len(blocks)·w·h)
    if show: print(player)
    count = 0
    for block in blocks:
        assert player.is_legal(block)
        loc = player.play(block)
        if loc is None: break
        player.place_block(loc, block)
        count += 1
        if show: print(player)
    return count


def read_file(file, url=True):
    """It reads a file of integers representing shapes. Each pair of consecutive integers represents
    a shape (width and height). It returns a list of shapes. If url is not asserted, file is assumed
    to be the name of a local file.
    """
    #efficiency:O(i)
    if url:
        with urllib.request.urlopen(file) as reader:
            items = reader.read().split()
    else:
        with open(file) as reader:
            items = reader.read().split()

    # Check there is an even number of items
    assert len(items) % 2 == 0, "Wrong number of items in " + file

    # Convert pairs of items to shapes, checking that the items are correct.
    R = []
    for i in range(0, len(items), 2):
        # Check the items are numbers
        assert items[i].isdigit() and items[i+1].isdigit(), "Some element in the list is not an integer"
        w, h = int(items[i]), int(items[i+1])
        assert w > 0 and h > 0, "Illegal size for a shape"
        R.append(Shape(w, h))
    return R
