from src.struct import *
from collections import deque
import src.tools as tools


def solve_backtracking(
    game: Game, start: Room, finish: Room, done: set = None
) -> tuple[bool, Rooms]:
    if done is None:
        done = set()

    if start == finish:
        return True, [start]

    h = hash(start)

    if h in done:
        return False, []

    if isinstance(start.character, Dragon):
        return False, []

    done.add(h)

    for r in tools.get_neighbors_room(game, *start.get_coords()):
        if tools.can_communicate(start, r):
            res, path = solve_backtracking(game, r, finish, done)
            if res:
                return True, [start] + path

    return False, []


def breadth_first_search(game: Game, start: Room, finish: Room) -> tuple[bool, Rooms]:
    done = set()
    lst = deque([[start]])

    while len(lst):
        path = lst.popleft()
        room = path[-1]

        if room == finish:
            return True, path
        if isinstance(room.character, Dragon):
            continue

        h = hash(room)

        if h not in done:
            done.add(h)
            for r in tools.get_neighbors_room(game, *room.get_coords()):
                if tools.can_communicate(room, r):
                    lst.append(path + [r])
    return False, []


def solve_for_list(
    game: Game, solve_f: callable, list: Characters
) -> tuple[None | Dragon, Rooms]:
    hero = game.get_hero()
    for character in list:
        res, path = solve_f(
            game,
            game[hero.get_coords()],
            game[character.get_coords()],
        )
        if res:
            return character, path
    return None, []


def solve(game: Game, solve_f: callable) -> tuple[None | Dragon, Rooms]:
    res, path = solve_for_list(game, solve_f, game.get_lst_treasure())
    if not res:
        res, path = solve_for_list(game, solve_f, game.get_lst_dragons())
    return res, path
