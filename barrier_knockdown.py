from pyfirmata import Arduino
import time
import hw_io
import ui
import trials


if __name__ == '__main__':

    # while True:
    #     ui.window.update()


    # setup buttons
    board = Arduino('COM5')
    print("Communication Successfully started")
    hw_io.setup_board(board)
    hw_io.turnOffLEDS(board)
    # buttons.turnOnLEDS(board)
    # buttons.turnOffLEDS(board)
    # buttons.write_to_led(board, 6, 1)
    #
    # while True:
    #     ui.window.update()

    holding_start = False

    while True:

        trials.trial_FSM(board)
        start_trial = hw_io.check_start(board)
        end_trial = hw_io.check_stop(board)

        # if(trials.state == trials.HOLD):
        #     print(start_trial)


        if start_trial:
            if(holding_start != True):
                holding_start = True
                if(trials.state == trials.READY):
                    trials.change_state(trials.HOLD)

        else:
            holding_start = False
            if(trials.state == trials.START):
                #trials.current_pattern.clear()
                # print(start_trial)
                trials.change_state(trials.GO)
            elif (trials.state == trials.HOLD):
                trials.change_state(trials.QUEUE)

        if ui.running_trials and trials.running == False:
            trials.running = True
            trials.change_state(trials.QUEUE)
        if trials.running:
            if end_trial == True and trials.state == trials.TRIAL:
                trials.change_state(trials.FINISH)



        photores_value = 0

        for x in range(6):
            try:
                if (x % 2 == 0):
                    photores_value = x + 1
                else:
                    photores_value = x - 1
                if(board.analog[x].read() < 0.3):

                    # print(photores_value)
                    ui.fill_purple(photores_value)

                    if trials.running and photores_value not in trials.current_pattern:
                        trials.current_pattern.append(photores_value)
                        print(trials.current_pattern)
                else:
                    ui.fill_red(photores_value)
            except:
                pass

        ui.window.update()



