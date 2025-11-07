# algorithm credits: https://graphicdesign.stackexchange.com/a/9122

import argparse
import sys
from PIL import Image
import numpy as np
import os

# saves an image, mode is L/RGB/RGBA
def save_image(arr, mode, path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    if arr.dtype != np.uint8:
        arr = np.clip(arr, 0.0, 1.0)
        arr = (arr * 255).astype(np.uint8)
    Image.fromarray(arr, mode).save(path)

def dual_blend(WHITE_IMAGE_PATH, BLACK_IMAGE_PATH, output_path, width=None, height=None):
    if not os.path.exists(WHITE_IMAGE_PATH) or not os.path.exists(BLACK_IMAGE_PATH):
        return

    try:
        # convert images to grayscale
        white_image = Image.open(WHITE_IMAGE_PATH).convert('L')
        black_image = Image.open(BLACK_IMAGE_PATH).convert('L')

        # resize dimensions defaults to black's size
        if width is None or height is None:
            width, height = black_image.size
        white_resized = white_image.resize((width, height), Image.NEAREST)
        black_resized = black_image.resize((width, height), Image.NEAREST)

        # convert to numpy arrays of brightness values
        white = np.array(white_resized, dtype=np.float32) / 255.0
        black = np.array(black_resized, dtype=np.float32) / 255.0

        # some adjustments to the images to make them more compatible
        # can be removed if original images already have good contrast
        # and satisfy the condition that black <= white mostly
        black = 0.6 * black
        white = 0.2 + 0.8 * white
        white = np.clip(white, 0.4, 1.0)
        black = np.clip(black, 0.0, 0.4)

        # must be satisfied that black <= white
        black = np.minimum(black, white)

        # compute transparency from white and black layers
        valid_mask = black <= white
        alpha = np.where(valid_mask, 1.0 - white + black, 1.0 - white)

        # recover luminance using the computed transparency
        luminance = np.zeros_like(black)
        safe_mask = valid_mask & (alpha != 0)
        np.divide(black, alpha, out=luminance, where=safe_mask)
        luminance = np.clip(luminance, 0.0, 1.0)

        # create final image
        final_luminance = (luminance * 255).astype(np.uint8)
        final_alpha = (alpha * 255).astype(np.uint8)
        R = Image.fromarray(final_luminance, mode='L')
        final_img = Image.merge('RGBA', (R, R, R, Image.fromarray(final_alpha, mode='L')))
        final_img.save(output_path)

    except Exception:
        pass

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("white_image")
    parser.add_argument("black_image")
    parser.add_argument("output_image", nargs="?")
    parser.add_argument("--width", type=int)
    parser.add_argument("--height", type=int)

    args = parser.parse_args()

    output_path = args.output_image or "blended.png"

    dual_blend(
        WHITE_IMAGE_PATH=args.white_image,
        BLACK_IMAGE_PATH=args.black_image,
        output_path=output_path,
        width=args.width,
        height=args.height,
    )


if __name__ == '__main__':
    main()