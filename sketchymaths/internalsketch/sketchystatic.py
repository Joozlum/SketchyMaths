from math import atan2, cos, sin


def translate_color_config(color_string: str):
    x = color_string.split(',')
    y = []
    for i in range(len(x)):
        try:
            y.append(float(x[i]))
        except TypeError:
            print("TypeError, setting value to 1!\nTo fix this change improper setting!")
            y.append(1.0)
        except ValueError:
            print("ValueError, setting value to 1!\nTo fix this change improper setting!")
            y.append(1.0)

    for i in range(len(y)):
        y[i] = adjust_color_input(y[i])
    if len(y) != 3:
        print("Error, too many colors!  Should only be 3, (r, g, b), not {}!".format(len(y)))
        print("Using default [1, 1, 1] until you change it!")
        y = [1, 1, 1]
    return y

def adjust_color_input(color):
    if type(color) is float or int:
        if color <= 0:
            return 0.0
        elif color <= 1:
            return color
        elif color > 1:
            return 255/color
    return 1

def get_angles(x, y):
    angle = atan2(y, x)
    angle1 = cos(angle + .3)
    angle2 = sin(angle + .3)
    angle3 = cos(angle - .3)
    angle4 = sin(angle - .3)
    return angle1, angle2, angle3, angle4

def process_connections(inst2, inst1):
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

def get_max_window_size(list_of_equations, window_size=(800, 600)):
    if list_of_equations:
        x_min = None
        y_min = None
        x_max = None
        y_max = None
        for equation in list_of_equations:
            if x_min is None:
                x_min = equation.x
                x_max = equation.right
                y_min = equation.y
                y_max = equation.top
            if equation.x < x_min:
                x_min = equation.x
            if equation.right > x_max:
                x_max = equation.right
            if equation.y < y_min:
                y_min = equation.y
            if equation.top > y_max:
                y_max = equation.top

        dx = x_max - x_min
        dy = y_max - y_min
        dxf = dx/(window_size[0])
        dyf = dy/(window_size[1])
        if dxf > dyf:
            adjusted_dy = ((y_max - y_min)/dxf)
            y_change = ((window_size[1])-adjusted_dy)
            return [dxf, x_min, y_min, y_change]
        else:
            y_change = (((window_size[1])*dyf)-dy)
            return [dyf, x_min, y_min, y_change]

def set_window_on_load(list_of_equations, zoom_factor, center_point):
    for equation in list_of_equations:
        equation.equationlabel.font_size /= zoom_factor[0]
        equation.x -= zoom_factor[1]
        equation.x /= zoom_factor[0]
        equation.y -= zoom_factor[2]
        equation.y /= zoom_factor[0]

        equation.y += zoom_factor[3] + 25
