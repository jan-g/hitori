import sys
from hitori.board import Hitori, solve


def main():
    lines = [l.strip() for l in sys.stdin.readlines() if l.strip()]
    board = Hitori(*lines)
    print(board)
    print()
    print("solving...")
    answers = solve(board)

    print(len(answers), "solutions found:")
    for a in answers:
        print()
        print(a)
