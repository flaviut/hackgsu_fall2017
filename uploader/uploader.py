import select
import sys

import serial

from http_client import HttpClientThread
from throttle import throttle

JERK_THRESHOLD = .5  # this seems to work well

previous_accl = None
previous_jerk = None

current_lock_state = None

current_toilet = 1

client = HttpClientThread()
client.start()


def update_server(event_type):
    client.put_event(event_type, current_toilet)


@throttle(seconds=2)
def handle_door_closed():
    print('CLOSED')
    update_server('closed')


def handle_lock(pot):
    global current_lock_state
    scaled_pot = pot / 0x3FF
    if scaled_pot > .83 and (current_lock_state == 'locked' or current_lock_state is None):
        current_lock_state = 'unlocked'
        print('UNLOCKED')
        update_server('unlocked')
    if scaled_pot < .45 and (current_lock_state == 'unlocked' or current_lock_state is None):
        current_lock_state = 'locked'
        print('LOCKED')
        update_server('locked')


def handle_accelerometer(x, y, z):
    global previous_accl, previous_jerk
    scaled_x, scaled_y, scaled_z = (x / 0x7FFF, y / 0x7FFF, z / 0x7FFF)
    abs_x, abs_y, abs_z = (abs(scaled_x), abs(scaled_y), abs(scaled_z))

    if previous_accl is None:
        previous_accl = abs_x, abs_y, abs_z
    else:
        previous_jerk = (abs(previous_accl[0] - abs_x),
                         abs(previous_accl[1] - abs_y),
                         abs(previous_accl[2] - abs_z))
        previous_accl = abs_x, abs_y, abs_z

    if (previous_jerk is not None and
            any([jerk > JERK_THRESHOLD for jerk in previous_jerk])):
        # door closed
        handle_door_closed()


def handle_change_toilet():
    global current_toilet
    if sys.stdin in select.select([sys.stdin], [], [], 0):
        current_toilet = int(sys.stdin.read(1))
        print('Changed toilet to ' + str(current_toilet))


def main():
    with serial.Serial('/dev/ttyACM0', 115200, timeout=0.1) as ser:
        while True:
            parsed_tup = map(int, ser.readline().decode('ascii').split(' '))
            pot, x, y, z = parsed_tup
            handle_accelerometer(x, y, z)
            handle_lock(pot)
            handle_change_toilet()


if __name__ == '__main__':
    main()
