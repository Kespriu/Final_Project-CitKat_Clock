import tkinter as tk
import time
import PIL, PIL.Image, PIL.ImageTk
import os
import math

class ClockImageImport(): 

    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        
        clock_img_path = os.path.join(base, "..", "Imports", "CitKatClock.png")
        eyes_img_path = os.path.join(base, "..", "Imports", "Eyes.png")
        tail_img_path = os.path.join(base, "..", "Imports", "Tail.png")
        nose_img_path = os.path.join(base, "..", "Imports", "Nose.png")
        
        exit_button_img_path = os.path.join(base, "..", "Imports", "ExitButton.png")
        move_button_img_path = os.path.join(base, "..", "Imports", "MoveButton.png")

        big_arrow_img_path = os.path.join(base, "..", "Imports", "BigArrow.png")
        small_arrow_img_path = os.path.join(base, "..", "Imports", "SmallArrow.png")

        speech_bubble_img_path = os.path.join(base, "..", "Imports", "SpeechBubble.png")

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

        exit_button_label.grid(column=1, row=0, sticky='ne')
        move_button_label.grid(column=1, row=0, sticky='ne', padx = 32)
        
        exit_button_label.bind("<Button-1>", self.on_click)
        move_button_label.bind("<Button-1>", self.start_move)
        move_button_label.bind("<B1-Motion>", self.on_move)
        
        small_cat = PIL.Image.open(clock_img_path)
        eyes = PIL.Image.open(eyes_img_path)
        tail = PIL.Image.open(tail_img_path)
        nose = PIL.Image.open(nose_img_path)
        big_arrow = PIL.Image.open(big_arrow_img_path)
        small_arrow = PIL.Image.open(small_arrow_img_path)
        temp_speech_bubble = PIL.Image.open(speech_bubble_img_path)

        scale_amount = 3

        small_cat = small_cat.resize((small_cat.width * scale_amount, small_cat.height * scale_amount), PIL.Image.Resampling.NEAREST)
        eyes = eyes.resize((eyes.width * scale_amount, eyes.height * scale_amount), PIL.Image.Resampling.NEAREST)
        tail = tail.resize((tail.width * scale_amount, tail.height * scale_amount), PIL.Image.Resampling.NEAREST)
        nose = nose.resize((nose.width * scale_amount, nose.height * scale_amount), PIL.Image.Resampling.NEAREST)
        big_arrow = big_arrow.resize((big_arrow.width * scale_amount, big_arrow.height * scale_amount), PIL.Image.Resampling.NEAREST)
        small_arrow = small_arrow.resize((small_arrow.width * scale_amount, small_arrow.height * scale_amount), PIL.Image.Resampling.NEAREST)
        temp_speech_bubble = temp_speech_bubble.resize((temp_speech_bubble.width * scale_amount, temp_speech_bubble.height * scale_amount), PIL.Image.Resampling.NEAREST)

        # keep a reference to the image to avoid GC
        speech_bubble_image = PIL.ImageTk.PhotoImage(temp_speech_bubble)
        speech_bubble_label = tk.Label(root, image=speech_bubble_image, bg='magenta')
        # Do NOT grid the speech bubble now — keep it hidden initially
        self.speech_bubble_label = speech_bubble_label
        self.speech_bubble_image = speech_bubble_image
        self.speech_bubble_visible = False

        # Create a transparent placeholder image
        placeholder_image = PIL.Image.new("RGBA", (temp_speech_bubble.width, temp_speech_bubble.height), (0, 0, 0, 0))
        self.placeholder_image = PIL.ImageTk.PhotoImage(placeholder_image)

        # Create the placeholder label
        self.placeholder_label = tk.Label(root, image=self.placeholder_image, bg='magenta')
        self.placeholder_label.grid(column=0, row=1, sticky='nw', padx=20)

        # Initially show the placeholder label
        self.placeholder_label.grid()

        big_arrow_source = self.make_pivot_image(big_arrow)
        small_arrow_source = self.make_pivot_image(small_arrow)

        tail_source_center_pivot = self.make_center_pivot_image(tail)
        nose_source_center_pivot = self.make_center_pivot_image(nose)

        # store the nose source (PIL Image) for pixel-level hit tests
        self.nose_src = nose_source_center_pivot

        small_cat_image = PIL.ImageTk.PhotoImage(small_cat)

        canvas = tk.Canvas(width=small_cat.width, height=small_cat.height, bg='magenta', highlightthickness=0)
        canvas.grid(column=1, row=1, sticky='nw')

        center_x = small_cat.width // 2
        center_y = small_cat.height // 2
        
        # Bottom left pivot for clock
        clock_center_x = center_x - 2
        clock_center_y = center_y - 8

        canvas.create_image(0, 0, anchor=tk.NW, image=small_cat_image)

        # Eyes and tail items
        eyes_item = canvas.create_image(center_x, center_y, anchor=tk.CENTER)
        tail_item = canvas.create_image(center_x - 6, center_y, anchor=tk.CENTER)

        eyes_tk = PIL.ImageTk.PhotoImage(eyes)
        canvas.itemconfig(eyes_item, image=eyes_tk)

        tail_tk_initial = PIL.ImageTk.PhotoImage(tail_source_center_pivot)
        canvas.itemconfig(tail_item, image=tail_tk_initial)

        nose_tk = PIL.ImageTk.PhotoImage(self.nose_src)
        nose_item = canvas.create_image(center_x, center_y, anchor=tk.CENTER)
        canvas.itemconfig(nose_item, image=nose_tk)

        # Keep references
        self.nose_item = nose_item
        self.nose_tk = nose_tk

        # Bind nose click to toggle speech bubble
        canvas.tag_bind(nose_item, "<Button-1>", self.on_nose_click)

        big_arrow_item = canvas.create_image(clock_center_x, clock_center_y, anchor=tk.CENTER)
        small_arrow_item = canvas.create_image(clock_center_x, clock_center_y, anchor=tk.CENTER)

        # Clock arrow anim
        self.animation = ClockFaceAnimation(
            canvas=canvas,
            big_arrow_source=big_arrow_source,
            small_arrow_source=small_arrow_source,
            big_arrow_item=big_arrow_item,
            small_arrow_item=small_arrow_item
        )
        self.animation.start()

        # Other animations
        self.other_animations = OtherAnimations(
            canvas=canvas,
            eyes_item=eyes_item,
            eyes_image_source=eyes,
            tail_item=tail_item,
            tail_image_source_center_pivot=tail_source_center_pivot,
            base_center=(center_x, center_y)
        )
        self.other_animations.start()

        #  refs
        self.root = root
        self.canvas = canvas
        self.small_cat_image = small_cat_image
        self.exit_button_image = exit_button_image
        self.move_button_image = move_button_image
        self.eyes_tk = eyes_tk
        self.tail_tk_initial = tail_tk_initial

        root.mainloop()

    # Button click events
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

    def _pointer_over_nose_sprite(self, event):
        img_coords = self.canvas.coords(self.nose_item)
        if not img_coords:
            return False

        img_x, img_y = img_coords[0], img_coords[1]
        dx = event.x - img_x
        dy = event.y - img_y

        px = int(dx + self.nose_src.width / 2)
        py = int(dy + self.nose_src.height / 2)

        if 0 <= px < self.nose_src.width and 0 <= py < self.nose_src.height:
            pixel = self.nose_src.getpixel((px, py))
            return pixel[3] > 0 if len(pixel) == 4 else any(pixel)
        return False

    def on_nose_click(self, event):
        # Only toggle when the clicked pixel is on the nose sprite
        if not self._pointer_over_nose_sprite(event):
            return

        if self.speech_bubble_visible:
            self.speech_bubble_label.grid_remove()
            self.placeholder_label.grid()  # Show the placeholder
        else:
            self.speech_bubble_label.grid(column=0, row=1, sticky='nw', padx=20)
            self.placeholder_label.grid_remove()  # Hide the placeholder

        self.speech_bubble_visible = not self.speech_bubble_visible

    def make_pivot_image(self, arrow_img):
        w, h = arrow_img.size
        new_side = int(max(w, h) * 4)
        new_img = PIL.Image.new("RGBA", (new_side, new_side), (0, 0, 0, 0))
        paste_x = new_side // 2
        paste_y = (new_side // 2) - h
        new_img.paste(arrow_img, (paste_x, paste_y))
        return new_img

    def make_center_pivot_image(self, img):
        w, h = img.size
        new_side = int(max(w, h) * 4)
        new_img = PIL.Image.new("RGBA", (new_side, new_side), (0, 0, 0, 0))
        paste_x = (new_side - w) // 2
        paste_y = (new_side - h) // 2
        new_img.paste(img, (paste_x, paste_y), mask=img)
        return new_img


class ClockFaceAnimation():
    def __init__(self, canvas, big_arrow_source, small_arrow_source, big_arrow_item, small_arrow_item):
        self.canvas = canvas
        self.big_arrow_source = big_arrow_source
        self.small_arrow_source = small_arrow_source
        self.big_arrow_item = big_arrow_item
        self.small_arrow_item = small_arrow_item

        # refs
        self.big_arrow_tk = PIL.ImageTk.PhotoImage(self.big_arrow_source)
        self.small_arrow_tk = PIL.ImageTk.PhotoImage(self.small_arrow_source)
        self.canvas.itemconfig(self.big_arrow_item, image=self.big_arrow_tk)
        self.canvas.itemconfig(self.small_arrow_item, image=self.small_arrow_tk)

        self._running = False

    def start(self):
        self._running = True
        self.update()

    def stop(self):
        self._running = False

    def update(self):
        current_time = time.localtime()
        hours = current_time.tm_hour % 12
        minutes = current_time.tm_min

        small_arrow_angle = (30 * hours) - 45
        big_arrow_angle = (6 * minutes) - 45

        rotated_big = self.big_arrow_source.rotate(
            -big_arrow_angle,
            resample=PIL.Image.Resampling.BICUBIC
        )
        rotated_small = self.small_arrow_source.rotate(
            -small_arrow_angle,
            resample=PIL.Image.Resampling.BICUBIC
        )

        self.big_arrow_tk = PIL.ImageTk.PhotoImage(rotated_big)
        self.small_arrow_tk = PIL.ImageTk.PhotoImage(rotated_small)

        self.canvas.itemconfig(self.big_arrow_item, image=self.big_arrow_tk)
        self.canvas.itemconfig(self.small_arrow_item, image=self.small_arrow_tk)

        if self._running:
            self.canvas.after(1000, self.update)


class OtherAnimations():
    def __init__(self, canvas, eyes_item, eyes_image_source, tail_item, tail_image_source_center_pivot, base_center):
        self.canvas = canvas

        self.eyes_item = eyes_item
        self.tail_item = tail_item

        self.eyes_src = eyes_image_source
        self.tail_src_center = tail_image_source_center_pivot

        self.center_x, self.center_y = base_center

        self._running = False
        self._start_epoch = time.time()

        # Eyes
        self.eyes_movex = 8 
        self.eyes_timer = .75

        # Tail rotation config
        self.tail_angle = 10
        self.tail_timer = .75 

        # Cache current tk images to keep references
        self._eyes_tk = PIL.ImageTk.PhotoImage(self.eyes_src)
        self.canvas.itemconfig(self.eyes_item, image=self._eyes_tk)
        self._tail_tk = PIL.ImageTk.PhotoImage(self.tail_src_center)
        self.canvas.itemconfig(self.tail_item, image=self._tail_tk)

    def start(self):
        self._running = True
        self.update()

    def stop(self):
        self._running = False

    def update(self):
        t = time.time() - self._start_epoch

        # Movement math
        eyes_x = self.eyes_movex * math.sin(2 * math.pi * self.eyes_timer * t)
        self.canvas.coords(self.eyes_item, self.center_x + eyes_x, self.center_y)

        tail_angle = self.tail_angle * math.sin(-2 * math.pi * self.tail_timer * t)
        rotated_tail = self.tail_src_center.rotate(-tail_angle, resample=PIL.Image.Resampling.NEAREST, expand=True)
        self._tail_tk = PIL.ImageTk.PhotoImage(rotated_tail)
        self.canvas.itemconfig(self.tail_item, image=self._tail_tk)

        if self._running:
            # Update time, smoothness
            self.canvas.after(20, self.update)


class DialougeChoices():
    def __init__(self):
        pass

def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())

def main():
    ClockImageImport()

if __name__ == "__main__":
    main()