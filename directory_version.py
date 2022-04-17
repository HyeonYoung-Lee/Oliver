import os
import tkinter
import traceback
import numpy as np
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def readDirectory():
    global interval
    resultF = open(path + '/result.txt', 'w')
    try:
        for filename in os.listdir(path):
            tmp = filename.split('ms')
            interval = tmp[len(tmp)-2]
            with open(os.path.join(path, filename), 'r') as f:
                analyzeData(path, filename, interval, pw, resultF)
        resultF.close()

        exitProg = messagebox.askquestion(
            "Complete", "Complete successfully\n Do you want to quit?")
        if exitProg == 'yes':
            window.destroy()

    except:
        resultF.close()
        messagebox.showwarning("warning", "please select directory")


def analyzeData(path, filename, interval, pw, resultF):
    if filename == 'result.txt':
        return

    full_path = path + '/' + filename
    # make copy data
    rawData = np.genfromtxt(full_path)
    copyData = rawData.copy()
    add = np.zeros((len(copyData), 1), dtype='float')
    copyData = np.append(copyData, add, axis=1)

    # calculate rate of change
    for i in range(len(copyData)-1):
        h = 0.000100001
        f_0 = copyData[i][1]
        f_1 = copyData[i+1][1]
        copyData[i][2] = (f_1 - f_0)/h

    # find five values in small order
    min_array = copyData.copy()
    min_array = min_array[min_array[:, 2].argsort()]
    min_array = min_array[:5]

    # choose the latest value of min array
    # its rate of change value must be smaller than -0.2
    time_temp = 0.0000000
    min_rate_of_change = 0.0
    for i in range(len(min_array)):
        if min_array[i][2] < -0.2 and min_array[i][0] > time_temp:
            time_temp = min_array[i][0]
            min_rate_of_change = min_array[i][2]

    # find index of the latest pulse in copy data
    min_array_idx = np.where((copyData[:, 2] == min_rate_of_change))
    x_second_idx = min_array_idx[0][0]
    x_second = float(x_second_idx)*(1/1000) + \
        float(x_second_idx)*(1/1000000000)
    x_second_value = copyData[x_second_idx][1]

    # calculate interval and pulse width
    cal_interval = float(interval) * (1/1000) + \
        float(interval) * (1/1000000000)
    pw = float(pw) * (1/1000) + float(pw) * (1/1000000000)

    # find time and index of first pulse
    subtract = cal_interval + pw
    x_first = x_second - subtract
    x_fisrt_idx = np.where((copyData[:, 0]) == round(x_first, 10))
    try:
        x_fisrt_idx = x_fisrt_idx[0][0]
        x_first_value = copyData[x_fisrt_idx][1]
        ## first_rate_of_change = copyData[x_fisrt_idx][2]
        get_ratio = x_second_value / x_first_value
        resultF.write(str(interval) + ' ' + str(x_first_value) +
                      ' ' + str(x_second_value) + ' ' + str(get_ratio) + '\n')

    except:
        resultF.write(filename + ' : !!!!! Analyze failed !!!!!\n')


# GUI
window = Tk()
window.title("이동준 돼지")
window.geometry("400x200")


def askDir():
    global path
    window.dir = filedialog.askdirectory()
    dir_name.configure(text=window.dir)
    path = window.dir


btn_selectDir = Button(window, text="Select Directory", command=askDir)
btn_selectDir.place(x=30, y=10)

dir_name = Label(window, text=" ")
dir_name.place(x=30, y=50)


def savePw():
    global pw
    tmp_pw = ent_pw.get()
    if(tmp_pw == ''):
        messagebox.showwarning("warning", "please enter pulse width")
        btn_ok['state'] = tkinter.DISABLED
    else:
        pw = ent_pw.get()
        btn_ok['state'] = tkinter.NORMAL


lb = Label(window, text="input pulse width : ")
lb.place(x=30, y=80)
ent_pw = Entry(window)
ent_pw.place(x=150, y=80)
btn_pw = Button(window, text='save pw', command=savePw)
btn_pw.place(x=300, y=80)

btn_ok = Button(window, text="OK", width=10,
                state=tkinter.DISABLED, command=readDirectory)
btn_ok.place(x=120, y=120)

window.mainloop()
