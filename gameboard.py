import collections
import numpy as np

Location = collections.namedtuple('Location', 'row column')
Shape = collections.namedtuple('Shape', 'width height')


class GameBoard:

    def __init__(self, shape):
        """Creates a lists of lists of booleans that represent each tile of the GameBoard."""

        self._shape=shape
        self._board=[[False]*shape.width for i in range(shape.height)]

        #Creates two lists with size equal to the height and width of the GameBoard that we will use as counters for rows and columns.
        #every position of this lists contains the number of squares occupied in such row or column.

        self._row_counters=[0]*shape.height
        self._column_counters=[0]*shape.width

    def get_shape(self):
        """returns the GameBoard shape"""

        return self._shape

    def __empty__(self, location):
        """returns if the location for shapes 1x1"""
        return not self._board[location.row][location.column]

    def row_counters(self):
        return self._row_counters

    def column_counters(self):
        return self._column_counters

    def __str__(self):
        """Prints the GameBoard"""
        #efficiency: O(w·h)

        self._board.reverse() #Revers the GameBoard so it appears at the screen with the  rows and columns inversed
        white_token = '\u2b1c' #unicode for a whitetoken.
        black_token = '\u2b1b' #unicode for a black token.
        aux = '' #string that will contain all of the tokens.
        for i in range(self._shape.height):
            if not i==self._shape.width:
                aux += '\n'
            for j in range(self._shape.width):
                if self._board[i][j]: #for every position in true in the GameBoard adds a black token to aux.
                    aux += black_token
                else:
                    aux += white_token #for every position in false in the GameBoard adds a white token to aux
        self._board.reverse() #reverse the board again to be able to do the modifications needed correctly.
        return aux

    def __repr__(self):
        """Returns a sring indicating the shape of the GameBoard and the occupied locations."""
        #efficiency:O(w·h)

        Occupied=False
        a='{}*{} board: {{'. format(self._shape.width, self._shape.height)

        #Adds each occupied location to a string.
        for j in range(self._shape.height):
            for i in range(self._shape.width):
                if not self.__empty__(Location(j, i)):
                    Occupied=True
                    a+='({},{}), '.format(j,i)

        if Occupied:
            a=a[:-2]

        return a+'}'


    def is_empty(self, location, shape=Shape(1,1)):
        """Returns if a square or rectangle from the GameBoard is empty or not."""
        #efficiency:O(w·h)

        #in case the shape is a rectangle.
        if shape.width != 1 or shape.height !=1:
            for i in range (shape.height):
                for j in range(shape.width):
                    if location.row+shape.height>self._shape.height or location.column+shape.width>self._shape.width:
                        return False
                    elif self._board[location.row+i][location.column+j]:
                        return False

        #in case the shape is a square.

        if shape.width ==1 and shape.height ==1:
            return not self._board[location.row][location.column]
        return True

    def is_full(self, location, shape=Shape(1,1)):
        "Returns if a square or a rectangle from the GameBoard is full or not"
        #efficiency:O(w·h)

        #in case the shape is a rectangle:
        if shape.width != 1 or shape.height !=1:
            for i in range (shape.height):
                for j in range(shape.width):
                    if not self._board[location.row+i][location.column+j]:
                        return False

        #in cas the shape is a square:
        if shape.width ==1 and shape.height ==1:
            return self._board[location.row][location.column]


    def put(self, location, shape = Shape (1, 1)):
        """The put function returns self with tokens in the give area of the gameboard.
        If the shape (or area) is not especified, the function will understand it
        as a square 1*1. It also raises exception in case the square is out of bounds
        or is already occupied and if the rectangle cannot be put on the board"""
        #efficiency:O(shape.width·sahpe.height)

        #in case it's a square:
        if (shape == (1, 1)):
            #if the given location is out of the board or if it's occupied.
            if location.row > self._shape.width or location.column > self._shape.height:
                raise Exception("The square is out of bounds.")
            if(self._board[location.row][location.column]):
                raise Exception("The square is already occupied.")
            else:
            #if neither of the two conditions is met, it puts the token in the indicated position.
                self._board[location.row][location.column] = True
                #add 1 to the lists of counters created in the __init__ function.
                self._row_counters[location.row] +=1
                self._column_counters[location.column]+=1
        else:
            #in case it's a rectangle:
            #if the given area is bigger than 1*1, it make sure the rectangle can be put on the board.
            if shape.width + location.column > self._shape.width or shape.height + location.row>self._shape.height:
                raise Exception('The rectangle cannot be put on the board')
            #it checks if every location of the rectangle in the board is empty.
            for i in range (shape.height):
                for j in range (shape.width):
                    if self._board[location.row + i][location.column + j ]:
                        raise Exception("The rectangle cannot be put on the board.")
                    else:
                        #puts a token in every given position.
                        self._board[location.row + i][location.column + j ] = True
                        #adds 1 to the counters in the corresponding position .
                        self._row_counters[location.row+i] +=1
                        self._column_counters[location.column+j]+=1

        return self

    def remove(self, location, shape =Shape (1, 1)):
        """The remove function returns self with the tokens in the given area of the gameboard removed.
        If the shape (or area) is not especified, the function will understand it
        as a square 1*1. It also raises exception in case the square is out of bounds
        or is already empty and if the rectangle cannot be removed"""
        #efficiency:O(shape.width·shape.height)
        #in case it's a square:
        if shape == (1, 1):
            #checks if the location is not empty.
            if self._board[location.row][location.column]:
                self._board[location.row][location.column] = False
                #substracts one from the counters.
                self._row_counters[location.row] -=1
                self._column_counters[location.column]-=1
            else:
                raise Exception("The square is already empty")

        else:
            #in case it's a rectangle:
            #its make sure the rectangle can be removed of the board.
            if shape.width + location.column > self._shape.width or shape.height + location.row>self._shape.height:
                raise Exception("The rectangle cannot be removed.")
            else:
                for i in range (shape.height):
                    for j in range (shape.width):
                        if not self._board[location.row + i][location.column + j]:
                            raise Exception("The rectangle cannot be removed.")
                        else:
                            #removes token from every given position.
                            self._board[location.row + i][location.column + j ] = False
                            #substracts one from the corresponding position of the counters.
                            self._row_counters[location.row+i]-=1
                            self._column_counters[location.column+j]-=1


        return self

    def full_rows(self):
        """returns a list with the rows that are fully covered with black tokens."""
        #efficiency: O(h)

            #It compares the tokens in the rows with their counters and returns the rows that are full.

        rows=[]

        for i in range(len(self.row_counters())):
            if self._row_counters[i]==self._shape.width:
                rows.append(i)
        return rows

    def full_columns(self):
            """returns a list with the columns that are fully covered with black tokens."""
            #efficiency:O(w)

            #It compares the tokens in the columns with their counters and returns the columns that are full.

            columns=[]
            for j in range(len(self.column_counters())):
                if self._column_counters[j]==self._shape.height:
                    columns.append(j)
            return columns

    def clear(self, location):
        """removes the tokens from the given locations"""

        #checks if it's empty:
        if not self.__empty__(location):
            self._board[location.row][location.column] = False
            #substracts 1 from the corresponding positions of the counters.
            self._row_counters[location.row] -= 1
            self._column_counters[location.column] -= 1

    def clear_rows(self, rows):
        """Returns self having cleared all tokens in the rows in the given list"""
        #efficiency: O(w·h)

        for i in rows:
            for j in range(self._shape.width):
                self.clear(Location(i, j))

        return self

    def clear_columns(self, columns):
        """Returns self having cleared all tokens in the columns in the given list"""
        #efficiency:O(w·h)

        for j in columns:
            for i in range(self._shape.height):
                self.clear(Location(i, j))

        return self
