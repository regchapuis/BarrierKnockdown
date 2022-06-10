from pyfirmata import Arduino, util
from pyfirmata import INPUT, OUTPUT, PWM
import time
import random
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

from tkinter.filedialog import askopenfilename, asksaveasfilename
import hw_io
import csv
import datetime
import trials

manual = False



def start_trials():
    global running_trials, numtrials_value
    num = numtrials_value.get()
    if(num.isnumeric()):
        print("Running trials: ", num)
        btn_start["state"] = "disabled"
        btn_pause["state"]="active"
        btn_end["state"] = "active"
        btn_rst["state"] = "active"
        running_trials = True


        entry_name["state"] = "disabled"
        entry_subj_num["state"] = "disabled"
        entry_group["state"] = "disabled"
        entry_numtrials["state"] = "disabled"
        entry_testtype["state"] = "disabled"
    else:
        print("Non numeric trial entry: ", num)

def pause_trials():
    global running_trials
    if pause_value.get().__eq__("Pause"):
        btn_start["state"]="disabled"
        btn_pause["state"]="active"
        btn_end["state"]="active"
        pause_value.set("Resume")
        running_trials = False
    else:
        btn_start["state"]="disabled"
        btn_pause["state"]="active"
        btn_end["state"]="active"
        pause_value.set("Pause")
        running_trials = True

def end_trials():
    global running_trials, trial_num
    btn_start["state"] = "active"
    btn_pause["state"]="disabled"
    btn_end["state"] = "disabled"
    running_trials = False
    trial_num = 0

def test_trial():
    global trial_num, reaction_t, movement_t, running_trials, iid_count, name_value, data_table
    if(running_trials):
        reaction_t = random.random()
        movement_t = random.random()
        trial_num = trial_num + 1
        data_table.insert(parent='',index='end',iid=iid_count,text='',
                          values=(name_value.get(), subj_num_value.get(), testtype_value.get(), group_value.get(), trial_num, 'Red', 'yes', reaction_t, movement_t))
        iid_count += 1

def parse_input(num):
    global simulation_ovals, simulation_canvas
    #print(num)
    simulation_canvas.itemconfig(simulation_ovals[num-1], fill='blue')

def fill_purple(num):
    global simulation_ovals, simulation_canvas
    #print(num)
    simulation_canvas.itemconfig(simulation_ovals[num], fill='purple')

def fill_red(num):
    global simulation_ovals, simulation_canvas
    #print(num)
    simulation_canvas.itemconfig(simulation_ovals[num], fill='red')

#CSV code from : https://stackoverflow.com/questions/62580527/saving-datas-from-treeview-to-csv-file-tkinter-python
def save_csv():
    global data_table
    # print("csv!")
    str = "data"+ datetime.datetime.now().strftime("%d-%m-%Y-%H-%M-%S") + ".csv"
    with open(str, "w", newline='') as myfile:
        csvwriter = csv.writer(myfile, delimiter=',')

        for row_id in data_table.get_children():
            row = data_table.item(row_id)['values']
            # print('save row:', row)
            csvwriter.writerow(row)

def clear_csv():
    global data_table, running_trials
    res = messagebox.askokcancel('Clear and Reset',
                           'If you click \'ok\' this will clear all of the data and reset the trials to 0.')

    if res:
        for item in data_table.get_children():
            data_table.delete(item)
        trials.reset_trials()
        btn_start["state"] = "active"

        entry_name["state"] = "normal"
        entry_subj_num["state"] = "normal"
        entry_group["state"] = "normal"
        entry_numtrials["state"] = "normal"
        entry_testtype["state"] = "normal"

        btn_rst["state"] = "disabled"
        running_trials = True

        red_count.set(0)
        green_count.set(0)
        blue_count.set(0)

def toggle_manual():
    global manual
    # print("Toggle manual")

    if toggle_value.get() == "Manual Pattern Checking":
        res = messagebox.askokcancel('Switch Pattern Checking Mode',
                                     "This will not use sensors, and will prompt the tester after each trial")
        if res:
            toggle_value.set("Automatic Pattern Checking")
            manual = True
    else:
        res = messagebox.askokcancel('Switch Pattern Checking Mode',
                                     "This will enable the barrier sensors to check for pattern correctness")
        if res:
            toggle_value.set("Manual Pattern Checking")
            manual = False

def manual_trial_prompt():
    global iid_count
    res = messagebox.askyesno("Trial", "Did the subject get the pattern correct?")
    if res:
        data_table.insert(parent='', index='end', iid=iid_count, text='',
                          values=(name_value.get(), subj_num_value.get(), testtype_value.get(), group_value.get(), trials.trials, trials.get_color(), 'yes', trials.get_reaction_time(),
                                  trials.get_movement_time()))
    else:
        data_table.insert(parent='', index='end', iid=iid_count, text='',
                          values=(name_value.get(), subj_num_value.get(), testtype_value.get(), group_value.get(), trials.trials, trials.get_color(), 'no', trials.get_reaction_time(),
                                  trials.get_movement_time()))
    iid_count+=1

def ready_prompt():
    res = messagebox.showinfo("Ready", "When Barriers are reset and you are ready, click to continue")

def async_trial_red():
    trials.async_trial = 1
    trials.STATE = trials.QUEUE
    trials.color = trials.RED
    # trials.running = True

def async_trial_blue():
    trials.async_trial = 1
    trials.STATE = trials.QUEUE
    trials.color= trials.BLUE
    # trials.running = True

def async_trial_green():
    trials.async_trial = 1
    trials.STATE = trials.QUEUE
    trials.color = trials.GREEN
    # trials.running = True

window = tk.Tk()
window.title("Barrier Knockdown Lab")
window.geometry('1200x500')
window.rowconfigure(0, weight=1)
window.columnconfigure(0, minsize=50)
window.columnconfigure(2, minsize=25, weight=1)
window.columnconfigure(3, minsize=125, weight=1)
window.columnconfigure(4, minsize=25, weight=1)
window.columnconfigure(5, minsize=1000)

window.rowconfigure(1, minsize=50)

#Frames and Segments
#txt_edit = tk.Text(window)
sidebar1 = tk.Frame(window)
sidebar2 = tk.Frame(window)
sidebar3 = tk.Frame(window)
sidebar4 = tk.Frame(window)
simulation_frame = tk.Frame(window)
data_frame = tk.Frame(window)

#Labels
label_name = tk.Label(sidebar1, text = "Subject Name:", anchor = "w")
label_subject_num = tk.Label(sidebar1, text = "Subject Number:", anchor = "w")
label_group = tk.Label(sidebar1, text = "Interference Pattern:", anchor = "w")
label_numtrials =  tk.Label(sidebar1, text = "Number of Trials:", anchor = "w")
label_testtype = tk.Label(sidebar1, text = "Test Type:", anchor = "w")

label_name.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
label_subject_num.grid(row=1, column=0, sticky="ew", padx=5, pady=5)
label_group.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
label_numtrials.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
label_testtype.grid(row=4, column=0, sticky="ew", padx=5, pady=5)




#Entries
name_value = tk.StringVar(window)
name_value.set("Subject 1")
entry_name = tk.Entry(sidebar2, width=20, textvariable = name_value)

subj_num_value = tk.StringVar(window)
subj_num_value.set("1")
entry_subj_num = tk.Entry(sidebar2, width=20, textvariable = subj_num_value)

group_options = ["Random", "Moderate", "Transitional", "Blocked", "Serial"]
group_value = tk.StringVar(window)
group_value.set("Random")
entry_group = ttk.Combobox(sidebar2, textvariable = group_value)
entry_group['values'] = group_options
entry_group['state'] = 'readonly'

testtype_options = ["Acquisition", "Transfer", "Retention"]
testtype_value = tk.StringVar(window)
testtype_value.set("Acquisition")
entry_testtype = ttk.Combobox(sidebar2, textvariable = testtype_value)
entry_testtype['values'] = testtype_options
entry_testtype['state'] = 'readonly'


numtrials_options = [5, 10, 15, 20, 25, 30]
numtrials_value = tk.StringVar(window)
numtrials_value.set(5)
entry_numtrials = ttk.Entry(sidebar2, textvariable = numtrials_value)
#entry_numtrials['values']= numtrials_options
#entry_numtrials['state'] = 'readonly'


entry_name.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
entry_subj_num.grid(row=1, column=1, sticky="ew", padx=5, pady=5)
entry_group.grid(row=2, column=1, sticky="ew", padx=5, pady=5)
entry_numtrials.grid(row=3, column=1, sticky="ew", padx=5, pady=5)
entry_testtype.grid(row=4, column=1, sticky="ew", padx=5, pady=5)



#Buttons
btn_start = tk.Button(sidebar1, text="Start", command=start_trials)

pause_value = tk.StringVar(window)
pause_value.set("Pause")
btn_pause = tk.Button(sidebar1, textvariable=pause_value, command=pause_trials)
btn_pause["state"]="disabled"

btn_end = tk.Button(sidebar1, text="End", command=end_trials)
btn_end["state"]="disabled"
btn_test = tk.Button(sidebar1, text="TEST", command=test_trial)

toggle_value = tk.StringVar(window)
toggle_value.set("Manual Pattern Checking")
btn_toggle = tk.Button(sidebar1, textvariable=toggle_value, command=toggle_manual)



btn_start.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
#btn_pause.grid(row=4, column=0, sticky="ew", padx=5, pady=5)
#btn_end.grid(row=5, column=0, sticky="ew", padx=5, pady=5)
# btn_test.grid(row=7, column=0, sticky="ew", padx=5, pady=5)
btn_toggle.grid(row=8, column=0, sticky="ew", padx=5, pady=5)


#Table Set up
table_cols = ('subject', 'subjnum', 'testtype', 'interference', 'trial', 'pattern', 'correct', 'reaction_time', 'movement_time')
data_table = ttk.Treeview(data_frame, columns=table_cols, show='headings')
data_table.heading('subject', text='Subject')

data_table.heading('subjnum', text='Subject #')
data_table.heading('testtype', text='Test Type')
data_table.heading('interference', text='Pattern')

data_table.heading('trial', text='Trial #')
data_table.heading('correct', text='Correct')
data_table.heading('pattern', text='Color')
data_table.heading('reaction_time', text='Reaction Time')
data_table.heading('movement_time', text='Movement Time')

data_table.column('#1', width =75)
data_table.column('#2', width =75)
data_table.column('#3', width =75)
data_table.column('#4', width =75)
data_table.column('#5', width =50)
data_table.column('#6', width =50)
data_table.column('#7', width =50)
data_table.column('#8', width =100)
data_table.column('#9', width =100)

#csv section
btn_save = tk.Button(sidebar3, text="Save Data", command=save_csv)
btn_save.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

btn_clear = tk.Button(sidebar3, text="Clear Data", command=clear_csv)
btn_clear.grid(row=1, column=0, sticky="ew", padx=5, pady=5)

btn_rst = tk.Button(sidebar1, text="Reset", command=clear_csv)
btn_rst["state"]="disabled"
btn_rst.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

label_redcount = tk.Label(sidebar3, text = "Red Trial Count:")
label_redcount.grid(row=2, column=0, sticky="ew", padx=5, pady=5)
label_bluecount = tk.Label(sidebar3, text = "Blue Trial Count:")
label_bluecount.grid(row=3, column=0, sticky="ew", padx=5, pady=5)
label_greencount = tk.Label(sidebar3, text = "Green Trial Count:")
label_greencount.grid(row=4, column=0, sticky="ew", padx=5, pady=5)

red_count = tk.IntVar(window)
red_count.set(0)
blue_count = tk.IntVar(window)
blue_count.set(0)
green_count = tk.IntVar(window)
green_count.set(0)

label_red = tk.Label(sidebar3, textvariable=red_count)
label_red.grid(row=2, column=1, sticky="ew", padx=0, pady=5)
label_blue = tk.Label(sidebar3, textvariable=blue_count)
label_blue.grid(row=3, column=1, sticky="ew", padx=0, pady=5)
label_green = tk.Label(sidebar3, textvariable=green_count)
label_green.grid(row=4, column=1, sticky="ew", padx=0, pady=5)

btn_add_red = tk.Button(sidebar3, text="Run 1 Red Trial", command=async_trial_red)
btn_add_red.grid(row=5, column=0, sticky="ew", padx=5, pady=5)

btn_add_blue = tk.Button(sidebar3, text="Run 1 Blue Trial", command=async_trial_blue)
btn_add_blue.grid(row=6, column=0, sticky="ew", padx=5, pady=5)

btn_add_green = tk.Button(sidebar3, text="Run 1 Green Trial", command=async_trial_green)
btn_add_green.grid(row=7, column=0, sticky="ew", padx=5, pady=5)




scrollbar = ttk.Scrollbar(data_frame, orient=tk.VERTICAL, command=data_table.yview)
data_table.configure(yscroll=scrollbar.set)
scrollbar.grid(row=0, column=2, sticky='nse')


#Setup Dot simulation
canvas_width = 150
canvas_height = 200
simulation_canvas= tk.Canvas(simulation_frame,bg="yellow",width=canvas_width, height=canvas_height)
#simulation_canvas.create_oval(10, 10, 40, 40, fill="red")
simulation_ovals = []
for x in range(3):
    for y in range(2):
        y1 = canvas_width*(x/3) + 20
        x1 = canvas_width*(y/2) + 20
        x2 = x1+30
        y2 = y1+30
        simulation_ovals.append(simulation_canvas.create_oval(x1, y1, x2, y2, fill="red"))

#simulation_canvas.pack()
simulation_canvas.grid(row=0, column = 0, sticky='nsew')

#Setup Frames
sidebar1.grid(row=0, column=0, sticky="nsw")
sidebar2.grid(row=0, column=1, sticky="nsw")
sidebar3.grid(row=0, column=3, sticky="nsew")
# sidebar4.grid(row=0, column=4, sticky="nsew")

data_table.grid(row=0, column=1, sticky="nsew")
simulation_frame.grid(row=1, column=0, sticky="nsew")
data_frame.grid(row=0, column=5, sticky="nsew")

#Functionality variables
running_trials = False
reaction_t = 0
movement_t = 0
trial_num = 0
iid_count = 0


