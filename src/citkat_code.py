import tkinter as tk
import time
import pygame
import PIL, PIL.Image, PIL.ImageTk
import os
import glob
import math

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
        big_arrow_img_path = os.path.join(base, "..", "Imports", "BigArrow.png")
        small_arrow_img_path = os.path.join(base, "..", "Imports", "SmallArrow.png")

        root = tk.Tk()
        root.title("CitKat Clock")
        root.attributes("-topmost", True)
        root.geometry("-0-50")
        root.overrideredirect(True)
        root.wm_attributes('-transparentcolor', 'magenta')
        root.configure(bg='magenta')

        exit_button_image = PIL.ImageTk.PhotoImage(file=exit_button_img_path)
        move_button_image = PIL.ImageTk.PhotoImage(file=move_button_img_path)

        exit_button_label = tk.Label(root, image=exit_button_image, bg='magenta')
        move_button_label = tk.Label(root, image=move_button_image, bg='magenta')

        exit_button_label.grid(column=0, row=0, sticky='ne')
        move_button_label.grid(column=0, row=0, sticky='ne', padx = 32)
        
        exit_button_label.bind("<Button-1>", self.on_click)
        move_button_label.bind("<Button-1>", self.start_move)
        move_button_label.bind("<B1-Motion>", self.on_move)
        
        small_cat = PIL.Image.open(clock_img_path)
        big_arrow = PIL.Image.open(big_arrow_img_path)
        small_arrow = PIL.Image.open(small_arrow_img_path)

        scale_amount = 3
 
        small_cat = small_cat.resize((small_cat.width * scale_amount, small_cat.height * scale_amount), PIL.Image.Resampling.NEAREST)
        big_arrow = big_arrow.resize((big_arrow.width * scale_amount, big_arrow.height * scale_amount), PIL.Image.Resampling.NEAREST)
        small_arrow = small_arrow.resize((small_arrow.width * scale_amount, small_arrow.height * scale_amount), PIL.Image.Resampling.NEAREST)

        self.big_arrow_source = self.make_pivot_image(big_arrow)
        self.small_arrow_source = self.make_pivot_image(small_arrow)

        small_cat_image = PIL.ImageTk.PhotoImage(small_cat)
        big_arrow_tk = PIL.ImageTk.PhotoImage(self.big_arrow_source)
        small_arrow_tk = PIL.ImageTk.PhotoImage(self.small_arrow_source)

        canvas = tk.Canvas(width=small_cat.width, height=small_cat.height, bg='magenta', highlightthickness=0)
        canvas.grid(column=0, row=1, sticky='nw')
        

        center_x = small_cat.width // 2
        center_y = small_cat.height // 2
        
        # Bottom left pivot
        self.clock_center_x = center_x - 2
        self.clock_center_y = center_y - 8

        canvas.create_image(0, 0, anchor=tk.NW, image=small_cat_image)

        # Since our arrow images are now centered squares, we anchor them right in the middle
        self.big_arrow_item = canvas.create_image(self.clock_center_x, self.clock_center_y, anchor=tk.CENTER, image=big_arrow_tk)
        self.small_arrow_item = canvas.create_image(self.clock_center_x, self.clock_center_y, anchor=tk.CENTER, image=small_arrow_tk)

        self.big_arrow_angle = 0 
        self.small_arrow_angle = 0 

        root.bind("<space>", self.rotate_arrows)

        # Store references
        self.canvas = canvas
        self.small_cat_image = small_cat_image
        self.big_arrow_tk = big_arrow_tk
        self.small_arrow_tk = small_arrow_tk
        self.exit_button_image = exit_button_image # Keep ref to avoid garbage collection
        self.move_button_image = move_button_image

        root.mainloop()

    # Button
    def on_click(self, event):
        event.widget.master.destroy()

    def start_move(self, event):
        root = event.widget.master
        self._drag_offset_x = event.x_root - root.winfo_rootx()
        self._drag_offset_y = event.y_root - root.winfo_rooty()

    def on_move(self, event):
        root = event.widget.master
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        root.geometry(f"+{x}+{y}")

    # Background square so the arrows don't get cut off
    def make_pivot_image(self, arrow_img):

        w, h = arrow_img.size
        
        new_side = int(max(w, h) * 4) 
        
        new_img = PIL.Image.new("RGBA", (new_side, new_side), (0, 0, 0, 0))
        
        paste_x = new_side // 2
        paste_y = (new_side // 2) - h
        
        new_img.paste(arrow_img, (paste_x, paste_y))
        return new_img

    def rotate_arrows(self, event):
        """Rotate the big and small arrows."""
        self.big_arrow_angle = (self.big_arrow_angle + 5) % 360
        self.small_arrow_angle = (self.small_arrow_angle + 5) % 360

        rotated_big = self.big_arrow_source.rotate(
            -self.big_arrow_angle,
            resample=PIL.Image.Resampling.NEAREST
        )
        rotated_small = self.small_arrow_source.rotate(
            -self.small_arrow_angle, 
            resample=PIL.Image.Resampling.NEAREST
        )

        self.big_arrow_tk = PIL.ImageTk.PhotoImage(rotated_big)
        self.small_arrow_tk = PIL.ImageTk.PhotoImage(rotated_small)

        self.canvas.itemconfig(self.big_arrow_item, image=self.big_arrow_tk)
        self.canvas.itemconfig(self.small_arrow_item, image=self.small_arrow_tk)


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