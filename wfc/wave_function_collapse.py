from random import choice, randrange, shuffle
from dataclasses import dataclass
from typing import Optional


@dataclass
class Constraint:
    top: str
    right: str
    bottom: str
    left: str


@dataclass
class TmpConstraint:
    top: Optional[str] = None
    right: Optional[str] = None
    bottom: Optional[str] = None
    left: Optional[str] = None


@dataclass
class Tile:
    uid: str
    constraint: Constraint


def _make_constraint(
    output: list[list[str]],
    tiles: dict[str, Tile],
    i: int,
    j: int
) -> TmpConstraint:
    constraint = TmpConstraint()
    h, w = len(output), len(output[0])

    if i - 1 >= 0 and output[i - 1][j] != '':
        constraint.top = tiles[output[i - 1][j]].constraint.bottom
    
    if j + 1 < w and output[i][j + 1] != '':
        constraint.right = tiles[output[i][j + 1]].constraint.left
    
    if i + 1 < h and output[i + 1][j] != '':
        constraint.bottom = tiles[output[i + 1][j]].constraint.top
    
    if j - 1 >= 0 and output[i][j - 1] != '':
        constraint.left = tiles[output[i][j - 1]].constraint.right

    return constraint


def _match_constraint(tile: Tile, constraint: TmpConstraint) -> bool:
    copy = Constraint(
        constraint.top or tile.constraint.top,
        constraint.right or tile.constraint.right,
        constraint.bottom or tile.constraint.bottom,
        constraint.left or tile.constraint.left,
    )
    return tile.constraint == copy


def generate(tiles: dict[str, Tile], width: int, height: int) -> list[list[str]]:
    def _generate(output: list[list[str]]) -> Optional[list[list[str]]]:
        cells = [(i, j) for i in range(height) for j in range(width) if output[i][j] == '']
        if not cells:
            return output

        least_entropy_cell: tuple[int, int] = (-1, -1) 
        least_entropy = len(tiles) + 1
        candidates: list[Tile] = []

        for i, j in cells:
            constraint = _make_constraint(output, tiles, i, j)
            _candidates = [tile for tile in tiles.values() if _match_constraint(tile, constraint)]

            if len(_candidates) < least_entropy:
                least_entropy = len(_candidates)
                candidates = _candidates
                least_entropy_cell = (i, j)
        
        if not candidates:
            return None

        shuffle(candidates)
        for candidate in candidates:
            output[least_entropy_cell[0]][least_entropy_cell[1]] = candidate.uid
            result = _generate(output)
            if result is not None:
                return result

        output[least_entropy_cell[0]][least_entropy_cell[1]] = ''
        return None

    result = [['' for _ in range(width)] for _ in range(height)]
    result[randrange(height)][randrange(width)] = choice(list(tiles.values())).uid
    return _generate(result)