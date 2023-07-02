from src.struct import *

COORDS = [Cell(0, -1), Cell(1, 0), Cell(0, 1), Cell(-1, 0)]


def get_neighbors(x: int, y: int) -> Cells:
    cell = Cell(x, y)
    return [cell + c for c in COORDS]


def is_cell_in_board(board: Game, cell: Cell) -> bool:
    x, y = cell.get_coords()
    return 0 <= x < board.width and 0 <= y < board.height


def get_valid_neighbors(board: Game, x: int, y: int) -> Cells:
    neighbors = get_neighbors(x, y)
    return list(filter(lambda c: is_cell_in_board(board, c), neighbors))


def cell_to_room(board: Game, lst_cell: Cells) -> Rooms:
    return [board[y][x] for x, y in list(map(lambda c: c.get_coords(), lst_cell))]


def get_neighbors_room(board: Game, x: int, y: int) -> Rooms:
    return cell_to_room(board, get_valid_neighbors(board, x, y))


def det_dir(src: Room, dest: Room) -> int:
    x1, y1 = src.get_coords()
    x2, y2 = dest.get_coords()
    if x1 == x2:
        if y1 < y2:
            return 0b10  # bottom
        return 0b1000  # top
    if y1 == y2:
        if x1 < x2:
            return 0b100  # right
        return 0b1  # left


def can_communicate(src: Room, dest: Room) -> bool:
    return src.walls & rotate_right(dest.walls, 2) & det_dir(src, dest)


def can_affront(hero: Hero, dragon: Dragon):
    return dragon.get_level() <= hero.get_level()


def next_level(hero: Hero, dragon: Dragon):
    hero_lvl = hero.get_level()
    dragon_lvl = dragon.get_level()
    if hero_lvl >= dragon_lvl:
        return hero_lvl + 1
    return -1
