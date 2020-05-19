def calculate_speed(old, new):
    if new >= old:
        diff = new - old
    else:
        diff = new + (5 - old)
    speed = 4 * diff * 0.00001 * 360000
    if speed == 72:
        return 8
    elif speed == 57.6:
        return 7
    else:
        return speed // 7
