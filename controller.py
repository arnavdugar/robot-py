import code
import position

robot, window = None, None


def draw_robot():
    window.clear_all()
    for leg in robot.legs:
        for segment in leg.segments:
            #window.draw_line(segment.name + ' center', segment.global_start_position, segment.global_start_position +
                             #segment.global_direction_center.scaled(segment.length), fill='#ccc')
            window.draw_line(segment.name + ' axis', segment.global_start_position, segment.global_start_position +
                             segment.global_axis.scaled(15.0), fill='#900')
            window.draw_line(segment.name, segment.global_start_position, segment.global_end_position)
    window.draw_polygon('robot', *[robot.legs[i].global_start_position for i in (0, 1, 3, 2)])
    window.draw_line('x-axis', position.Position(0, 0, 0), position.Position(200, 0, 0), dash=(2, 4), fill='red')
    window.draw_line('y-axis', position.Position(0, 0, 0), position.Position(0, 200, 0), dash=(2, 4), fill='green')
    window.draw_line('z-axis', position.Position(0, 0, 0), position.Position(0, 0, 200), dash=(2, 4), fill='blue')


def set_rotation(l, s, rotation):
    segment = robot.legs[l].segments[s]
    segment.rotation = rotation
    draw_robot()
    #window.update_item(segment.name, segment.global_start_position, segment.global_end_position)


def values():
    return [[segment.value for segment in leg.segments] for leg in robot.legs]