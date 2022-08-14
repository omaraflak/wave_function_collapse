import os
import cv2
import numpy as np
from numpy.typing import NDArray
from wfc.wave_function_collapse import Constraint, Tile, generate


def read_image(filepath: str) -> NDArray:
    return cv2.imread(filepath, cv2.IMREAD_COLOR)


def make_tile(filepath: str) -> Tile:
    filename = os.path.basename(filepath)
    uid, constraints_str = filename.split('.')[0].split('_')
    assert len(constraints_str) % 4 == 0
    sockets = len(constraints_str) // 4
    constraint = Constraint(*[
        constraints_str[i:i+sockets]
        for i in range(0, len(constraints_str), sockets)
    ])
    return Tile(uid, constraint)


def build_image(images: dict[str, NDArray], ids: list[list[str]]) -> NDArray:
    height, width, depth = images[next(iter(images.keys()))].shape
    tiles_h, tiles_w = len(ids), len(ids[0])
    output = np.zeros((tiles_h * height, tiles_w * width, depth))
    for i in range(tiles_h):
        for j in range(tiles_w):
            output[i * height:i * height + height, j * width:j * width + width] = images[ids[i][j]]
    return output


def rotate_tile_and_image(tile: Tile, image: NDArray, rotation: int) -> tuple[Tile, NDArray]:
    constraint = tile.constraint
    for _ in range(rotation):
        image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        constraint = Constraint(
            constraint.left[::-1],
            constraint.top,
            constraint.right[::-1],
            constraint.bottom
        )
    return Tile(f"{tile.uid}#{rotation}", constraint), image


def get_tiles_and_images(files: list[str]) -> tuple[dict[str, Tile], dict [str, NDArray]]:
    files_to_tiles = {file: make_tile(file) for file in files}
    tiles = {tile.uid: tile for tile in files_to_tiles.values()}
    images = {files_to_tiles[file].uid: read_image(file) for file in files}
    for tile in list(tiles.values()):
        for i in range(3):
            rotated_tile, rotated_image = rotate_tile_and_image(tile, images[tile.uid], i + 1)
            tiles[rotated_tile.uid] = rotated_tile
            images[rotated_tile.uid] = rotated_image
    return tiles, images


def main():
    dir = 'images/tracks'
    files = [os.path.join(dir, path) for path in os.listdir(dir)]
    tiles, images = get_tiles_and_images(files)
    output = build_image(images, generate(tiles, 20, 20))
    cv2.imwrite(f'output/{os.path.basename(dir)}.png', output)

if __name__ == '__main__':
    main()