#! /usr/bin/env python
#  -*- coding: utf-8 -*-
#
# GUI module generated by PAGE version 5.3
#  in conjunction with Tcl version 8.6
#    Jun 27, 2020 12:26:22 PM BST  platform: Linux

import sys

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

def vp_start_gui():
    '''Starting point when module is the main routine.'''
    global val, w, root
    root = tk.Tk()
    test_GUI_support.set_Tk_var()
    top = GUI (root)
    test_GUI_support.init(root, top)
    logo = tk.PhotoImage(file="download.png")
    logo_label = tk.Label(root, image = logo)
    logo_label.place(relx=0.015, rely=0.015)
    logo_label.configure(background = "#d6c7c7")
    root.mainloop()

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

        top.geometry("1340x759+259+134")
        top.minsize(1, 1)
        top.maxsize(1920, 1200)
        top.resizable(1, 1)
        top.title("EV GUI")
        top.configure(background="#d6c7c7")
        top.configure(highlightbackground="#d8d8d8")
        top.configure(highlightcolor="black")
        top.configure(highlightthickness="1")

        self.prj_name = tk.Message(top)
        self.prj_name.place(relx=0.119, rely=0.009, relheight=0.059
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
        self.Labelframe1.place(relx=0.028, rely=0.09, relheight=0.244
                , relwidth=0.955)
        self.Labelframe1.configure(relief='groove')
        self.Labelframe1.configure(text='''Block 1''')
        self.Labelframe1.configure(background="#a0d8ba")

        self.Label1 = tk.Label(self.Labelframe1)
        self.Label1.place(relx=0.039, rely=0.216, height=31, width=70
                , bordermode='ignore')
        self.Label1.configure(activebackground="#f9f9f9")
        self.Label1.configure(background="#a0d8ba")
        self.Label1.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1.configure(text='''Label''')

        self.Entry1 = tk.Entry(self.Labelframe1)
        self.Entry1.place(relx=0.094, rely=0.162, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1.configure(background="white")
        self.Entry1.configure(font="TkFixedFont")
        self.Entry1.configure(selectbackground="#c4c4c4")

        self.Label1_8 = tk.Label(self.Labelframe1)
        self.Label1_8.place(relx=0.039, rely=0.595, height=31, width=70
                , bordermode='ignore')
        self.Label1_8.configure(activebackground="#f9f9f9")
        self.Label1_8.configure(background="#a0d8ba")
        self.Label1_8.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_8.configure(text='''Label''')

        self.Label1_9 = tk.Label(self.Labelframe1)
        self.Label1_9.place(relx=0.383, rely=0.216, height=31, width=70
                , bordermode='ignore')
        self.Label1_9.configure(activebackground="#f9f9f9")
        self.Label1_9.configure(background="#a0d8ba")
        self.Label1_9.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_9.configure(text='''Label''')

        self.Label1_10 = tk.Label(self.Labelframe1)
        self.Label1_10.place(relx=0.383, rely=0.595, height=31, width=70
                , bordermode='ignore')
        self.Label1_10.configure(activebackground="#f9f9f9")
        self.Label1_10.configure(background="#a0d8ba")
        self.Label1_10.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_10.configure(text='''Label''')

        self.Label1_11 = tk.Label(self.Labelframe1)
        self.Label1_11.place(relx=0.711, rely=0.216, height=31, width=70
                , bordermode='ignore')
        self.Label1_11.configure(activebackground="#f9f9f9")
        self.Label1_11.configure(background="#a0d8ba")
        self.Label1_11.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_11.configure(text='''Label''')

        self.Label1_12 = tk.Label(self.Labelframe1)
        self.Label1_12.place(relx=0.711, rely=0.595, height=31, width=70
                , bordermode='ignore')
        self.Label1_12.configure(activebackground="#f9f9f9")
        self.Label1_12.configure(background="#a0d8ba")
        self.Label1_12.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_12.configure(text='''Label''')

        self.Entry1_13 = tk.Entry(self.Labelframe1)
        self.Entry1_13.place(relx=0.094, rely=0.541, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1_13.configure(background="white")
        self.Entry1_13.configure(font="TkFixedFont")
        self.Entry1_13.configure(selectbackground="#c4c4c4")

        self.Entry1_14 = tk.Entry(self.Labelframe1)
        self.Entry1_14.place(relx=0.438, rely=0.162, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1_14.configure(background="white")
        self.Entry1_14.configure(font="TkFixedFont")
        self.Entry1_14.configure(selectbackground="#c4c4c4")

        self.Entry1_15 = tk.Entry(self.Labelframe1)
        self.Entry1_15.place(relx=0.438, rely=0.541, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1_15.configure(background="white")
        self.Entry1_15.configure(font="TkFixedFont")
        self.Entry1_15.configure(selectbackground="#c4c4c4")

        self.Entry1_16 = tk.Entry(self.Labelframe1)
        self.Entry1_16.place(relx=0.766, rely=0.162, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1_16.configure(background="white")
        self.Entry1_16.configure(font="TkFixedFont")
        self.Entry1_16.configure(selectbackground="#c4c4c4")

        self.Entry1_17 = tk.Entry(self.Labelframe1)
        self.Entry1_17.place(relx=0.766, rely=0.541, height=43, relwidth=0.161
                , bordermode='ignore')
        self.Entry1_17.configure(background="white")
        self.Entry1_17.configure(font="TkFixedFont")
        self.Entry1_17.configure(selectbackground="#c4c4c4")

        self.Labelframe1_6 = tk.LabelFrame(top)
        self.Labelframe1_6.place(relx=0.028, rely=0.366, relheight=0.586
                , relwidth=0.47)
        self.Labelframe1_6.configure(relief='raised')
        self.Labelframe1_6.configure(relief="raised")
        self.Labelframe1_6.configure(text='''Block 2''')
        self.Labelframe1_6.configure(background="#a3f9ff")
        self.Labelframe1_6.configure(cursor="fleur")
        self.Labelframe1_6.configure(highlightbackground="#000000")

        self.Button1 = tk.Button(self.Labelframe1_6)
        self.Button1.place(relx=0.165, rely=0.099, height=31, width=71
                , bordermode='ignore')
        self.Button1.configure(activebackground="#f9f9f9")
        self.Button1.configure(cursor="hand2")
        self.Button1.configure(text='''Button''')

        self.Button1_18 = tk.Button(self.Labelframe1_6)
        self.Button1_18.place(relx=0.165, rely=0.279, height=31, width=71
                , bordermode='ignore')
        self.Button1_18.configure(activebackground="#f9f9f9")
        self.Button1_18.configure(cursor="hand2")
        self.Button1_18.configure(text='''Button''')

        self.Button1_19 = tk.Button(self.Labelframe1_6)
        self.Button1_19.place(relx=0.165, rely=0.458, height=31, width=71
                , bordermode='ignore')
        self.Button1_19.configure(activebackground="#f9f9f9")
        self.Button1_19.configure(cursor="hand2")
        self.Button1_19.configure(text='''Button''')

        self.Button1_20 = tk.Button(self.Labelframe1_6)
        self.Button1_20.place(relx=0.165, rely=0.638, height=31, width=71
                , bordermode='ignore')
        self.Button1_20.configure(activebackground="#f9f9f9")
        self.Button1_20.configure(cursor="hand2")
        self.Button1_20.configure(text='''Button''')

        self.Button1_21 = tk.Button(self.Labelframe1_6)
        self.Button1_21.place(relx=0.163, rely=0.813, height=31, width=71
                , bordermode='ignore')
        self.Button1_21.configure(activebackground="#f9f9f9")
        self.Button1_21.configure(cursor="hand2")
        self.Button1_21.configure(text='''Button''')

        self.Radiobutton1 = tk.Radiobutton(self.Labelframe1_6)
        self.Radiobutton1.place(relx=0.341, rely=0.11, relheight=0.052
                , relwidth=0.111, bordermode='ignore')
        self.Radiobutton1.configure(activebackground="#f9f9f9")
        self.Radiobutton1.configure(background="#a3f9ff")
        self.Radiobutton1.configure(cursor="hand2")
        self.Radiobutton1.configure(highlightbackground="#a3f9ff")
        self.Radiobutton1.configure(justify='left')
        self.Radiobutton1.configure(text='''Radio''')
        self.Radiobutton1.configure(variable=test_GUI_support.selectedButton)

        self.Radiobutton1_1 = tk.Radiobutton(self.Labelframe1_6)
        self.Radiobutton1_1.place(relx=0.559, rely=0.11, relheight=0.052
                , relwidth=0.111, bordermode='ignore')
        self.Radiobutton1_1.configure(activebackground="#f9f9f9")
        self.Radiobutton1_1.configure(background="#a3f9ff")
        self.Radiobutton1_1.configure(cursor="hand2")
        self.Radiobutton1_1.configure(highlightbackground="#a3f9ff")
        self.Radiobutton1_1.configure(justify='left')
        self.Radiobutton1_1.configure(text='''Radio''')
        self.Radiobutton1_1.configure(variable=test_GUI_support.selectedButton)

        self.Radiobutton1_2 = tk.Radiobutton(self.Labelframe1_6)
        self.Radiobutton1_2.place(relx=0.77, rely=0.11, relheight=0.052
                , relwidth=0.111, bordermode='ignore')
        self.Radiobutton1_2.configure(activebackground="#f9f9f9")
        self.Radiobutton1_2.configure(background="#a3f9ff")
        self.Radiobutton1_2.configure(borderwidth="0")
        self.Radiobutton1_2.configure(cursor="hand2")
        self.Radiobutton1_2.configure(highlightbackground="#a3f9ff")
        self.Radiobutton1_2.configure(justify='left')
        self.Radiobutton1_2.configure(text='''Radio''')
        self.Radiobutton1_2.configure(variable=test_GUI_support.selectedButton)

        self.Entry2 = tk.Entry(self.Labelframe1_6)
        self.Entry2.place(relx=0.335, rely=0.27, height=33, relwidth=0.613
                , bordermode='ignore')
        self.Entry2.configure(background="white")
        self.Entry2.configure(font="TkFixedFont")
        self.Entry2.configure(selectbackground="#c4c4c4")

        self.Label1_3 = tk.Label(self.Labelframe1_6)
        self.Label1_3.place(relx=0.029, rely=0.103, height=31, width=70
                , bordermode='ignore')
        self.Label1_3.configure(activebackground="#f9f9f9")
        self.Label1_3.configure(background="#a3f9ff")
        self.Label1_3.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_3.configure(text='''Label''')

        self.Label1_4 = tk.Label(self.Labelframe1_6)
        self.Label1_4.place(relx=0.032, rely=0.283, height=31, width=70
                , bordermode='ignore')
        self.Label1_4.configure(activebackground="#f9f9f9")
        self.Label1_4.configure(background="#a3f9ff")
        self.Label1_4.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_4.configure(text='''Label''')

        self.Label1_1 = tk.Label(self.Labelframe1_6)
        self.Label1_1.place(relx=0.032, rely=0.458, height=31, width=70
                , bordermode='ignore')
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(background="#a3f9ff")
        self.Label1_1.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_1.configure(text='''Label''')

        self.Label1_2 = tk.Label(self.Labelframe1_6)
        self.Label1_2.place(relx=0.032, rely=0.638, height=31, width=70
                , bordermode='ignore')
        self.Label1_2.configure(activebackground="#f9f9f9")
        self.Label1_2.configure(background="#a3f9ff")
        self.Label1_2.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_2.configure(text='''Label''')

        self.Label1_1 = tk.Label(self.Labelframe1_6)
        self.Label1_1.place(relx=0.033, rely=0.818, height=31, width=70
                , bordermode='ignore')
        self.Label1_1.configure(activebackground="#f9f9f9")
        self.Label1_1.configure(background="#a3f9ff")
        self.Label1_1.configure(font="-family {DejaVu Sans} -size 13 -weight normal -slant roman -underline 0 -overstrike 0")
        self.Label1_1.configure(text='''Label''')

        self.Scale1 = tk.Scale(self.Labelframe1_6, from_=0.0, to=100.0)
        self.Scale1.place(relx=0.325, rely=0.429, relwidth=0.625, relheight=0.0
                , height=42, bordermode='ignore')
        self.Scale1.configure(activebackground="#a3f9ff")
        self.Scale1.configure(background="#a3f9ff")
        self.Scale1.configure(cursor="hand2")
        self.Scale1.configure(highlightbackground="#a3f9ff")
        self.Scale1.configure(orient="horizontal")
        self.Scale1.configure(troughcolor="#ffffff")

        self.TCombobox1 = ttk.Combobox(self.Labelframe1_6)
        self.TCombobox1.place(relx=0.333, rely=0.652, relheight=0.047
                , relwidth=0.614, bordermode='ignore')
        self.TCombobox1.configure(textvariable=test_GUI_support.combobox)
        self.TCombobox1.configure(takefocus="")

        self.Labelframe1_7 = tk.LabelFrame(top)
        self.Labelframe1_7.place(relx=0.513, rely=0.366, relheight=0.586
                , relwidth=0.47)
        self.Labelframe1_7.configure(relief='groove')
        self.Labelframe1_7.configure(text='''Block 3''')
        self.Labelframe1_7.configure(background="#fcfcd1")

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





