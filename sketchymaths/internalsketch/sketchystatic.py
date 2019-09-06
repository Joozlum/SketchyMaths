from math import atan2, cos, sin


def get_angles(x, y):
    angle = atan2(y, x)
    angle1 = cos(angle + .3)
    angle2 = sin(angle + .3)
    angle3 = cos(angle - .3)
    angle4 = sin(angle - .3)
    return angle1, angle2, angle3, angle4

def process_connections(inst1, inst2):
    """
    Takes in two instances and using their position properties determines what
    points to use to draw a line between them along with an arrow

    :param inst1:
    :param inst2:
    :return: List of points to draw a line through
    """
    x_change = inst2.center_x - inst1.center_x
    y_change = inst2.center_y - inst1.center_y
    if abs(x_change) > abs(y_change):
        y1 = inst1.center_y
        y2 = inst2.center_y
        if x_change > 0:
            x1 = inst1.right
            x2 = inst2.x
        else:
            x1 = inst1.x
            x2 = inst2.right
    else:
        x1 = inst1.center_x
        x2 = inst2.center_x
        if y_change > 0:
            y1 = inst1.top
            y2 = inst2.y
        else:
            y1 = inst1.y
            y2 = inst2.top

    #  calculating points to create arrow:
    x0 = round(x2 - x1)
    y0 = round(y2 - y1)
    pcos, psin, ncos, nsin = get_angles(x0, y0)
    ax = -10 * pcos + x2
    ay = -10 * psin + y2
    bx = -10 * ncos + x2
    by = -10 * nsin + y2

    return x1, y1, x2, y2, ax, ay, bx, by, x2, y2