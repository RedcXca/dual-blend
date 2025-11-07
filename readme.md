## dual-blend

Utilizes the classic "white print / black print" layer trick to merge a light-source image and a dark-source image into one RGBA asset.
Essentially, it is able to display two completely different images on a white vs black background.

<img width="1224" height="1030" alt="image" src="https://github.com/user-attachments/assets/357d5ea4-c925-41db-87f5-3cdab1146ad6" />

### Requirements
- Python 3.9+
- Pillow
- NumPy

Install dependencies with:
```
pip install pillow numpy
```

### Usage
```
python main.py WHITE_IMAGE BLACK_IMAGE [OUTPUT_IMAGE] [--width WIDTH] [--height HEIGHT]
```

- `WHITE_IMAGE` – path to the light/highlight version.
- `BLACK_IMAGE` – path to the shadow/dark version.
- `OUTPUT_IMAGE` – optional path for the result; defaults to `blended.png`.
- `--width` / `--height` – optional dimensions; omit to keep the black image's size.

Example:
```
python main.py whitecat.png blackcat.png combined.png --width 1024 --height 768
```

### Notes
- The processing assumptions work best when, at most pixels, the dark image is not brighter than the white image. If your sources already satisfy this constraint, you can adjust or remove the pre-blend clipping in `main.py` to have a less "washed out" final output.
 - Credits to [Ilmari Karonen](https://graphicdesign.stackexchange.com/users/3239/ilmari-karonen) for the original workflow described in [this answer](https://graphicdesign.stackexchange.com/a/9122).
