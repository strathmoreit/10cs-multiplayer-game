
from PIL import Image
from collections import deque

INPUT_FILE = "assets/player_sheet.png"
OUTPUT_FILE = "assets/player_sheet_clean.png"

# Sprite sheet layout
FRAME_WIDTH = 60
FRAME_COUNT = 9

# Original palette colours
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Cleanup settings
COLOUR_TOLERANCE = 45
MIN_ALPHA = 10

# Only treat nearly transparent or nearly black
# pixels as potential background.
BACKGROUND_RGB_LIMIT = 8
BACKGROUND_ALPHA_LIMIT = 40


def close_to(colour, target):
    return all(
        abs(colour[i] - target[i]) <= COLOUR_TOLERANCE
        for i in range(3)
    )


def clean_colours(image):
    pixels = image.load()
    changed = 0
    transparent = 0

    for y in range(image.height):
        for x in range(image.width):
            r, g, b, a = pixels[x, y]

            if a < MIN_ALPHA:
                if a != 0:
                    transparent += 1
                pixels[x, y] = (0, 0, 0, 0)
                continue

            rgb = (r, g, b)

            if close_to(rgb, RED):
                pixels[x, y] = (*RED, a)
                changed += 1

            elif close_to(rgb, BLUE):
                pixels[x, y] = (*BLUE, a)
                changed += 1

    return changed, transparent


def remove_background(image, left, right):
    """
    Flood-fill background pixels connected to the
    boundary of one animation frame.
    """

    pixels = image.load()
    height = image.height

    visited = set()
    queue = deque()

    def is_background(x, y):
        r, g, b, a = pixels[x, y]

        return (
            a <= BACKGROUND_ALPHA_LIMIT
            or (
                r <= BACKGROUND_RGB_LIMIT
                and g <= BACKGROUND_RGB_LIMIT
                and b <= BACKGROUND_RGB_LIMIT
                and a < 255
            )
        )

    # Start from frame boundaries
    for x in range(left, right):
        for y in (0, height - 1):
            if is_background(x, y):
                queue.append((x, y))

    for y in range(height):
        for x in (left, right - 1):
            if is_background(x, y):
                queue.append((x, y))

    removed = 0

    while queue:
        x, y = queue.popleft()

        if (x, y) in visited:
            continue

        if not (left <= x < right and 0 <= y < height):
            continue

        visited.add((x, y))

        if not is_background(x, y):
            continue

        if pixels[x, y][3] != 0:
            removed += 1

        pixels[x, y] = (0, 0, 0, 0)

        queue.extend([
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ])

    return removed


# Load original image
image = Image.open(INPUT_FILE).convert("RGBA")

print("Original size:", image.size)

# Step 1: Standardise palette colours
changed, transparent = clean_colours(image)

# Step 2: Remove background artefacts
removed = 0

for frame in range(FRAME_COUNT):
    left = frame * FRAME_WIDTH
    right = min(left + FRAME_WIDTH, image.width)

    if left >= image.width:
        break

    removed += remove_background(image, left, right)

# Save
image.save(OUTPUT_FILE)

print("Saved:", OUTPUT_FILE)
print("Palette pixels standardised:", changed)
print("Faint pixels removed:", transparent)
print("Background pixels removed:", removed)
print("Final size:", image.size)
