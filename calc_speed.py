def calculate_speed(old, new):
    if new >= old:
        diff = new - old
    else new < old:
        diff = new + (5 - old)
    speed = 4 * diff * 0.00001 * 360000
    # ["blue", "white", "red", "green", "yellow"]

def get_rows(speed):
    if speed <= 32:
        return speed // 4
    else:
        return 8
    