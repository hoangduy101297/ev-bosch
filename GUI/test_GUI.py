#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.4
#  in conjunction with Tcl version 8.6
#    Jul 09, 2020 01:21:00 PM BST  platform: Linux


import sys
import os
#import xlsxwriter

try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk

try:
    import ttk
    py3 = False
except ImportError:
    import tkinter.ttk as ttk
    py3 = True

import test_GUI_support
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.backends.backend_tkagg import NavigationToolbar2TkAgg
 
# Implement the default Matplotlib key bindings.
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure
import matplotlib.animation as animation
import numpy as np

#Global Var
top = None
var_en_Accel = None
var_en_Brk = None
var_en_VehSpd = None
var_en_Trq = None
var_en_Console = None

#0: Spd, 1: Trq
g_fig = [None, None]
g_canvas = [None, None]

spd_data = []
trq_data = []
time_data = []
time = 0

def vp_start_gui(root):
    '''Starting point when module is the main routine.'''
    global val, w, spd_fig, g_fig, g_canvas, top
    #root = tk.Tk()
    root.tk.call('wm', 'iconphoto',root._w, tk.PhotoImage(file = os.path.realpath('..')+'/ev-bosch/GUI/icon.png'))
    test_GUI_support.set_Tk_var()
    top = GUI (root)
    
    init_textVar()

    test_GUI_support.init(root, top)


    g_fig[0], g_canvas[0] = create_fig(top.TNotebook1_t1_8)
    g_fig[1], g_canvas[1] = create_fig(top.TNotebook1_t2_9)
    
    logo = tk.PhotoImage(file= os.path.realpath('..')+'/ev-bosch/GUI/logo.png')
    logo_label = tk.Label(root, image = logo)
    logo_label.configure(background = "#d6c7c7")
    logo_label.place(relx=0.015, rely=0.015) 
    
    #return top
    root.mainloop()

def init_textVar():
    global var_en_Accel, var_en_VehSpd, var_en_Brk, var_en_Trq, var_en_Console
    
    var_en_Accel = tk.StringVar()
    var_en_Brk = tk.StringVar()
    var_en_VehSpd = tk.StringVar()
    var_en_Trq = tk.StringVar()
    var_en_Console = tk.StringVar()

def create_fig(parent):
    fig = Figure(dpi=100)
    fig.add_subplot(111, ylim = ([0,255]), xlim = ([0,100])).plot(0, 0, color = 'r')
    
    canvas = FigureCanvasTkAgg(fig, master=parent)  # A tk.DrawingArea.
    canvas.draw()
    
    toolbar = NavigationToolbar2TkAgg(canvas, parent)
    toolbar.update()
    canvas.get_tk_widget().pack(padx = 10, pady = 10, fill = 'x', expand = 1)
    
    return fig, canvas

def GUI_callback(new_data):
     
    update_data(new_data)
    update_fig()

def update_data(new_data):
    # 0:Spd, 1:Crnt, 2: UBat, 3: Brk, 4: UMotor, 5: Temp, 6: iBat 
    global spd_data, trq_data, time_data, time, var_en_Accel, var_en_VehSpd, var_en_Brk, var_en_Trq 
    
    var_en_Accel.set(new_data[1])#dummy
    var_en_Brk.set(new_data[3])
    var_en_VehSpd.set(new_data[0])
    var_en_Trq.set(new_data[4]) #dummy
    
    spd_data.append(new_data[0])
    trq_data.append(new_data[3])#dummy
    
    time = time + 0.1
    time_data.append(time)

def update_fig(): 
    g_fig[0].add_subplot(111, ylim = ([0,255]), xlim = ([0,100])).plot(time_data, spd_data, color = 'r')
    g_canvas[0].draw()
    
    g_fig[1].add_subplot(111, ylim = ([0,255]), xlim = ([0,100])).plot(time_data, trq_data, color = 'r')
    g_canvas[1].draw()

def send_can_cmd():
    global var_en_Console
    text = top.en_Cmd.get()   
    #var_en_Console.set(text)
    
    print(text)
        
    console_text = "Set Vehicle Speed Limit to "+text+" km/h"
    top.en_Console.delete(1.0, tk.END)
    top.en_Console.insert(tk.END, console_text)
    
#############################################
##########Generated Function#################
#############################################

w = None
def create_GUI(rt, *args, **kwargs):
    '''Starting point when module is imported by another module.
       Correct form of call: 'create_GUI(root, *args, **kwargs)' .'''
    global w, w_win, root
    #rt = root
    root = rt
    w = tk.Toplevel (root)
    test_GUI_support.set_Tk_var()
    top = GUI (w)
    test_GUI_support.init(w, top, *args, **kwargs)
    return (w, top)

def destroy_GUI():
    global w
    w.destroy()
    w = None

class GUI:
    def __init__(self, top=None):
        '''This class configures and populates the toplevel window.
           top is the toplevel containing window.'''
        _bgcolor = '#d9d9d9'  # X11 color: 'gray85'
        _fgcolor = '#000000'  # X11 color: 'black'
        _compcolor = '#d9d9d9' # X11 color: 'gray85'
        _ana1color = '#d9d9d9' # X11 color: 'gray85'
        _ana2color = '#ececec' # Closest X11 color: 'gray92'
        self.style = ttk.Style()
        if sys.platform == "win32":
            self.style.theme_use('winnative')
        self.style.configure('.',background=_bgcolor)
        self.style.configure('.',foreground=_fgcolor)
        self.style.configure('.',font="TkDefaultFont")
        self.style.map('.',background=
            [('selected', _compcolor), ('active',_ana2color)])

        top.geometry("1340x759+360+174")
        top.minsize(1, 1)
        top.maxsize(1920, 1200)
        top.resizable(1, 1)
        top.title("EV GUI")
        top.configure(background="#d6c7c7")
        top.configure(highlightbackground="#d8d8d8")
        top.configure(highlightcolor="black")
        top.configure(highlightthickness="1")

        self.prj_name = tk.Message(top)
        self.prj_name.place(relx=0.125, rely=0.009, relheight=0.059
                , relwidth=0.219)
        self.prj_name.configure(background="#d6c7c7")
        self.prj_name.configure(font="-family {DejaVu Serif} -size 15 -weight normal -slant roman -underline 0 -overstrike 0")
        self.prj_name.configure(foreground="#ff0000")
        self.prj_name.configure(highlightbackground="#d6c7c7")
        self.prj_name.configure(highlightthickness="1")
        self.prj_name.configure(text='''EV Project @ RBVH/EJV''')
        self.prj_name.configure(width=293)

        self.menubar = tk.Menu(top,font="TkMenuFont",bg=_bgcolor,fg=_fgcolor)
        top.configure(menu = self.menubar)

        self.Labelframe1 = tk.LabelFrame(top)
        self.Labelframe1.place(relx=0.513, rely=0.09, relheight=0.246
                , relwidth=0.472)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Data Output''')
        self.Labelframe1.configure(background="#faffba")

        self.lb_VehSpd = tk.Label(self.Labelframe1)
        self.lb_VehSpd.place(relx=0.036, rely=0.214, height=31, width=70
                , bordermode='ignore')
        self.lb_VehSpd.configure(activebackground="#f9f9f9")
        self.lb_VehSpd.configure(background="#faffba")
        self.lb_VehSpd.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_VehSpd.configure(text='''Speed''')

        self.en_VehSpd = tk.Entry(self.Labelframe1, textvariable = var_en_VehSpd)
        self.en_VehSpd.place(relx=0.149, rely=0.171, height=43, relwidth=0.326
                , bordermode='ignore')
        self.en_VehSpd.configure(background="white")
        self.en_VehSpd.configure(cursor="")
        self.en_VehSpd.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_VehSpd.configure(selectbackground="#c4c4c4")

        self.lb_Trq = tk.Label(self.Labelframe1)
        self.lb_Trq.place(relx=0.506, rely=0.588, height=31, width=71
                , bordermode='ignore')
        self.lb_Trq.configure(activebackground="#f9f9f9")
        self.lb_Trq.configure(background="#faffba")
        self.lb_Trq.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_Trq.configure(text='''Torque''')

        self.lb_Brk = tk.Label(self.Labelframe1)
        self.lb_Brk.place(relx=0.517, rely=0.203, height=31, width=70
                , bordermode='ignore')
        self.lb_Brk.configure(activebackground="#f9f9f9")
        self.lb_Brk.configure(background="#faffba")
        self.lb_Brk.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_Brk.configure(text='''Brake''')

        self.la_Acc = tk.Label(self.Labelframe1)
        self.la_Acc.place(relx=0.04, rely=0.588, height=32, width=70
                , bordermode='ignore')
        self.la_Acc.configure(activebackground="#f9f9f9")
        self.la_Acc.configure(background="#faffba")
        self.la_Acc.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.la_Acc.configure(text='''ACC''')

        self.en_Trq = tk.Entry(self.Labelframe1, textvariable = var_en_Trq)
        self.en_Trq.place(relx=0.625, rely=0.545, height=43, relwidth=0.326
                , bordermode='ignore')
        self.en_Trq.configure(background="white")
        self.en_Trq.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_Trq.configure(selectbackground="#c4c4c4")

        self.en_Brk = tk.Entry(self.Labelframe1, textvariable = var_en_Brk)
        self.en_Brk.place(relx=0.623, rely=0.171, height=43, relwidth=0.326
                , bordermode='ignore')
        self.en_Brk.configure(background="white")
        self.en_Brk.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_Brk.configure(selectbackground="#c4c4c4")

        self.en_Acc = tk.Entry(self.Labelframe1, textvariable = var_en_Accel)
        self.en_Acc.place(relx=0.149, rely=0.54, height=43, relwidth=0.326
                , bordermode='ignore')
        self.en_Acc.configure(background="white")
        self.en_Acc.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_Acc.configure(selectbackground="#c4c4c4")

        self.Labelframe1_6 = tk.LabelFrame(top)
        self.Labelframe1_6.place(relx=0.028, rely=0.366, relheight=0.586
                , relwidth=0.469)
        self.Labelframe1_6.configure(relief='raised')
        self.Labelframe1_6.configure(relief="raised")
        self.Labelframe1_6.configure(text='''Control Board''')
        self.Labelframe1_6.configure(background="#a3f9ff")
        self.Labelframe1_6.configure(highlightbackground="#000000")

        self.rdBtn_Mode_Eco = tk.Radiobutton(self.Labelframe1_6)
        self.rdBtn_Mode_Eco.place(relx=0.273, rely=0.124, relheight=0.049
                , relwidth=0.146, bordermode='ignore')
        self.rdBtn_Mode_Eco.configure(activebackground="#93e0e5")
        self.rdBtn_Mode_Eco.configure(background="#a3f9ff")
        self.rdBtn_Mode_Eco.configure(cursor="hand2")
        self.rdBtn_Mode_Eco.configure(font="-family {DejaVu Sans} -size 16 -weight normal -slant roman -underline 0 -overstrike 0")
        self.rdBtn_Mode_Eco.configure(highlightbackground="#a3f9ff")
        self.rdBtn_Mode_Eco.configure(justify='left')
        self.rdBtn_Mode_Eco.configure(text='''ECO''')
        self.rdBtn_Mode_Eco.configure(value="MODE_ECO")
        self.rdBtn_Mode_Eco.configure(variable=test_GUI_support.vehMode)

        self.rdBtn_Mode_Spt = tk.Radiobutton(self.Labelframe1_6)
        self.rdBtn_Mode_Spt.place(relx=0.455, rely=0.119, relheight=0.052
                , relwidth=0.175, bordermode='ignore')
        self.rdBtn_Mode_Spt.configure(activebackground="#93e0e5")
        self.rdBtn_Mode_Spt.configure(background="#a3f9ff")
        self.rdBtn_Mode_Spt.configure(cursor="hand2")
        self.rdBtn_Mode_Spt.configure(font="-family {DejaVu Sans} -size 16 -weight normal -slant roman -underline 0 -overstrike 0")
        self.rdBtn_Mode_Spt.configure(highlightbackground="#a3f9ff")
        self.rdBtn_Mode_Spt.configure(justify='left')
        self.rdBtn_Mode_Spt.configure(text='''Sport''')
        self.rdBtn_Mode_Spt.configure(value="MODE_SPORT")
        self.rdBtn_Mode_Spt.configure(variable=test_GUI_support.vehMode)

        self.rdBtn_Mode_3 = tk.Radiobutton(self.Labelframe1_6)
        self.rdBtn_Mode_3.place(relx=0.641, rely=0.117, relheight=0.056
                , relwidth=0.226, bordermode='ignore')
        self.rdBtn_Mode_3.configure(activebackground="#93e0e5")
        self.rdBtn_Mode_3.configure(background="#a3f9ff")
        self.rdBtn_Mode_3.configure(borderwidth="0")
        self.rdBtn_Mode_3.configure(cursor="hand2")
        self.rdBtn_Mode_3.configure(font="-family {DejaVu Sans} -size 16 -weight normal -slant roman -underline 0 -overstrike 0")
        self.rdBtn_Mode_3.configure(highlightbackground="#a3f9ff")
        self.rdBtn_Mode_3.configure(justify='left')
        self.rdBtn_Mode_3.configure(text='''MODE_3''')
        self.rdBtn_Mode_3.configure(value="mode3")
        self.rdBtn_Mode_3.configure(variable=test_GUI_support.vehMode)

        self.en_Cmd = tk.Entry(self.Labelframe1_6)
        self.en_Cmd.place(relx=0.302, rely=0.245, height=33, relwidth=0.486
                , bordermode='ignore')
        self.en_Cmd.configure(background="white")
        self.en_Cmd.configure(font="TkFixedFont")
        self.en_Cmd.configure(selectbackground="#c4c4c4")

        self.lb_Mode = tk.Label(self.Labelframe1_6)
        self.lb_Mode.place(relx=0.159, rely=0.115, height=31, width=80
                , bordermode='ignore')
        self.lb_Mode.configure(activebackground="#f9f9f9")
        self.lb_Mode.configure(background="#a3f9ff")
        self.lb_Mode.configure(font="-family {DejaVu Sans} -size 16 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_Mode.configure(text='''Mode''')

        self.lb_Cmd = tk.Label(self.Labelframe1_6)
        self.lb_Cmd.place(relx=0.078, rely=0.247, height=31, width=131
                , bordermode='ignore')
        self.lb_Cmd.configure(activebackground="#f9f9f9")
        self.lb_Cmd.configure(background="#a3f9ff")
        self.lb_Cmd.configure(font="-family {DejaVu Sans} -size 16 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_Cmd.configure(text='''Command''')

        self.btn_Unlock = tk.Button(self.Labelframe1_6)
        self.btn_Unlock.place(relx=0.079, rely=0.697, height=101, width=151
                , bordermode='ignore')
        self.btn_Unlock.configure(activebackground="#46ff03")
        self.btn_Unlock.configure(activeforeground="#ffffff")
        self.btn_Unlock.configure(background="#46ff03")
        self.btn_Unlock.configure(borderwidth="5")
        self.btn_Unlock.configure(cursor="hand2")
        self.btn_Unlock.configure(font="-family {DejaVu Sans} -size 19 -weight bold -slant roman -underline 0 -overstrike 0")
        self.btn_Unlock.configure(highlightbackground="#ffffff")
        self.btn_Unlock.configure(highlightcolor="#ffffff")
        self.btn_Unlock.configure(highlightthickness="3")
        self.btn_Unlock.configure(overrelief="groove")
        self.btn_Unlock.configure(relief="groove")
        self.btn_Unlock.configure(text='''UNLOCK''')

        self.btn_Lock = tk.Button(self.Labelframe1_6)
        self.btn_Lock.place(relx=0.382, rely=0.697, height=101, width=151
                , bordermode='ignore')
        self.btn_Lock.configure(activebackground="#f7ff0f")
        self.btn_Lock.configure(activeforeground="#ffffff")
        self.btn_Lock.configure(background="#f7ff0f")
        self.btn_Lock.configure(borderwidth="5")
        self.btn_Lock.configure(cursor="hand2")
        self.btn_Lock.configure(font="-family {DejaVu Sans} -size 20 -weight bold -slant roman -underline 0 -overstrike 0")
        self.btn_Lock.configure(highlightbackground="#ffffff")
        self.btn_Lock.configure(highlightcolor="#ffffff")
        self.btn_Lock.configure(highlightthickness="3")
        self.btn_Lock.configure(overrelief="groove")
        self.btn_Lock.configure(relief="groove")
        self.btn_Lock.configure(text='''LOCK''')

        self.btn_Lock_5 = tk.Button(self.Labelframe1_6)
        self.btn_Lock_5.place(relx=0.684, rely=0.694, height=101, width=151
                , bordermode='ignore')
        self.btn_Lock_5.configure(activebackground="#ff0000")
        self.btn_Lock_5.configure(activeforeground="white")
        self.btn_Lock_5.configure(activeforeground="#ffffff")
        self.btn_Lock_5.configure(background="#ff0000")
        self.btn_Lock_5.configure(borderwidth="5")
        self.btn_Lock_5.configure(cursor="hand2")
        self.btn_Lock_5.configure(font="-family {DejaVu Sans} -size 20 -weight bold -slant roman -underline 0 -overstrike 0")
        self.btn_Lock_5.configure(highlightbackground="#ffffff")
        self.btn_Lock_5.configure(highlightcolor="#ffffff")
        self.btn_Lock_5.configure(highlightthickness="3")
        self.btn_Lock_5.configure(overrelief="groove")
        self.btn_Lock_5.configure(relief="groove")
        self.btn_Lock_5.configure(text='''STOP''')

        self.btn_CmdSend = tk.Button(self.Labelframe1_6, command = send_can_cmd)
        self.btn_CmdSend.place(relx=0.819, rely=0.249, height=31, width=73
                , bordermode='ignore')
        self.btn_CmdSend.configure(activebackground="#f9f9f9")
        self.btn_CmdSend.configure(cursor="fleur")
        self.btn_CmdSend.configure(text='''Send''')

        self.en_Console = tk.Text(self.Labelframe1_6)
        self.en_Console.place(relx=0.079, rely=0.449, height=93, relwidth=0.836
                , bordermode='ignore')
        self.en_Console.configure(background="#ffffffffffff")
        self.en_Console.configure(font="TkFixedFont")
        self.en_Console.configure(selectbackground="blue")
        self.en_Console.configure(selectforeground="white")

        self.lb_Console = tk.Label(self.Labelframe1_6)
        self.lb_Console.place(relx=0.064, rely=0.382, height=21, width=110
                , bordermode='ignore')
        self.lb_Console.configure(activebackground="#f9f9f9")
        self.lb_Console.configure(background="#a3f9ff")
        self.lb_Console.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.lb_Console.configure(text='''Console''')

        self.Labelframe1_7 = tk.LabelFrame(top)
        self.Labelframe1_7.place(relx=0.513, rely=0.366, relheight=0.586
                , relwidth=0.47)
        self.Labelframe1_7.configure(relief='groove')
        self.Labelframe1_7.configure(text='''Graph''')
        self.Labelframe1_7.configure(highlightcolor="#ffffff")

        self.style.configure('TNotebook.Tab', background=_bgcolor)
        self.style.configure('TNotebook.Tab', foreground=_fgcolor)
        self.style.map('TNotebook.Tab', background=
            [('selected', _compcolor), ('active',_ana2color)])
        self.TNotebook1_7 = ttk.Notebook(self.Labelframe1_7)
        self.TNotebook1_7.place(relx=0.016, rely=0.045, relheight=0.935
                , relwidth=0.971, bordermode='ignore')
        self.TNotebook1_7.configure(takefocus="")
        self.TNotebook1_t1_8 = tk.Frame(self.TNotebook1_7)
        self.TNotebook1_7.add(self.TNotebook1_t1_8, padding=3)
        self.TNotebook1_7.tab(0, text="Speed",compound="left",underline="-1",)
        self.TNotebook1_t1_8.configure(relief="groove")
        self.TNotebook1_t2_9 = tk.Frame(self.TNotebook1_7)
        self.TNotebook1_7.add(self.TNotebook1_t2_9, padding=3)
        self.TNotebook1_7.tab(1, text="Torque",compound="left",underline="-1",)

        self.Labelframe1_8 = tk.LabelFrame(top)
        self.Labelframe1_8.place(relx=0.03, rely=0.092, relheight=0.242
                , relwidth=0.471)
        self.Labelframe1_8.configure(relief='groove')
        self.Labelframe1_8.configure(text='''Torque Formular''')
        self.Labelframe1_8.configure(highlightcolor="#ffffff")

        self.TNotebook1_8 = ttk.Notebook(self.Labelframe1_8)
        self.TNotebook1_8.place(relx=0.016, rely=0.109, relheight=0.88
                , relwidth=0.971, bordermode='ignore')
        self.TNotebook1_8.configure(takefocus="")
        self.TNotebook1t1_9 = tk.Frame(self.TNotebook1_8)
        self.TNotebook1_8.add(self.TNotebook1t1_9, padding=3)
        self.TNotebook1_8.tab(0, text="Level 1", compound="left", underline="-1"
                ,)
        self.TNotebook1t1_9.configure(relief="groove")
        self.TNotebook1t2_10 = tk.Frame(self.TNotebook1_8)
        self.TNotebook1_8.add(self.TNotebook1t2_10, padding=3)
        self.TNotebook1_8.tab(1, text="Level 2", compound="left", underline="-1"
                ,)
        self.TNotebook1_8_t1 = tk.Frame(self.TNotebook1_8)
        self.TNotebook1_8.add(self.TNotebook1_8_t1, padding=3)
        self.TNotebook1_8.tab(2, text="Level 3", compound="left", underline="-1"
                ,)

        self.btn_Update_TF = tk.Button(self.TNotebook1t1_9)
        self.btn_Update_TF.place(relx=0.867, rely=0.515, height=41, width=67)
        self.btn_Update_TF.configure(activebackground="#f9f9f9")
        self.btn_Update_TF.configure(text='''Update''')

        self.Label1 = tk.Label(self.TNotebook1t1_9)
        self.Label1.place(relx=0.052, rely=0.147, height=31, width=70)
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(font="-family {DejaVu Sans} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1.configure(text='''Trq =''')

        self.Label1_15 = tk.Label(self.TNotebook1t1_9)
        self.Label1_15.place(relx=0.268, rely=0.147, height=31, width=140)
        self.Label1_15.configure(activebackground="#f9f9f9")
        self.Label1_15.configure(font="-family {DejaVu Sans} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_15.configure(text='''x Trq(ACC) -''')

        self.Label1_16 = tk.Label(self.TNotebook1t1_9)
        self.Label1_16.place(relx=0.607, rely=0.147, height=31, width=140)
        self.Label1_16.configure(activebackground="#f9f9f9")
        self.Label1_16.configure(font="-family {DejaVu Sans} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_16.configure(text='''x Trq(Brk) -''')

        self.en_K1 = tk.Entry(self.TNotebook1t1_9)
        self.en_K1.place(relx=0.172, rely=0.147,height=33, relwidth=0.092)
        self.en_K1.configure(background="white")
        self.en_K1.configure(font="-family {Liberation Mono} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_K1.configure(selectbackground="blue")
        self.en_K1.configure(selectforeground="white")

        self.en_K2 = tk.Entry(self.TNotebook1t1_9)
        self.en_K2.place(relx=0.512, rely=0.147,height=33, relwidth=0.092)
        self.en_K2.configure(background="white")
        self.en_K2.configure(font="-family {Liberation Mono} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_K2.configure(selectbackground="blue")
        self.en_K2.configure(selectforeground="white")

        self.en_const = tk.Entry(self.TNotebook1t1_9)
        self.en_const.place(relx=0.851, rely=0.147,height=33, relwidth=0.092)
        self.en_const.configure(background="white")
        self.en_const.configure(font="-family {Liberation Mono} -size 17 -weight normal -slant roman -underline 0 -overstrike 0")
        self.en_const.configure(selectbackground="blue")
        self.en_const.configure(selectforeground="white")

        self.Frame1 = tk.Frame(self.TNotebook1t1_9)
        self.Frame1.place(relx=0.016, rely=0.449, relheight=0.478
                , relwidth=0.843)
        self.Frame1.configure(relief='groove')
        self.Frame1.configure(borderwidth="2")
        self.Frame1.configure(relief="groove")

        self.Message1 = tk.Message(self.Frame1)
        self.Message1.place(relx=0.008, rely=0.031, relheight=0.846
                , relwidth=0.975)
        self.Message1.configure(anchor='sw')
        self.Message1.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Message1.configure(padx="0")
        self.Message1.configure(pady="0")
        self.Message1.configure(text='''Description: User gives the value of K1, K2 and Power-Loss Constant (C)''')
        self.Message1.configure(width=502)

        
    @staticmethod
    def popup1(event, *args, **kwargs):
        Popupmenu1 = tk.Menu(root, tearoff=0)
        Popupmenu1.configure(activebackground="#f9f9f9")
        Popupmenu1.post(event.x_root, event.y_root)

    @staticmethod
    def popup2(event, *args, **kwargs):
        Popupmenu2 = tk.Menu(root, tearoff=0)
        Popupmenu2.configure(activebackground="#f9f9f9")
        Popupmenu2.post(event.x_root, event.y_root)

    @staticmethod
    def popup3(event, *args, **kwargs):
        Popupmenu3 = tk.Menu(root, tearoff=0)
        Popupmenu3.configure(activebackground="#f9f9f9")
        Popupmenu3.post(event.x_root, event.y_root)

    @staticmethod
    def popup4(event, *args, **kwargs):
        Popupmenu4 = tk.Menu(root, tearoff=0)
        Popupmenu4.configure(activebackground="#f9f9f9")
        Popupmenu4.post(event.x_root, event.y_root)

    @staticmethod
    def popup5(event, *args, **kwargs):
        Popupmenu5 = tk.Menu(root, tearoff=0)
        Popupmenu5.configure(activebackground="#f9f9f9")
        Popupmenu5.post(event.x_root, event.y_root)

    @staticmethod
    def popup6(event, *args, **kwargs):
        Popupmenu6 = tk.Menu(root, tearoff=0)
        Popupmenu6.configure(activebackground="#f9f9f9")
        Popupmenu6.post(event.x_root, event.y_root)

    @staticmethod
    def popup7(event, *args, **kwargs):
        Popupmenu7 = tk.Menu(root, tearoff=0)
        Popupmenu7.configure(activebackground="#f9f9f9")
        Popupmenu7.post(event.x_root, event.y_root)

    @staticmethod
    def popup8(event, *args, **kwargs):
        Popupmenu8 = tk.Menu(root, tearoff=0)
        Popupmenu8.configure(activebackground="#f9f9f9")
        Popupmenu8.post(event.x_root, event.y_root)

    @staticmethod
    def popup9(event, *args, **kwargs):
        Popupmenu9 = tk.Menu(root, tearoff=0)
        Popupmenu9.configure(activebackground="#f9f9f9")
        Popupmenu9.post(event.x_root, event.y_root)

    @staticmethod
    def popup10(event, *args, **kwargs):
        Popupmenu10 = tk.Menu(root, tearoff=0)
        Popupmenu10.configure(activebackground="#f9f9f9")
        Popupmenu10.post(event.x_root, event.y_root)

    @staticmethod
    def popup11(event, *args, **kwargs):
        Popupmenu11 = tk.Menu(root, tearoff=0)
        Popupmenu11.configure(activebackground="#f9f9f9")
        Popupmenu11.post(event.x_root, event.y_root)
        



if __name__ == '__main__':
    vp_start_gui()





