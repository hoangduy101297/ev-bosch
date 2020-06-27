import Tkinter as tk
#from PIL import ImageTk
#from PIL import Image

#This creates the main window of an application
window = tk.Tk()
logo = tk.PhotoImage(file="download.png")
logo_label = tk.Label(window, image = logo).place(relx=0, rely=0.088)
window.title("Join")
window.geometry("300x300")
window.configure(background='grey')


#Creates a Tkinter-compatible photo image, which can be used everywhere Tkinter expects an image object.
#img = ImageTk.PhotoImage(Image.open(path))

#The Label widget is a standard Tkinter widget used to display a text or image on the screen.
#panel = tk.Label(window, image = img)

#The Pack geometry manager packs widgets in rows or columns.
#panel.pack(side = "bottom", fill = "both", expand = "yes")

#Start the GUI
window.mainloop()

    logo = tk.PhotoImage(file="download.png")
    logo_label = tk.Label(root, image = logo)
    logo_label.place(relx=0.015, rely=0.015)
    logo_label.configure(background = "#d6c7c7")