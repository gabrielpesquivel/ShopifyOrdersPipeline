from . import config

class LayoutManager:
    def __init__(self, canvas_obj):
        self.c = canvas_obj
        self.cursor_x = config.MARGIN
        self.cursor_y = config.PAGE_HEIGHT - config.MARGIN
        self.row_height = 0
        self.page_count = 1

    def add_item(self, width, height):
        """
        Calculates position for next item. 
        Returns (x, y) or triggers new page if full.
        """
        # Check if item fits in current row
        if self.cursor_x + width > config.PAGE_WIDTH - config.MARGIN:
            # Move to next row
            self.cursor_x = config.MARGIN
            self.cursor_y -= (self.row_height + config.GAP)
            self.row_height = 0

        # Check if item fits on page vertically
        if self.cursor_y - height < config.MARGIN:
            # New Page
            self.c.showPage()
            self.page_count += 1
            self.cursor_x = config.MARGIN
            self.cursor_y = config.PAGE_HEIGHT - config.MARGIN
            self.row_height = 0

        # Calculate draw position
        # cursor_y is the TOP of the row, so we draw down from there
        draw_x = self.cursor_x
        draw_y = self.cursor_y - height

        # Update cursor for next item
        self.cursor_x += width + config.GAP
        if height > self.row_height:
            self.row_height = height
            
        return draw_x, draw_y