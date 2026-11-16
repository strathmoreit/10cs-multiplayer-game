# A script to remove artifacts from the player sprite sheet that makes recolouring messy

from PIL import Image

INPUT_FILE = "assets/player_sheet.png"
OUTPUT_FILE = "assets/player_sheet_clean.png"

# Standard colours for palette swapping
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# How close a colour must be to pure red or blue
TOLERANCE = 45


def close_to(color, target):
    return all(
        abs(color[i] - target[i]) <= TOLERANCE
        for i in range(3)
    )


image = Image.open(INPUT_FILE).convert("RGBA")
pixels = image.load()

red_changed = 0
blue_changed = 0

for y in range(image.height):
    for x in range(image.width):
        r, g, b, a = pixels[x, y]

        # Leave fully transparent pixels alone
        if a == 0:
            continue

        rgb = (r, g, b)

        if close_to(rgb, RED):
            pixels[x, y] = (*RED, a)
            red_changed += 1

        elif close_to(rgb, BLUE):
            pixels[x, y] = (*BLUE, a)
            blue_changed += 1

image.save(OUTPUT_FILE)

print("Saved:", OUTPUT_FILE)
print("Red pixels processed:", red_changed)
print("Blue pixels processed:", blue_changed)
print("Image size:", image.size)
