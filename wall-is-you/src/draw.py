import src.fltk as fltk
from src.struct import *

CELL_WIDTH = 100
WIDTH = 10


def draw_edges(x: int, y: int) -> None:
    x *= CELL_WIDTH
    y *= CELL_WIDTH

    # drawing the top left corner
    fltk.rectangle(x, y, x + WIDTH, y + WIDTH * 2, remplissage="black")
    fltk.rectangle(x, y, x + WIDTH * 2, y + WIDTH, remplissage="black")

    # drawing the top right corner
    fltk.rectangle(
        x + CELL_WIDTH, y, x + CELL_WIDTH - WIDTH, y + WIDTH * 2, remplissage="black"
    )
    fltk.rectangle(
        x + CELL_WIDTH, y, x + CELL_WIDTH - WIDTH * 2, y + WIDTH, remplissage="black"
    )

    # drawing the bottom left corner
    fltk.rectangle(
        x, y + CELL_WIDTH, x + WIDTH, y + CELL_WIDTH - WIDTH * 2, remplissage="black"
    )
    fltk.rectangle(
        x, y + CELL_WIDTH, x + WIDTH * 2, y + CELL_WIDTH - WIDTH, remplissage="black"
    )

    # drawing the bottom right corner
    fltk.rectangle(
        x + CELL_WIDTH,
        y + CELL_WIDTH,
        x + CELL_WIDTH - WIDTH,
        y + CELL_WIDTH - WIDTH * 2,
        remplissage="black",
    )
    fltk.rectangle(
        x + CELL_WIDTH,
        y + CELL_WIDTH,
        x + CELL_WIDTH - WIDTH * 2,
        y + CELL_WIDTH - WIDTH,
        remplissage="black",
    )


def draw_room(room: Room) -> None:
    x, y = room.get_coords()
    x *= CELL_WIDTH
    y *= CELL_WIDTH
    walls = room.walls

    # drawing the up wall
    if not (walls & 8):
        room.add_tag(
            fltk.rectangle(x, y, x + CELL_WIDTH, y + WIDTH, remplissage="black")
        )

    # drawing the right wall
    if not (walls & 4):
        room.add_tag(
            fltk.rectangle(
                x + CELL_WIDTH,
                y,
                x + CELL_WIDTH - WIDTH,
                y + CELL_WIDTH - WIDTH,
                remplissage="black",
            )
        )

    # drawing the bottom wall
    if not (walls & 2):
        room.add_tag(
            fltk.rectangle(
                x,
                y + CELL_WIDTH,
                x + CELL_WIDTH,
                y + CELL_WIDTH - WIDTH,
                remplissage="black",
            )
        )

    # drawing the left wall
    if not (walls & 1):
        room.add_tag(
            fltk.rectangle(x, y, x + WIDTH, y + CELL_WIDTH, remplissage="black")
        )


def place_character(character: Character) -> None:
    x, y = character.get_coords()
    x *= CELL_WIDTH
    y *= CELL_WIDTH
    character.set_tag_img(
        fltk.image(
            x + CELL_WIDTH / 2,
            y + CELL_WIDTH / 2,
            character.src,
            ancrage="center",
            largeur=int(CELL_WIDTH * 70 / 100),
            hauteur=int(CELL_WIDTH * 70 / 100),
        )
    )
    if not isinstance(character, Treasure):
        character.set_tag_lvl(
            fltk.texte(
                x + WIDTH * 2, y + WIDTH, character.get_level(), "red", taille=12
            )
        )


def place_lst_char(lst_character: Characters = None) -> None:
    for character in lst_character:
        place_character(character)


def draw_game(game: Game) -> None:
    for y in range(game.height):
        for x in range(game.width):
            draw_edges(x, y)
            draw_room(game[y][x])

    place_lst_char(game.lst_dragons)
    place_character(game.get_hero())


def erase_lst_tag(lst_tag: list[int]) -> None:
    for tag in lst_tag:
        fltk.efface(tag)


def erase_character(character: Character) -> None:
    fltk.efface(character.get_tag_img())
    fltk.efface(character.get_tag_lvl())
    character.set_tag_img(None)
    character.set_tag_lvl(None)


def erase_lst_character(lst_character: Characters) -> None:
    for character in lst_character:
        erase_character(character)


def erase_room(room: Room) -> None:
    for wall_tag in room.get_tag():
        fltk.efface(wall_tag)


def draw_path(lst_rooms: Rooms) -> list[int]:
    lst_tag = []
    for i in range(len(lst_rooms) - 1):
        x1, y1 = lst_rooms[i].get_coords()
        x2, y2 = lst_rooms[i + 1].get_coords()
        lst_tag.append(
            fltk.ligne(
                x1 * CELL_WIDTH + CELL_WIDTH / 2,
                y1 * CELL_WIDTH + CELL_WIDTH / 2,
                x2 * CELL_WIDTH + CELL_WIDTH / 2,
                y2 * CELL_WIDTH + CELL_WIDTH / 2,
                couleur="red",
            )
        )
    return lst_tag


def write_centred_text(x: int, y: int, text: str, **kwargs) -> None:
    width, height = fltk.taille_texte(text)
    fltk.texte(x - len(text) - width / 2, y - height / 2, text, **kwargs)


def write_result(game: Game) -> None:
    x = game.width * CELL_WIDTH / 2
    y = game.height * CELL_WIDTH / 2

    text = "Defaite !"
    color = "red"
    if game.is_win():
        text = "Victoire !"
        color = "green"

    write_centred_text(x, y, text, couleur=color)
