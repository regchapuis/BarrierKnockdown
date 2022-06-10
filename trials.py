import random
import time
import ui
import hw_io

QUEUE = 0
START = 1
FINISH = 2
PAUSED = 3
TRIAL = 4
GO = 5
HOLD = 6
READY = 7


BLUE = 0
RED = 1
GREEN = 2

BLUE_PATTERN =[5, 2, 1]
RED_PATTERN =[5, 2, 3]
GREEN_PATTERN = [2, 3, 0]


running = False
paused = False
holding = False
trials = 1
color = BLUE
state = PAUSED

colors = [BLUE, RED, GREEN]
last_color1 = RED
last_color2 = GREEN

color_counts = [0, 0, 0]
count_five = 0
async_trial = 0


reaction_time = 0
movement_tme = 0
current_pattern = []
pattern_check = "yes"

def print_state():
    if state == PAUSED:
        print("State: Paused")
    elif state == QUEUE:
        print("State: Queue")
    elif state == START:
        print("State: Start")
    elif state == FINISH:
        print("State: Finish")
    elif state == TRIAL:
        print("State: Trial")
    elif state == GO:
        print("State: Go")
    elif state == HOLD:
        print("State: Hold")
    elif state == READY:
        print("State: Ready")
    else:
        print("Unknown State")

def change_state(new):
    global state
    state = new
    print_state()

def get_reaction_time():
    global reaction_time
    return reaction_time

def get_movement_time():
    global movement_time
    return movement_time



def trial_FSM(board):
    global state, reaction_time, movement_time, trials, color, async_trial, pattern_check, current_pattern
    #print_state()

    if(state == PAUSED): #Any time a trial is not currently happening
        return
    elif (state == QUEUE): #When the queue light is on and then waits a random time interval
        hw_io.turnOffLEDS(board)
        color = next_color()
        lightQueueLED(board)
        change_state(READY)
        return
    elif (state == READY):
        if async_trial:
            lightQueueLED(board)

        return
    elif(state == HOLD):
        # print("sleep")
        time.sleep((random.random()*2)+1) #pauses for 1-3 seconds randomly
        # print("sleep over")
        lightStartLED(board)
        reaction_time = time.time()
        change_state(START)
        return
    elif (state == START): #When the start light turns on, starts the reaction timer
        return
    elif (state == GO): #when the user releases the start button, ends reaction timer, starts movement timer

        current_time = time.time()

        reaction_time = current_time - reaction_time
        movement_time = current_time
        # print("start movement timer", current_time, movement_tme)
        change_state(TRIAL)
        return
    elif (state == TRIAL): #in the middle of the barrier knockdown
        return
    elif (state == FINISH): #when the user pushes the end button on the trial
        hw_io.turnOffLEDS(board)

        movement_time = time.time() - movement_time
        # print("end movement timer", movement_time)

        if(ui.manual):
            ui.manual_trial_prompt()
        else:
            print(current_pattern)
            if(current_pattern == GREEN_PATTERN):
                print("CORRECT PATTERN: GREEN")
                pattern_check = "yes"
            elif(current_pattern == BLUE_PATTERN):
                print("CORRECT PATTERN: BLUE")
                pattern_check = "yes"
            elif(current_pattern == RED_PATTERN):
                print("CORRECT PATTERN: RED")
                pattern_check = "yes"
            else:
                print("INCORRECT PATTERN")
                pattern_check = "no"


            ui.data_table.insert(parent='', index='end', iid=ui.iid_count, text='',
                              values=(ui.name_value.get(), ui.subj_num_value.get(), ui.testtype_value.get(), ui.group_value.get(), trials, get_color(), pattern_check, reaction_time,
                                      movement_time))
            ui.iid_count += 1
        increment_count()

        if async_trial:
            async_trial =0
            # print("finished async trial")

        if(trials >= int(ui.numtrials_value.get())):
            change_state(PAUSED)
            print("Finished with all trials")
        else:
            ui.ready_prompt()
            trials=trials+1
            print("Running Trial", trials)
            change_state(QUEUE)
        current_pattern = []

        return


def next_color():
    global color, colors, last_color1, last_color2, color_counts, count_five, async_trial

    if async_trial:
        # print("Async trial")
        return color

    g = ui.group_value.get()
    # print("New color for group:", g)

    current = color
    last_color2 = last_color1
    last_color1 = current

    if g == "Random":
        color = random.choice(colors)

        # only 2 in a row can be the same
        if (last_color1 == last_color2):
            while (color == last_color1):
                color = random.choice(colors)

    elif g == "Moderate": #Groups of five
        # print("Mod")
        count_five += 1
        if (count_five % 5 == 0):
            color = (color + 1) % len(colors)
        else:
            color = current

    elif g == "Transitional": #transition from blocks to random
        # print("Trans")

        if (trials <= (trials/3)): #first third of trials in blocks of 5
            count_five += 1
            if (count_five % 5 == 0):
                color = (color + 1) % len(colors)
            else:
                color = current
        elif (trials <= 2*(trials/3)): #second third of trials in blocks of 3
            count_five += 1
            if (count_five % 3 == 0):
                color = (color + 1) % len(colors)
            else:
                color = current
        else: #third third of trials are random
            color = random.choice(colors)

            # only 2 in a row can be the same
            if (last_color1 == last_color2):
                while (color == last_color1):
                    color = random.choice(colors)



    elif g == "Blocked": #equally spaced blocks
        div = int(int(ui.numtrials_value.get())/len(colors))
        for x in range (len(colors)):
            # print(trials, div, x)
            if trials <= (x+1)*div:
                color = x-1
                break

    elif g == "Serial": #colors in order!
        color = (color+1)%len(colors)
    else:
        print("Invalid Group Type")

    # print("Next color:", get_color())
    color_counts[color]= color_counts[color]+1
    return color

def get_color():
    global color

    if(color == RED):
        return "Red"
    elif(color == BLUE):
        return "Blue"
    else:
        return"Green"

def lightQueueLED(board):
    global color
    hw_io.turnOffLEDS(board)
    if(color == BLUE):
        hw_io.write_to_led(board, hw_io.Q_BLUE_LED, 1)
    elif(color == RED):
        hw_io.write_to_led(board, hw_io.Q_RED_LED, 1)
    else:
        hw_io.write_to_led(board, hw_io.Q_GREEN_LED, 1)


def lightStartLED(board):
    global color
    hw_io.turnOffLEDS(board)
    if(color == BLUE):
        hw_io.write_to_led(board, hw_io.Q_BLUE_LED, 0)
        hw_io.write_to_led(board, hw_io.START_BLUE_LED, 1)
    elif(color == RED):
        hw_io.write_to_led(board, hw_io.Q_RED_LED, 0)
        hw_io.write_to_led(board, hw_io.START_RED_LED, 1)
    else:
        hw_io.write_to_led(board, hw_io.Q_GREEN_LED, 0)
        hw_io.write_to_led(board, hw_io.START_GREEN_LED, 1)


def reset_trials():
    global trials, color, state, last_color1, last_color2, reaction_time, movement_tme, current_pattern

    trials = 1
    color = BLUE
    state = QUEUE

    last_color1 = RED
    last_color2 = GREEN

    reaction_time = 0
    movement_tme = 0
    current_pattern = []

def increment_count():
    global color
    if color == RED:
        ui.red_count.set(ui.red_count.get()+1)
    elif color == GREEN:
        ui.green_count.set(ui.green_count.get()+1)
    else:
        ui.blue_count.set(ui.blue_count.get()+1)




