from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM

Q_BLUE_LED = 10
Q_RED_LED = 9
Q_GREEN_LED = 8
START_BLUE_LED = 6
START_RED_LED = 7
START_GREEN_LED = 11

PHOTORES_0 = 1
PHOTORES_1 = 0
PHOTORES_2 = 3
PHOTORES_3 = 2
PHOTORES_4 = 5
PHOTORES_5 = 4


import time

def setup_board(board):

    #board = Arduino('COM5')
    #print("Communication Successfully started")

    it = util.Iterator(board)
    it.start()

    board.digital[2].mode = INPUT
    board.digital[3].mode = INPUT

    #LEDS
    board.digital[4].mode = OUTPUT
    board.digital[5].mode = OUTPUT
    board.digital[6].mode = OUTPUT
    board.digital[7].mode = OUTPUT
    board.digital[9].mode = OUTPUT
    board.digital[10].mode = OUTPUT
    board.digital[11].mode = OUTPUT

    turnOffLEDS(board)

    board.analog[0].mode = INPUT
    board.analog[1].mode = INPUT
    board.analog[2].mode = INPUT
    board.analog[3].mode = INPUT
    board.analog[4].mode = INPUT
    board.analog[5].mode = INPUT



def check_start(board):
    # print(board.digital[2].read())
    return(board.digital[2].read())

def check_stop(board):
    # print(board.digital[3].read())
    return(board.digital[3].read())

def write_to_led(board, led, state):
    board.digital[led].write(state)



def turnOffLEDS(board):
    write_to_led(board, Q_BLUE_LED, 0)
    write_to_led(board, Q_RED_LED, 0)
    write_to_led(board, Q_GREEN_LED, 0)
    write_to_led(board, START_BLUE_LED, 0)
    write_to_led(board, START_RED_LED, 0)
    write_to_led(board, START_GREEN_LED, 0)

def turnOnLEDS(board):
    write_to_led(board, Q_BLUE_LED, 1)
    write_to_led(board, Q_RED_LED, 1)
    write_to_led(board, Q_GREEN_LED, 1)
    write_to_led(board, START_BLUE_LED, 1)
    write_to_led(board, START_RED_LED, 1)
    write_to_led(board, START_GREEN_LED, 1)


def check_photores(board):
    # print(board.analog[1].read())
    return(board.analog[0].read())


def check_buttons(board):
    # print(board.analog[0].read())

    b1 = board.digital[7].read()
    b2 = board.digital[4].read()
    b3 = board.digital[6].read()
    b4 = board.digital[3].read()
    b5 = board.digital[5].read()
    b6 = board.digital[2].read()

    if(b1):
        return 1
    if(b2):
        return 2
    if(b3):
        return 3
    if(b4):
        return 4
    if(b5):
        return 5
    if(b6):
        return 6

    return 0


# board = Arduino('COM5')
# print("Communication Successfully started")
# setup_board(board)

# while True:
#     print(check_buttons(board))