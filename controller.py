import code
import position

robot, window = None, None


def init():
    c = window.canvas[2]
    c.bind("<Button-1>", callback1)
    c = window.canvas[1]
    c.bind("<Button-1>", callback2)


def callback1(event):
    x, y = event.x - 200, 200 - event.y
    for i in range(len(robot.legs)):
        l = robot.legs[i]
        a, p = l.compute_base(position.Position(x, y, 0), l.segments[0])
        set_angle(i, 0, a)

def callback2(event):
    x, y = event.x - 200, 200 - event.y
    print(x, y)
    pass


def draw_robot():
    window.clear_all()
    for leg in robot.legs:
        draw_leg(leg)
    window.draw_polygon('robot', *[leg.global_start_position for leg in robot.legs])
    window.draw_coordinates()


def draw_leg(leg):
    for segment in leg.segments:
        #window.draw_line(segment.name + ' center', segment.global_start_position, segment.global_start_position +
                         #segment.global_direction_center.scaled(segment.length), fill='#ccc')
        window.draw_line(segment.name + ' axis', segment.global_start_position, segment.global_start_position +
                         segment.global_axis.scaled(15.0), fill='#900')
        window.draw_line(segment.name, segment.global_start_position, segment.global_end_position)


def set_rotation(l, s, rotation):
    segment = robot.legs[l].segments[s]
    segment.rotation = rotation
    draw_robot()
    #window.update_item(segment.name, segment.global_start_position, segment.global_end_position)


def set_angle(l, s, angle):
    segment = robot.legs[l].segments[s]
    segment.angle = angle
    draw_robot()
    #window.update_item(segment.name, segment.global_start_position, segment.global_end_position)


def values():
    return [[segment.value for segment in leg.segments] for leg in robot.legs]