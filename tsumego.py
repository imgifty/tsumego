import random
import os
import sgf

from board import Board
from tracker import insert_problem, solved_daily_problem, get_solved_problems


def read_sgf(file_name):
    with open(file_name) as f:
        game = sgf.parse(f.read())
        return game


def create_position(game):
    assert len(game.children) == 1
    game_tree = game.children[0]
    nodes = game_tree.nodes
    node = nodes[0]
    b = Board(node)

    while True:
        print(b.create_ascii_art())
        print(f'{b.get_starting_player()} to play (top-left): ')
        placement = input('>>')
        stone = valid_move(placement)

        if stone is not None:
            valid = b.suggest_move(stone)
            if valid:
                b.advance()
                finished = b.advance()
                if finished:
                    print(b.create_ascii_art())
                    return True
            else:
                return False


def valid_move(placement):
    try:
        top, _, bottom = placement.partition('-')
        stone = int(bottom)-1, int(top)-1

        if 0 <= stone[0] <= 18 and 0 <= stone[1] <= 18:
            return stone
        else:
            return None
    except ValueError:
        return None


def main(seed=None):
    if not solved_daily_problem():
        samples = '/home/alexander/Work/tsumego/samples/'
        collection = os.path.join(samples, 'CD 1 - FAMOUS TSUMEGO COMPOSERS/CHO CHIKUN Encyclopedia Life And Death - Elementary')

        files = [os.path.join(collection, f) for f in os.listdir(collection)]

        if seed is None:
            numbers = set(get_solved_problems(collection))
            remaining = set(range(0, len(files))) - numbers
            print(f'🌝 Daily TSUMEGO ({len(numbers)}/{len(files)}) Challenge 🌚')
            seed = random.choice(list(remaining))

        game = read_sgf(files[seed])
        successful = create_position(game)

        if not successful:
            print(f'You dun GOOFED 🤡 !!')
            print('Try again? (Y/n)')
            yes = input('>>')
            if yes == 'y' or yes == '':
                main(seed)
            elif yes == 'n':
                insert_problem(collection, seed, successful)
                return 0
        else:
            print(f'You solved it, but still a 😹 !!')
            insert_problem(collection, seed, successful)
            return 0


if __name__ == '__main__':
    exit(main())
