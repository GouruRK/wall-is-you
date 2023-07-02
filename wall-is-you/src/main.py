import src.fltk as fltk
import src.draw as draw
from src.draw import CELL_WIDTH
import src.parse as parse
import src.tools as tools
from src.struct import *
import src.solve as solve
import src.interract as interract


def main(path) -> None:
    game = Game(*parse.parse(path))
    target, path = solve.solve(game, solve.breadth_first_search)

    fltk.cree_fenetre(game.width * CELL_WIDTH, game.height * CELL_WIDTH)
    draw.draw_game(game)
    lst_tag_path = draw.draw_path(path)

    tev = None
    while tev != "Quitte" and not game.is_win():
        ev = fltk.donne_ev()
        tev = fltk.type_ev(ev)

        if tev == "ClicGauche":
            interract.rotate_room_on_click(
                game, fltk.abscisse_souris(), fltk.ordonnee_souris()
            )

            target, path = solve.solve(game, solve.breadth_first_search)
            draw.erase_lst_tag(lst_tag_path)
            lst_tag_path = draw.draw_path(path)
        elif tev == "ClicDroit":
            interract.add_trasure_on_click(
                game, fltk.abscisse_souris(), fltk.ordonnee_souris()
            )

            draw.erase_lst_tag(lst_tag_path)
            target, path = solve.solve(game, solve.breadth_first_search)
            lst_tag_path = draw.draw_path(path)
        elif tev == "Touche":
            touche = fltk.touche(ev)
            if touche == "space" and path:
                if isinstance(target, Dragon):
                    if tools.can_affront(game.get_hero(), target):
                        interract.fight(game, target)

                        draw.erase_lst_tag(lst_tag_path)
                    else:
                        break
                elif isinstance(target, Treasure):
                    interract.capture_treasure(game, target)

                draw.erase_lst_tag(lst_tag_path)
                target, path = solve.solve(game, solve.breadth_first_search)
                lst_tag_path = draw.draw_path(path)
            elif touche == "s":
                parse.save(game)

        fltk.mise_a_jour()

    if tev != "Quitte":
        fltk.efface_tout()
        draw.write_result(game)
        fltk.attend_ev()

    fltk.ferme_fenetre()
