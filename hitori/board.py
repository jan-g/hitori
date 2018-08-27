from collections import defaultdict
from functools import partial
from hitori.union_find import UnionFind


class Hitori:
    """A representation of a Hitori board.

    This implements an immutable, value-style board.
    >>> board = Hitori("48163257",
                       "36721654",
                       "23482861",
                       "41657735",
                       "72318512",
                       "35673184",
                       "64235478",
                       "87142356")

    The `blank` method constructs a *new* instance, with the specified space blanked out; the current instance
    remains unchanged.
    >>> b2 = board.blank(0, 0)
    """
    BLANK = '#'

    @classmethod
    def parse(cls, layout):
        lines = layout.split("\n")
        return Hitori(*lines)

    def __init__(self, *lines):
        assert all(len(l) == len(lines[0]) for l in lines)
        self.lines = tuple(lines)

    def __getitem__(self, coord):
        x, y = coord
        return self.lines[y][x]

    def size(self):
        return len(self.lines[0]), len(self.lines)

    def row(self, y):
        return [(x, y) for x in range(len(self.lines[0]))]

    def col(self, x):
        return [(x, y) for y in range(len(self.lines))]

    def is_blank(self, x, y):
        return 0 <= x < len(self.lines[0]) and 0 <= y < len(self.lines) and self[x, y] == Hitori.BLANK

    def blank(self, x, y):
        if self.is_blank(x - 1, y) or self.is_blank(x + 1, y) or self.is_blank(x, y - 1) or self.is_blank(x, y + 1):
            raise ValueError("can't blank that square")
        lines = list(self.lines)
        lines[y] = lines[y][:x] + Hitori.BLANK + lines[y][x + 1:]
        return Hitori(*lines)

    def __str__(self):
        return '\n'.join(self.lines)

    def __eq__(self, other):
        return isinstance(other, Hitori) and other.lines == self.lines

    def __hash__(self):
        return hash(self.lines)


def solve(board):
    """We perform a depth-first recursive search for solutions.

    We do this by constructing a list of generator functions; each function takes a board (and
    the current and remaining generators). If it has work to do, it produces one or more
    modifications of the original board and recursively passes that to the following generator functions.

    We end the chain with a function which simply prints out any boards that make it all the way
    through the filter chain.
    """
    mx, my = board.size()

    answers = set()

    gens = ([partial(blank_some, row_n(y)) for y in range(my)] +
            # [print_candidate] +
            [partial(blank_some, col_n(x)) for x in range(mx)] +
            # [print_candidate] +
            [check_connectedness,
             # print_candidate,
             partial(collect_candidate, answers)])

    gens[0](board, gens)

    return answers


def row_n(n):
    """This returns a selector which picks the coordinates of cells in a given row"""
    def row(board):
        return board.row(n)

    return row


def col_n(n):
    """This returns a selector which picks the coordinates of cells in a given column"""
    def col(board):
        return board.col(n)

    return col


def blank_some(selector, board, generators):
    """Given a selector that picks some cells from the current board, check to see if we've any duplicate cell values.

    If we have, pick one of those duplicate values and try blanking out all but one of them.
    Continue to search the board by re-examining the same row or column - since a row/column may contain multiple
    sets of duplicate values.

    Once we've eliminated all the duplicate values in the current row or column, pass the candidate board on
    for processing by any following filters.

    (We additionally permit blanking out *all* of the duplicate values in a set - since this isn't explicitly prohibited
    in the definition of a Hitori puzzle that I found.)
    """
    cells = selector(board)
    counts = defaultdict(list)

    # Group the cells into sets of those which have the same value
    for (x, y) in cells:
        if not board.is_blank(x, y):
            counts[board[x, y]].append((x, y))

    # Are there any values appearing in more than one square?
    for value, where in counts.items():
        if len(where) > 1:
            # Okay, let's try these options -
            # Either: blank all but one of these,
            # or: blank them all.
            for (x, y) in where:
                # Blank them all out except for this one.
                b2 = board

                for (x2, y2) in where:
                    if (x2, y2) != (x, y):
                        try:
                            b2 = b2.blank(x2, y2)
                        except ValueError:
                            break
                else:
                    # We need to check this row/column again, to see if anything else can be blanked
                    generators[0](b2, generators)

            # Try blanking them all out
            b2 = board
            for (x, y) in where:
                try:
                    b2 = b2.blank(x, y)
                except ValueError:
                    break
            else:
                generators[0](b2, generators)

            return
    else:
        # Apparently not. Try the next generator, if one is given.
        if len(generators) > 1:
            generators[1](board, generators[1:])


def print_candidate(board, generators):
    """Print out a candidate board, if it reaches this filter.

    The board is passed on to any following generators/filters - which permits this to be used
    for outputting debugging during intermediate stages.
    """
    print(board)
    print()

    if len(generators) > 1:
        generators[1](board, generators[1:])


def check_connectedness(board, generators):
    """We check that all non-blank squares are connected.

    This is done with a union-find data structure; all squares that are next to
    other non-blank squares share an equivalence class.

    The board is then completely connected iff the size of the final equivalence set
    is the same as the total number of non-blank cells.
    """
    mx, my = board.size()
    cells = set((x, y)
                for y in range(my)
                for x in range(mx)
                if not board.is_blank(x, y))

    if len(cells) > 0:
        uf = UnionFind(cells)
        for (x, y) in cells:
            some_x, some_y = x, y
            uf.union((x, y), (x - 1, y))
            uf.union((x, y), (x + 1, y))
            uf.union((x, y), (x, y - 1))
            uf.union((x, y), (x, y + 1))

        _, n = uf.find((some_x, some_y))
        if n != len(cells):
            return

    # This passes, keep processing
    if len(generators) > 1:
        generators[1](board, generators[1:])


def collect_candidate(collection, board, generators):
    """As the board passes through this filter, add it to a collection of solutions"""
    collection.add(board)

    if len(generators) > 1:
        generators[1](board, generators[1:])
