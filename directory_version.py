import os
import tkinter
import traceback
import numpy as np
import natsort
from tkinter import *
from tkinter import filedialog
from tkinter import messagebox


def readDirectory():
    global interval
    resultF = open(path + '/result.txt', 'w')
    filelist = os.listdir(path)
    filelist = natsort.natsorted(filelist)
    try:
        for filename in filelist:
            tmp = filename.split('ms')
            interval = tmp[len(tmp)-2]
            with open(os.path.join(path, filename), 'r') as f:
                analyzeData(path, filename, interval, pw, resultF)
        resultF.close()
        print('Complete successfully')
        exitProg = messagebox.askquestion(
            "Complete", "Complete successfully\n Do you want to quit?")
        if exitProg == 'yes':
            window.destroy()

    except:
        resultF.close()
        print(filename)
        traceback.print_exc()
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
        h = copyData[1][0]
        f_0 = copyData[i][1]
        f_1 = copyData[i+1][1]
        copyData[i][2] = (f_1 - f_0)/h

    # find five values in small order
    for i in range(len(copyData)-1, -1, -1):
        if copyData[i][2] < - 0.2:
            x_second_idx = i
            break

    # find time and index of first pulse
    subtract = int(interval) + int(pw)
    subtract_round = subtract / (round(h, 7)*1000)

    x_first_idx = int(x_second_idx - subtract_round)

    try:
        x_first_time = copyData[x_first_idx][0]
        x_second_time = copyData[x_second_idx][0]
        x_first_value = copyData[x_first_idx][1]
        x_second_value = copyData[x_second_idx][1]
        ppf = x_second_value / x_first_value

        print(filename, ' : success')
        resultF.write(str(interval) + '    ' + str(x_first_value) +
                      '    ' + str(x_second_value) + '    ' + str(ppf) + '\n')

    except:
        print(filename, ' : failed')
        traceback.print_exc()
        resultF.write(filename + ' : !!!!! Analyze failed !!!!!\n')


# GUI
window = Tk()
window.title("PPF_comb_20220421")
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
