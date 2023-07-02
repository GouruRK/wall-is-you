# wall-is-you
___

- [wall-is-you](#wall-is-you)
  - [Presentation](#presentation)
  - [Install](#install)
  - [Game purpose](#game-purpose)
  - [Controls](#controls)

## Presentation
This is the final project of python for first years students at [Université Gustave Eiffel](https://www.univ-gustave-eiffel.fr/) of 2022-2023.

## Install

To install this little project, use the command
```
git clone https://github.com/GouruRK/wall-is-you.git
cd wall-is-you
```
Once on the `wall-is-you` folder, launch it using 
```
python3 wall-is-you [map] 
```
and give a map path from the `maps` folder.

*Note that windows users should use the `py` command instead of `python3`*

## Game purpose

The goal of the Hero is to clear the map by killing all dragons. The Hero can only attack a dragon if there is a path between them. You can rotate a room by `clicking` on it. If the Hero can kill multiples dragons, it target the dragon with the higher level. User can place a treasure by using `right click`, which has a higher priority than any other dragons.
Hero follow the path by pressing the "`space`" key.

## Controls

* `Right click` : Place a treasure
* `Left click` : Rotate a room
* `Space` : follow the showing path
