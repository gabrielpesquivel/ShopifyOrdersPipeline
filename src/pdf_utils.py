from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor, magenta

def setup_canvas(output_path, page_size):
    c = canvas.Canvas(output_path, pagesize=page_size)
    return c

def draw_cutting_rectangle(c, x, y, width, height):
    """
    Draw a thin magenta rectangle for cutting machine.

    Args:
        c: ReportLab canvas
        x: Bottom-left x coordinate in points
        y: Bottom-left y coordinate in points
        width: Rectangle width in points
        height: Rectangle height in points
    """
    c.saveState()
    c.setStrokeColor(magenta)  # Magenta color for cutting machine
    c.setLineWidth(0.5)  # Thin line (0.5 points)
    c.rect(x, y, width, height, fill=0, stroke=1)
    c.restoreState()

def draw_shapely_poly(c, poly, color, alpha=1.0):
    """Draws a Shapely polygon onto the ReportLab canvas."""
    path = c.beginPath()
    
    # Handle both Polygon and MultiPolygon
    if poly.geom_type == 'Polygon':
        geoms = [poly]
    else:
        geoms = poly.geoms

    for p in geoms:
        x, y = p.exterior.xy
        path.moveTo(x[0], y[0])
        for i in range(1, len(x)):
            path.lineTo(x[i], y[i])
        path.close()
        
        # Handle holes (like inside 'O')
        for interior in p.interiors:
            xi, yi = interior.xy
            path.moveTo(xi[0], yi[0])
            for i in range(1, len(xi)):
                path.lineTo(xi[i], yi[i])
            path.close()

    c.saveState()
    c.setFillAlpha(alpha)
    c.setFillColor(color)
    c.drawPath(path, fill=1, stroke=0)
    c.restoreState()