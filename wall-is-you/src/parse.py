from src.struct import *

CELL_REPR = {
    "╞": 1,  # 1  -> 0001
    "╥": 2,  # 2  -> 0010
    "╗": 3,  # 3  -> 0011
    "╡": 4,  # 4  -> 0100
    "═": 5,  # 5  -> 0101
    "╔": 6,  # 6  -> 0110
    "╦": 7,  # 7  -> 0111
    "╨": 8,  # 8  -> 1000
    "╝": 9,  # 9  -> 1001
    "║": 10,  # 10 -> 1010
    "╣": 11,  # 11 -> 1011
    "╚": 12,  # 12 -> 1100
    "╩": 13,  # 13 -> 1101
    "╠": 14,  # 14 -> 1110
    "╬": 15,  # 15 -> 1111
}


CELL_REPR_INV = {value: key for key, value in CELL_REPR.items()}


def parse_map(file) -> tuple[Board, Characters]:
    board = []
    lst_char = []
    y = 0
    for line in file:
        x = 0
        line = line.rstrip()
        res_line = []
        if line[0] not in CELL_REPR:
            line = line.split()
            infos = list(map(int, line[1:]))
            if line[0] == "D":
                char = Dragon
            elif line[0] == "A":
                char = Hero
            else:
                raise ValueError
            lst_char.append(char(*infos))
        else:
            for car in line:
                res_line.append(Room(x, y, CELL_REPR[car]))
                x += 1
            y += 1
            board.append(res_line)
    return board, lst_char


def add_character_room(board: Board, character: Character) -> None:
    x, y = character.get_coords()
    board[y][x].add_character(character)


def add_list_character_room(board: Board, lst_character: Characters) -> None:
    for c in lst_character:
        add_character_room(board, c)


def parse(path: str) -> tuple[Board, Hero, Dragons]:
    with open(path, "r", encoding="utf-8") as file:
        board, lst_char = parse_map(file)

    hero = lst_char[0]
    lst_dragons = lst_char[1:]
    add_character_room(board, hero)
    add_list_character_room(board, lst_dragons)
    return board, hero, lst_dragons


def save(game: Game) -> None:
    with open("./assets/maps/save.txt", "w", encoding="utf-8") as file:
        for y in range(game.height):
            for x in range(game.width):
                file.write(CELL_REPR_INV[game[y][x].get_walls()])
            file.write("\n")

        hero = game.get_hero()
        x, y = hero.get_coords()
        file.write(f"A {y} {x} {hero.get_level()}\n")

        for dragon in game.get_lst_dragons():
            x, y = dragon.get_coords()
            file.write(f"D {y} {x} {dragon.get_level()}\n")
