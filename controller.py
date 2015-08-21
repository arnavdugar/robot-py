import position

robot, window = None, None


def init():
    c = window.canvas[2]
    c.bind("<Button-1>", callback1)
    c = window.canvas[1]
    c.bind("<Button-1>", callback2)


def callback1(event):
    x, y = event.x - 200, 200 - event.y
    for leg in robot.legs:
        old_x, old_y, old_z = leg.global_end_position
        leg.move_to(position.Position(x, y, old_z))
    draw_robot()

def callback2(event):
    r, z = abs(event.x - 200), 200 - event.y
    for i in range(len(robot.legs)):
        l = robot.legs[i]
        start = l.segments[0].global_end_position
        position = l.global_end_position.copy
        position.z = 0
        position.normalize()
        position *= r
        position.z = z
        a, p = l.compute_remaining(position, start)
        set_angle(i, 1, a)
    draw_robot()


def draw_robot():
    window.clear_all()
    for leg in robot.legs:
        draw_leg(leg)
    window.draw_polygon('robot', *[leg.global_start_position for leg in robot.legs])
    window.draw_coordinates()


def draw_leg(leg):
    for segment in leg.segments:
        segment_name = segment.name.replace(' ', '_')
        window.draw_line(segment_name + ' center', segment.global_start_position, segment.global_start_position +
                         segment.global_direction_center * segment.length, fill='#ccc')
        window.draw_line(segment_name + ' axis', segment.global_start_position, segment.global_start_position +
                         segment.global_axis * 15, fill='#900')
        window.draw_line(segment_name, segment.global_start_position, segment.global_end_position)


def set_rotation(l, s, rotation):
    segment = robot.legs[l].segments[s]
    segment.rotation = rotation
    segment_name = segment.name.replace(' ', '_')
    window.update_item(segment_name, segment.global_start_position, segment.global_end_position)


def set_angle(l, s, angle):
    segment = robot.legs[l].segments[s]
    segment.angle = angle
    segment_name = segment.name.replace(' ', '_')
    window.update_item(segment_name, segment.global_start_position, segment.global_end_position)


def values():
    return [[segment.value for segment in leg.segments] for leg in robot.legs]


def reset():
    for leg in robot.legs:
        for segment in leg.segments:
            segment.rotation = segment.default_rotation
    draw_robot()


def commit():
    values, indexes = [], []
    for leg in robot.legs:
        values.extend(segment.value for segment in leg.segments)
        indexes.extend(segment.write_index for segment in leg.segments)
    data = [0 for _ in range(len(values))]
    for i in range(len(values)):
        data[indexes[i]] = values[i]
    data = arduino_board.build_data(b'\xff', data)
    arduino_board.write(data)


def move_leg(l, x, y, z):
    leg = robot.legs[l]
    new_position = leg.global_end_position + position.Position(x, y, z)
    leg.move_to(new_position)
    draw_robot()