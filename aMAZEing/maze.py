#
# Maze Solver 1.0
# https://gist.github.com/a613/49d65dc30e98c165d567
# March 2014
# alex@python.code.trimtab.ca
#
# Solves a maze stored in a text file, and outputs the solution
# path to a second text file in the same format.
#
# Required command-line arguments: <input_file> <output_file>
# Example usage:
#
# <in.txt>
# ####################################
# #S#  ##  ######## # #      #     # #
# # #   #             # #        #   #
# #   # ##### ## ###### # #######  # #
# ### # ##    ##      # # #     #### #
# #   #    #  #######   #   ###    #E#
# ####################################
#
# python maze.py in.txt out.txt
#
# <out.txt>
# ####################################
# #S#  ##  ########.#.#>>>>>v#  >>v# #
# #v#>>v#    >>>v.....#^#   >>>>^#>>v#
# #>>^#v#####^##v######^# #######  #v#
# ###.#v##>>>^##>>>>>v#^# #     ####v#
# #...#>>>^#..#######>>^#   ###    #E#
# ####################################
#


import operator
import sys


class Maze(object):
    """Represents a two-dimensional maze, where each cell can hold a
       single marker."""

    def __init__(self):
        self.data = []

    # Added by Lorenzo Leonardini
    def read_personal(self, asd):
        maze = []
        for line in asd:
            maze.append(list(line))
        self.data = maze

    def read_file(self, path):
        """Read a maze text file and split out each character. Return
           a 2-dimensional list where the first dimension is rows and
           the second is columns."""
        maze = []
        with open(path) as f:
            for line in f.read().splitlines():
                maze.append(list(line))
        self.data = maze

    def write_file(self, path):
        """Write the specified 2-dimensional maze to the specified
           file, writing one line per row and with columns
           side-by-side."""
        with open(path, 'w') as f:
            for r, line in enumerate(self.data):
                f.write('%s\n' % ''.join(line))

    # Added by Lorenzo Leonardini
    def return_solution(self, sol='', where=None):
        start_symbol = 'S'
        end_symbol = 'E'
        vacant_symbol = ' '
        backtrack_symbol = '.'
        directions = (0, 1), (1, 0), (0, -1), (-1, 0)
        direction_marks = '>', 'v', '<', '^'
        direction_key = 'D', 'S', 'A', 'W'

        where = where or self.find(start_symbol)
        # print(where)
        if self.get(where) == end_symbol:
            # standing on the end cell
            return sol

        if self.get(where) == start_symbol:
            next_cell = map(operator.add, where, directions[0])
            if self.get(next_cell) in direction_marks and self.get(next_cell) != '<':
                return self.return_solution('D', next_cell)
            else:
                return self.return_solution('S', map(operator.add, where, directions[1]))

        if self.get(where) not in direction_marks:
            return

        direction = directions[direction_marks.index(self.get(where))]
        next_cell = map(operator.add, where, direction)
        return self.return_solution(sol + direction_key[directions.index(direction)], next_cell)


    def find(self, symbol):
        """Find the first instance of the specified symbol in the
           maze, and return the row-index and column-index of the
           matching cell. Return None if no such cell is found."""
        for r, line in enumerate(self.data):
            try:
                return r, line.index('S')
            except ValueError:
                pass

    def get(self, where):
        """Return the symbol stored in the specified cell."""
        r, c = where
        return self.data[r][c]

    def set(self, where, symbol):
        """Store the specified symbol in the specified cell."""
        r, c = where
        self.data[r][c] = symbol

    def __str__(self):
        return '\n'.join(''.join(r) for r in self.data)


def solve(maze, where=None, direction=None):
    """Finds a path through the specified maze beginning at where (or
       a cell marked 'S' if where is not provided), and a cell marked
       'E'. At each cell the four directions are tried in the order
       RIGHT, DOWN, LEFT, UP. When a cell is left, a marker symbol
       (one of '>', 'v', '<', '^') is written indicating the new
       direction, and if backtracking is necessary, a symbol ('.') is
       also written. The return value is None if no solution was
       found, and a (row_index, column_index) tuple when a solution
       is found."""
    start_symbol = 'S'
    end_symbol = 'E'
    vacant_symbol = ' '
    backtrack_symbol = '.'
    directions = (0, 1), (1, 0), (0, -1), (-1, 0)
    direction_marks = '>', 'v', '<', '^'

    where = where or maze.find(start_symbol)
    if not where:
        # no start cell found
        return
    if maze.get(where) == end_symbol:
        # standing on the end cell
        return where
    if maze.get(where) not in (vacant_symbol, start_symbol):
        # somebody has been here
        return

    for direction in directions:
        next_cell = map(operator.add, where, direction)

        # spray-painting direction
        marker = direction_marks[directions.index(direction)]
        if maze.get(where) != start_symbol:
            maze.set(where, marker)

        sub_solve = solve(maze, next_cell, direction)
        if sub_solve:
            # found solution in this direction
            return sub_solve

    # no directions worked from here - have to backtrack
    maze.set(where, backtrack_symbol)

if __name__ == '__main__':
    if len(sys.argv) < 3:
        print 'Arguments: <input file> <output file>'
        sys.exit(1)
    input_file, output_file = sys.argv[1:3]

    maze = Maze()
    maze.read_file(input_file)

    solution = solve(maze)
    if solution:
        print 'Found end of maze at %s' % solution
    else:
        print 'No solution (no start, end, or path)'

    print maze
    maze.write_file(output_file)
