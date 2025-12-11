from reportlab.pdfgen import canvas
from reportlab.lib.colors import CMYKColor

def setup_canvas(output_path, page_size):
    c = canvas.Canvas(output_path, pagesize=page_size)
    return c

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