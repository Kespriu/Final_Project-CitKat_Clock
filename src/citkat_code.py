import tkinter as tk
import time
import pygame
import PIL, PIL.Image, PIL.ImageTk
import os
import glob

# Getting an actual widget on screen and getting it to move around. (Make pixel art of CitKat Clock).
# Getting the desktop toy to be pinned above other applications.
# Implementing the text bubbles and having them pop up when the Kat is clicked on.
# Making dialogue options for said text bubbles.
# Getting the clock on the Kats Tummy to tell the time and show it in real time through animation.
# Getting the clock to pop up when clicked on and final touch ups.

class ClockImageImport(): 

    def __init__(self):

        base = os.path.dirname(os.path.abspath(__file__))

        clock_img_path = os.path.join(base, "..", "Imports", "CitKatClock.png")
        exit_button_img_path = os.path.join(base, "..", "Imports", "ExitButton.png")
        move_button_img_path = os.path.join(base, "..", "Imports", "MoveButton.png")

        root = tk.Tk(className="CitKatClock")

        # Window starts in bottom right corner
        root.geometry("-0-50")

        # Remove title bar and borders
        root.overrideredirect(True)

        root.configure(bg='magenta')
        root.wm_attributes('-transparentcolor', 'magenta')

        lbl = tk.Label(root, text="Hello", bg='black', fg='white', padx=20, pady=10)

        img = PIL.ImageTk.PhotoImage(file=exit_button_img_path)
        img2 = PIL.ImageTk.PhotoImage(file=move_button_img_path)
        lbl1 = tk.Label(root, image=img, bg='magenta')
        lbl2 = tk.Label(root, image=img2, bg='magenta')

        lbl1.grid(column=0, row=0, sticky='ne')
        lbl2.grid(column=0, row=0, sticky='ne', padx = 32)

        lbl1.bind("<Button-1>", self.on_click)
        lbl2.bind("<Button-1>", self.start_move)
        lbl2.bind("<B1-Motion>", self.on_move)
        
        small_cat = PIL.Image.open(clock_img_path)
        small_cat = small_cat.resize((132, 417), PIL.Image.Resampling.NEAREST)
        small_cat_image = PIL.ImageTk.PhotoImage(small_cat)
        canvas = tk.Canvas(width=small_cat.width + 100, height=small_cat.height + 100, bg='magenta', highlightthickness=0)
        canvas.grid(column=0, row=1, sticky='nw')
        canvas.create_image(50, 50, anchor=tk.NW, image=small_cat_image)

        root.mainloop()

    def on_click(self, event):
        #print("Exit button clicked")
        event.widget.master.destroy()

    def start_move(self, event):
        root = event.widget.master
        self._drag_offset_x = event.x_root - root.winfo_rootx()
        self._drag_offset_y = event.y_root - root.winfo_rooty()

    def on_move(self, event):
        #print("Move button clicked")
        root = event.widget.master
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        root.geometry(f"+{x}+{y}")


class ClockFaceAnimation():

    def __init__(self):
        pass
        
class TailAnimation():

    def __init__(self):
        pass
class DialougeChoices():

    def __init__(self):
        pass

class Pinning():

    def __init__(self):
        pass

def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())

def main():
    ClockImageImport()
    ClockFaceAnimation()
    TailAnimation()
    DialougeChoices()
    Pinning()

if __name__ == "__main__":
    main()