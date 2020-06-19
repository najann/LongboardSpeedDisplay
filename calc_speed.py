def calculate_speed(old, new):
    if new >= old:
        return new - old
    else:
        return new + (5 - old)
