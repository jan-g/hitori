from hitori.board import Hitori, solve
import pytest


def test_board():
    b1 = Hitori("12", "34")

    b2 = b1.blank(0, 0)

    assert str(b1) == "12\n34"
    assert str(b2) == "#2\n34"


def test_cannot_blank_neighbouring_squares():
    b1 = Hitori("12", "34").blank(0, 0)

    with pytest.raises(ValueError):
        b2 = b1.blank(1, 0)

    with pytest.raises(ValueError):
        b2 = b1.blank(0, 1)

    assert str(b1.blank(1, 1)) == "#2\n3#"

    b1 = Hitori("12", "34").blank(1, 0)

    with pytest.raises(ValueError):
        b2 = b1.blank(0, 0)

    with pytest.raises(ValueError):
        b2 = b1.blank(1, 1)

    assert str(b1.blank(0, 1)) == "1#\n#4"


def test_solve():
    b1 = Hitori("11", "21")

    bs = solve(b1)
    assert len(bs) == 1
    b2 = bs.pop()
    assert b2 == Hitori("1#", "21")

def test_longer():
    board = Hitori("15312",
                   "54134",
                   "34315",
                   "44233",
                   "21544")

    assert solve(board) == {
        Hitori("153#2",
               "5#134",
               "34#15",
               "4#2#3",
               "2154#")
    }
