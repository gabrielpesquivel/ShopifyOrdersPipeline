import os
import pandas as pd
from shapely import affinity
from reportlab.lib.colors import CMYKColor

from src import config, geometry, pdf_utils, layout
import re

def determine_size_category(text):
    """
    Determine size category based on text content according to asset_specs.md:
    - Flags: 6mm
    - Symbols: 10mm
    - Initials + Numbers: 5mm (1-2 characters)
    - Dates + Words over 3 characters: 4mm
    """
    text = text.strip()

    # Check for flag emojis (country flags are in range U+1F1E6-U+1F1FF)
    if any('\U0001F1E6' <= char <= '\U0001F1FF' for char in text):
        return 'Flags'

    # Check for symbols (single character that's not alphanumeric)
    if len(text) == 1 and not text.isalnum():
        return 'Symbols'

    # Check for initials or numbers (1-2 characters of letters/numbers)
    if len(text) <= 2 and text.replace(' ', '').isalnum():
        return 'Initials'

    # Everything else (dates, words over 3 characters)
    return 'Words'

def process_orders():
    # 1. Find CSV files
    input_files = [f for f in os.listdir(config.INPUT_DIR) if f.endswith('.csv')]
    
    if not input_files:
        print("No CSV files found in input_csv/")
        return

    for csv_file in input_files:
        print(f"Processing {csv_file}...")
        
        # Setup paths
        input_path = os.path.join(config.INPUT_DIR, csv_file)
        output_filename = csv_file.replace('.csv', '_gangsheet.pdf')
        output_path = os.path.join(config.OUTPUT_DIR, output_filename)
        
        # Load Data
        df = pd.read_csv(input_path)
        
        # Setup PDF
        c = pdf_utils.setup_canvas(output_path, (config.PAGE_WIDTH, config.PAGE_HEIGHT))
        layout_mgr = layout.LayoutManager(c)
        
        # Process Rows
        for index, row in df.iterrows():
            # Parse the lineitem name (format: "Category - TEXT / COLOR")
            lineitem_name = str(row.get('Lineitem name', ''))

            # Extract the text part (between the dash and slash, or the whole name if no slash)
            if ' - ' in lineitem_name:
                text = lineitem_name.split(' - ', 1)[1]  # Get everything after first " - "
                if ' / ' in text:
                    text = text.split(' / ')[0]  # Get everything before " / "
            else:
                text = lineitem_name

            # Skip items we don't want to print (like Priming Wipe)
            if not text or text.strip() == '' or 'Priming Wipe' in lineitem_name:
                continue

            # Determine size category based on text content
            size = determine_size_category(text)
            qty = int(row.get('Lineitem quantity', 1))

            # Get Config for this size
            size_cfg = config.SIZE_MAP.get(size, config.SIZE_MAP['Words'])
            
            # Generate Geometry (Once per unique design)
            # Optimization: If many rows have same text/size, you could cache this
            text_geo, bg_geo, w, h = geometry.create_sticker_geometry(
                text, config.FONT_PATH, size_cfg
            )
            
            # Add to Sheet (Repeat for Quantity)
            for _ in range(qty):
                # Get Position
                x, y = layout_mgr.add_item(w, h)
                
                # Move Geometry to Position
                final_text = affinity.translate(text_geo, xoff=x, yoff=y)
                final_bg = affinity.translate(bg_geo, xoff=x, yoff=y)
                
                # Draw Background (White 4% opacity)
                # CMYK(0,0,0,0) is white
                pdf_utils.draw_shapely_poly(c, final_bg, CMYKColor(0,0,0,0), alpha=0.04)

                # Draw Text (Black #221f1f - RGB(34,31,31) = CMYK(0,0.09,0.09,0.87))
                pdf_utils.draw_shapely_poly(c, final_text, CMYKColor(0, 0.09, 0.09, 0.87), alpha=1.0)

        # Save PDF
        c.save()
        print(f"Saved: {output_path}")

if __name__ == "__main__":    
    if not os.path.exists(config.FONT_PATH):
        print(f"ERROR: Font not found at {config.FONT_PATH}")
        print("Please place a .ttf file in the assets folder.")
    else:
        process_orders()