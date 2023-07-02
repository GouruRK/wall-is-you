class Cell:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def get_coords(self) -> tuple[int, int]:
        return self.x, self.y

    def set_coords(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __add__(self, other: object) -> "Cell":
        if not isinstance(other, Cell):
            raise NotImplementedError
        return Cell(self.x + other.x, self.y + other.y)

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cell):
            raise NotImplementedError
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.get_coords())


class Character(Cell):
    def __init__(self, x: int, y: int, src: str, level: int = 1) -> None:
        super().__init__(x, y)
        self.level = level
        self.src = src
        self.tag_img = None
        self.tag_lvl = None

    def get_level(self) -> int:
        return self.level

    def set_level(self, value) -> None:
        self.level = value

    def set_tag_img(self, tag) -> None:
        self.tag_img = tag

    def get_tag_img(self) -> int:
        return self.tag_img

    def set_tag_lvl(self, tag) -> None:
        self.tag_lvl = tag

    def get_tag_lvl(self) -> int:
        return self.tag_lvl


class Dragon(Character):
    def __init__(self, y: int, x: int, level: int = 1) -> None:
        super().__init__(x, y, "./wall-is-you/assets/Dragon_s.png", level)


class Hero(Character):
    def __init__(self, y: int, x: int, level: int = 1) -> None:
        super().__init__(x, y, "./wall-is-you/assets/Knight_s.png", level)


class Treasure(Character):
    def __init__(self, y: int, x: int) -> None:
        super().__init__(x, y, "./wall-is-you/assets/Treasure.png")


class Room(Cell):
    def __init__(
        self, x: int, y: int, walls: int, character: "Character" = None
    ) -> None:
        super().__init__(x, y)
        self.character = character
        self.walls = walls
        self.lst_tag = []

    def add_character(self, character) -> None:
        if self.character is not None:
            return
        self.character = character
        self.character.set_coords(*self.get_coords())

    def remove_character(self) -> None:
        self.character = None

    def add_tag(self, tag) -> None:
        self.lst_tag.append(tag)

    def get_tag(self) -> int:
        return self.lst_tag

    def get_walls(self) -> int:
        return self.walls

    def get_character(self) -> "Character":
        return self.character

    def rotate(self) -> None:
        self.walls = rotate_right(self.get_walls())


Cells = list[Cell]
Rooms = list[Room]
Board = list[list[Room]]
Dragons = list[Dragon]
Trasures = list[Treasure]
Characters = list[Character]


class Game:
    def __init__(self, board: Board, hero: Hero, lst_dragons: Dragons) -> None:
        self.board = board
        self.hero = hero
        self.lst_dragons = sorted(
            lst_dragons, key=lambda d: d.get_level(), reverse=True
        )
        self.lst_treasure = []
        self.width = len(self.board[0])
        self.height = len(self.board)

    def __getitem__(self, index: tuple | int) -> Room:
        if isinstance(index, tuple):
            return self.board[index[1]][index[0]]
        return self.board[index]

    def __setitem__(self, index: int, value: "Character") -> None:
        self[index].add_character(value)

    def get_lst_dragons(self) -> Dragons:
        return self.lst_dragons

    def get_lst_treasure(self) -> Trasures:
        return self.lst_treasure

    def get_hero(self):
        return self.hero

    def add_char(self, char: "Character") -> None:
        if not isinstance(char, Character):
            raise NotImplementedError
        x, y = char.get_coords()
        self[y][x].add_character(char)
        if isinstance(char, Treasure):
            self.lst_treasure.append(char)

    def remove_char(self, char: "Character") -> None:
        if not isinstance(char, Character):
            raise NotImplementedError
        x, y = char.get_coords()
        self[y][x].remove_character()
        if isinstance(char, Dragon):
            self.get_lst_dragons().remove(char)
        elif isinstance(char, Treasure):
            self.get_lst_treasure().remove(char)

    def move_character(self, char: "Character", x: int, y: int) -> None:
        if not isinstance(char, Character):
            raise NotImplementedError
        self[char.get_coords()].remove_character()
        self[y][x].add_character(char)
        if isinstance(char, Treasure):
            self.update_lst_treasue()

    def is_win(self) -> bool:
        return not self.get_lst_dragons()

    def update_lst_treasure(self) -> None:
        lst = self.get_lst_treasure()
        x, y = self.get_hero().get_coords()
        lst.sort(key=lambda a: dist_room(self[y][x], self[a.get_coords()]))


def rotate_right(n, d: int = 1, nb_bits: int = 4) -> int:
    for _ in range(d):
        r = n & 1
        n = n >> 1
        n = n | r << (nb_bits - 1)
    return n


def dist_room(room1: Room, room2: Room) -> int:
    x1, y1 = room1.get_coords()
    x2, y2 = room2.get_coords()
    return (x2 - x1) ** 2 + (y2 - y1) ** 2
