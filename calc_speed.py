_SLICES_NUM = 5


def calculate_speed(old, new):
    if new >= old:
        return new - old
    else:
        return new + (_SLICES_NUM - old)
