import src.draw as draw
from src.draw import CELL_WIDTH
from src.struct import *
import src.tools as tools


def mouse_to_coords(x: int, y: int) -> tuple[int, int]:
    return x // CELL_WIDTH, y // CELL_WIDTH


def rotate_room(game: Game, x: int, y: int) -> None:
    room = game[y][x]
    room.rotate()

    draw.erase_room(room)
    draw.draw_room(room)


def rotate_room_on_click(game: Game, x: int, y: int) -> None:
    rotate_room(game, *mouse_to_coords(x, y))


def fight(game: Game, dragon: Dragon) -> None:
    hero = game.get_hero()

    draw.erase_character(dragon)
    draw.erase_character(hero)

    hero.set_level(tools.next_level(hero, dragon))

    game.remove_char(dragon)
    game.move_character(hero, *dragon.get_coords())

    draw.place_character(hero)


def add_treasure(game: Game, x: int, y: int) -> None:
    room = game[y][x]
    character = room.get_character()
    if character is not None:
        if isinstance(character, Treasure):
            draw.erase_character(character)
            game.remove_char(character)
            game.update_lst_treasure()
        return
    treasure = Treasure(y, x)
    draw.place_character(treasure)
    game.add_char(treasure)
    game.update_lst_treasure()


def add_trasure_on_click(game: Game, x: int, y: int) -> None:
    add_treasure(game, *mouse_to_coords(x, y))


def capture_treasure(game: Game, treasure: Treasure) -> None:
    hero = game.get_hero()

    draw.erase_character(hero)
    draw.erase_character(treasure)

    game.remove_char(treasure)
    game.move_character(hero, *treasure.get_coords())
    game.update_lst_treasure()

    draw.place_character(hero)
