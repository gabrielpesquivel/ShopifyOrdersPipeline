import os

# Paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INPUT_DIR = os.path.join(BASE_DIR, 'input_csv')
OUTPUT_DIR = os.path.join(BASE_DIR, 'output_sheet')
ASSETS_DIR = os.path.join(BASE_DIR, 'assets')
FONT_PATH = os.path.join(ASSETS_DIR, 'Arial_Bold.ttf')

# Page Specs (A4 in points)
MM_TO_PTS = 2.83465
PAGE_WIDTH = 210 * MM_TO_PTS
PAGE_HEIGHT = 297 * MM_TO_PTS
MARGIN = 10 * MM_TO_PTS
GAP = 5 * MM_TO_PTS  # Space between stickers

# Product Specs
# Add your specific product sizes here
SIZE_MAP = {
    'Small': {'font_size': 30, 'offset_mm': 1.5},
    'Medium': {'font_size': 50, 'offset_mm': 2.0},
    'Large': {'font_size': 80, 'offset_mm': 3.0}
}