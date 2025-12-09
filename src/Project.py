import tkinter as tk
import time
import PIL, PIL.Image, PIL.ImageTk
import os
import math

class ClockImageImport(): 

    def __init__(self):
        base = os.path.dirname(os.path.abspath(__file__))
        
        clock_img_path = os.path.join(base, "..", "Imports", "CitKatClock.png")
        big_clock_img_path = os.path.join(base, "..", "Imports", "BigClock.png")
        eyes_img_path = os.path.join(base, "..", "Imports", "Eyes.png")
        tail_img_path = os.path.join(base, "..", "Imports", "Tail.png")
        nose_img_path = os.path.join(base, "..", "Imports", "Nose.png")
        bowtie_img_path = os.path.join(base, "..", "Imports", "Bowtie.png")
        
        exit_button_img_path = os.path.join(base, "..", "Imports", "ExitButton.png")
        move_button_img_path = os.path.join(base, "..", "Imports", "MoveButton.png")

        big_arrow_img_path = os.path.join(base, "..", "Imports", "BigArrow.png")
        small_arrow_img_path = os.path.join(base, "..", "Imports", "SmallArrow.png")
        big_big_arrow_img_path = os.path.join(base, "..", "Imports", "BigBigArrow.png")
        big_small_arrow_img_path = os.path.join(base, "..", "Imports", "BigSmallArrow.png")

        speech_bubble_img_path = os.path.join(base, "..", "Imports", "SpeechBubble.png")
        speech_bubble_purple_img_path = os.path.join(base, "..", "Imports", "SpeechBubblePurple.png")

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
        big_clock = PIL.Image.open(big_clock_img_path)
        eyes = PIL.Image.open(eyes_img_path)
        tail = PIL.Image.open(tail_img_path)
        nose = PIL.Image.open(nose_img_path)
        bowtie = PIL.Image.open(bowtie_img_path)
        big_arrow = PIL.Image.open(big_arrow_img_path)
        small_arrow = PIL.Image.open(small_arrow_img_path)
        big_big_arrow = PIL.Image.open(big_big_arrow_img_path)
        big_small_arrow = PIL.Image.open(big_small_arrow_img_path)
        speech_bubble = PIL.Image.open(speech_bubble_img_path)
        speech_bubble_purple = PIL.Image.open(speech_bubble_purple_img_path)

        scale_amount = 3

        small_cat = small_cat.resize((small_cat.width * scale_amount, small_cat.height * scale_amount),
                                      PIL.Image.Resampling.NEAREST)
        big_clock = big_clock.resize((big_clock.width * scale_amount, big_clock.height * scale_amount), 
                                     PIL.Image.Resampling.NEAREST)
        eyes = eyes.resize((eyes.width * scale_amount, eyes.height * scale_amount), PIL.Image.Resampling.
                           NEAREST)
        tail = tail.resize((tail.width * scale_amount, tail.height * scale_amount), PIL.Image.Resampling.
                           NEAREST)
        nose = nose.resize((nose.width * scale_amount, nose.height * scale_amount), PIL.Image.Resampling.
                           NEAREST)
        bowtie = bowtie.resize((bowtie.width * scale_amount, bowtie.height * scale_amount), PIL.Image.
                               Resampling.NEAREST)
        big_arrow = big_arrow.resize((big_arrow.width * scale_amount, big_arrow.height * scale_amount), 
                                     PIL.Image.Resampling.NEAREST)
        small_arrow = small_arrow.resize((small_arrow.width * scale_amount, small_arrow.height * scale_amount), 
                                         PIL.Image.Resampling.NEAREST)
        big_big_arrow = big_big_arrow.resize((big_big_arrow.width * scale_amount, big_big_arrow.height *
                                               scale_amount), PIL.Image.Resampling.NEAREST)
        big_small_arrow = big_small_arrow.resize((big_small_arrow.width * scale_amount, big_small_arrow.height
                                                   * scale_amount), PIL.Image.Resampling.NEAREST)
        speech_bubble = speech_bubble.resize((speech_bubble.width * scale_amount, speech_bubble.height * scale_amount), 
                                             PIL.Image.Resampling.NEAREST)
        speech_bubble_purple = speech_bubble_purple.resize((speech_bubble_purple.width * scale_amount, speech_bubble_purple.height
                                                             * scale_amount), PIL.Image.Resampling.NEAREST)

        # Create transparent spacer image for speech bubble alignment
        spacer_image = PIL.Image.new("RGBA", (speech_bubble.width, speech_bubble.height), (0, 0, 0, 0))
        self.spacer_image = PIL.ImageTk.PhotoImage(spacer_image)

        self.spacer_label = tk.Label(root, image=self.spacer_image, bg='magenta')
        self.spacer_label.grid(column=0, row=1, sticky='nw', padx=20)

        self.spacer_label.grid()
        
        
        big_arrow_source = self.make_pivot_image(big_arrow)
        small_arrow_source = self.make_pivot_image(small_arrow)
        big_big_arrow_source = self.make_pivot_image(big_big_arrow)
        big_small_arrow_source = self.make_pivot_image(big_small_arrow)

        tail_source_center_pivot = self.make_center_pivot_image(tail)
        nose_source_center_pivot = self.make_center_pivot_image(nose)
        bowtie_source_center_pivot = self.make_center_pivot_image(bowtie)
        

        self.nose_src = nose_source_center_pivot
        self.bowtie_src = bowtie_source_center_pivot

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
        
        bowtie_tk = PIL.ImageTk.PhotoImage(self.bowtie_src)
        bowtie_item = canvas.create_image(center_x, center_y, anchor=tk.CENTER)
        canvas.itemconfig(bowtie_item, image=bowtie_tk)

        # refs
        self.nose_item = nose_item
        self.bowtie_item = bowtie_item

        self.canvas = canvas
        canvas.bind("<Button-1>", self.on_canvas_click)

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
        
        # Initialize DialogueChoices
        self.dialogue_choices = DialogueChoices(root)

        # Keep references for big clock and arrows
        self.big_clock_tk = PIL.ImageTk.PhotoImage(big_clock)
        self.big_big_arrow_source = big_big_arrow_source
        self.big_small_arrow_source = big_small_arrow_source

        # Create big clock and arrows (hidden initially)
        self.big_clock_item = canvas.create_image(clock_center_x, clock_center_y, anchor=tk.CENTER)
        self.big_big_arrow_item = canvas.create_image(clock_center_x, clock_center_y, anchor=tk.CENTER)
        self.big_small_arrow_item = canvas.create_image(clock_center_x, clock_center_y, anchor=tk.CENTER)

        # Hide big clock and arrows initially
        canvas.itemconfig(self.big_clock_item, state="hidden")
        canvas.itemconfig(self.big_big_arrow_item, state="hidden")
        canvas.itemconfig(self.big_small_arrow_item, state="hidden")

        # Track external big clock window/animation
        self.big_clock_window = None
        self.big_clock_animation = None

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

    def on_canvas_click(self, event):
        if self._pointer_over_bowtie_sprite(event):
            self.on_bowtie_click(event)
        elif self._pointer_over_nose_sprite(event):
            self.on_nose_click(event)

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

    def _pointer_over_bowtie_sprite(self, event):
        img_coords = self.canvas.coords(self.bowtie_item)
        if not img_coords:
            return False

        img_x, img_y = img_coords[0], img_coords[1]
        dx = event.x - img_x
        dy = event.y - img_y

        px = int(dx + self.bowtie_src.width / 2)
        py = int(dy + self.bowtie_src.height / 2)

        if 0 <= px < self.bowtie_src.width and 0 <= py < self.bowtie_src.height:
            pixel = self.bowtie_src.getpixel((px, py))
            return pixel[3] > 0 if len(pixel) == 4 else any(pixel)
        return False

    def on_nose_click(self, event):
        # Only toggle when the clicked pixel is on the nose sprite
        if not self._pointer_over_nose_sprite(event):
            return

        if self.dialogue_choices.speech_bubble_visible:
            self.dialogue_choices.hide_speech_bubbles()
        else:
            self.dialogue_choices.show_speech_bubbles()
            
            if self.dialogue_choices.date_label.cget("text") == "Return":
                self.dialogue_choices.reset_ui()

        self.dialogue_choices.speech_bubble_visible = not self.dialogue_choices.speech_bubble_visible
        
    def on_bowtie_click(self, event):
        if not self._pointer_over_bowtie_sprite(event):
            return

        if self.big_clock_window is not None and self.big_clock_window.winfo_exists():
            self.big_clock_window.lift()
            self.big_clock_window.focus_force()
            return

        # Get the dimensions of the main window
        main_window_x = self.root.winfo_x()
        main_window_y = self.root.winfo_y()
        main_window_width = self.root.winfo_width()
        main_window_height = self.root.winfo_height()

        # Calculate the position to center the new window
        big_clock_width = self.big_clock_tk.width()
        big_clock_height = self.big_clock_tk.height()
        new_window_x = main_window_x + (main_window_width - big_clock_width) // 2
        new_window_y = main_window_y + (main_window_height - big_clock_height) // 2

        # Create a new window for the big clock
        big_clock_window = tk.Toplevel(self.root)
        big_clock_window.title("Big Clock")
        big_clock_window.attributes("-topmost", True)
        big_clock_window.geometry(f"{big_clock_width}x{big_clock_height}+{new_window_x}+{new_window_y}")
        big_clock_window.configure(bg='magenta')
        big_clock_window.overrideredirect(True)
        big_clock_window.wm_attributes('-transparentcolor', 'magenta')

        # Create a new canvas for the big clock
        big_canvas = tk.Canvas(
            big_clock_window,
            width=big_clock_width,
            height=big_clock_height,
            bg='magenta',
            highlightthickness=0
        )
        big_canvas.pack()

        # Add the big clock to the new canvas
        big_clock_item = big_canvas.create_image(0, 0, anchor=tk.NW, image=self.big_clock_tk)

        # Add the big arrows to the new canvas
        big_big_arrow_item = big_canvas.create_image(big_clock_width // 2, big_clock_height // 2, anchor=tk.CENTER)
        big_small_arrow_item = big_canvas.create_image(big_clock_width // 2, big_clock_height // 2, anchor=tk.CENTER)

        # Initialize and start the big clock animation
        big_clock_animation = ClockFaceAnimation(
            canvas=big_canvas,
            big_arrow_source=self.big_big_arrow_source,
            small_arrow_source=self.big_small_arrow_source,
            big_arrow_item=big_big_arrow_item,
            small_arrow_item=big_small_arrow_item
        )
        big_clock_animation.start()

        # Remember window and animation so we know one is open
        self.big_clock_window = big_clock_window
        self.big_clock_animation = big_clock_animation

        # Add "Move" and "Close" buttons
        move_button = tk.Label(big_clock_window, image=self.move_button_image, bg='magenta')
        close_button = tk.Label(big_clock_window, image=self.exit_button_image, bg='magenta')

        move_button.place(x=big_clock_width - 64, y=0)  # Adjust position for "Move" button
        close_button.place(x=big_clock_width - 32, y=0)  # Adjust position for "Close" button

        # Bind move and close functionality
        move_button.bind("<Button-1>", lambda event: self.start_move_big_clock(event, big_clock_window))
        move_button.bind("<B1-Motion>", lambda event: self.on_move_big_clock(event, big_clock_window))
        close_button.bind("<Button-1>", lambda event: self.close_big_clock(big_clock_window, big_clock_animation))

    def start_move_big_clock(self, event, window):
        self._drag_offset_x = event.x_root - window.winfo_rootx()
        self._drag_offset_y = event.y_root - window.winfo_rooty()

    def on_move_big_clock(self, event, window):
        x = event.x_root - self._drag_offset_x
        y = event.y_root - self._drag_offset_y
        window.geometry(f"+{x}+{y}")
        
    def close_big_clock(self, window, animation):
        animation.stop()  # Stop the animation
        window.destroy()  # Destroy the Toplevel window

        # Clear tracking if this was the tracked window
        if self.big_clock_window is window:
            self.big_clock_window = None
            self.big_clock_animation = None

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


class DialogueChoices():
    def __init__(self, root):
        self.root = root
        self.speech_bubble_visible = False

        # Define scale amount for resizing
        scale_amount = 3

        # Load and resize speech bubble images
        speech_bubble_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                           "..", "Imports", "SpeechBubble.png")
        speech_bubble_purple_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 
                                                 "..", "Imports", "SpeechBubblePurple.png")

        speech_bubble = PIL.Image.open(speech_bubble_path)
        speech_bubble_purple = PIL.Image.open(speech_bubble_purple_path)

        speech_bubble = speech_bubble.resize((speech_bubble.width * scale_amount, speech_bubble.height * 
                                              scale_amount), PIL.Image.Resampling.NEAREST)
        speech_bubble_purple = speech_bubble_purple.resize((speech_bubble_purple.width * scale_amount, speech_bubble_purple.height
                                                             * scale_amount), PIL.Image.Resampling.NEAREST)

        self.speech_bubble_image = PIL.ImageTk.PhotoImage(speech_bubble)
        self.speech_bubble_image_2 = PIL.ImageTk.PhotoImage(speech_bubble_purple)
        self.speech_bubble_image_3 = PIL.ImageTk.PhotoImage(speech_bubble_purple)

        # Create speech bubble labels
        self.speech_bubble_label = tk.Label(root, image=self.speech_bubble_image, bg='magenta')
        self.speech_bubble_label_2 = tk.Label(root, image=self.speech_bubble_image_2, bg='magenta')
        self.speech_bubble_label_3 = tk.Label(root, image=self.speech_bubble_image_3, bg='magenta')

        # Add labels for text on top of each speech bubble
        self.text_label = tk.Label(root, text="Hello Everynyan!", font=("Bahnschrift", 18), bg='white', fg='black')
        self.date_label = tk.Label(root, text="Date", font=("Bahnschrift", 18), bg='#cb75f4', fg='black')
        self.time_label = tk.Label(root, text="Time", font=("Bahnschrift", 18), bg='#cb75f4', fg='black')

        # Initially hide all speech bubbles
        self.hide_speech_bubbles()

        # Bind click events
        self.speech_bubble_label_2.bind("<Button-1>", self.on_speech_bubble_2_click)
        self.speech_bubble_label_3.bind("<Button-1>", self.on_speech_bubble_3_click)

    def show_speech_bubbles(self):
        self.speech_bubble_label.place(x=30, y=35)
        self.speech_bubble_label_2.place(x=30, y=105)
        self.speech_bubble_label_3.place(x=30, y=175)

        self.text_label.place(x=40, y=40)
        self.date_label.place(x=40, y=110)
        self.time_label.place(x=40, y=180)

    def hide_speech_bubbles(self):
        self.speech_bubble_label.place_forget()
        self.speech_bubble_label_2.place_forget()
        self.speech_bubble_label_3.place_forget()
        self.text_label.place_forget()
        self.date_label.place_forget()
        self.time_label.place_forget()

    def reset_ui(self):
        self.show_speech_bubbles()
        self.update_speech_bubble_text(self.text_label, "Hello Everynyan!")
        self.update_speech_bubble_text(self.date_label, "Date")
        self.update_speech_bubble_text(self.time_label, "Time")
        self.speech_bubble_label_2.bind("<Button-1>", self.on_speech_bubble_2_click)

    def update_speech_bubble_text(self, label, text):
        label.config(text=text)

    def on_speech_bubble_2_click(self, event):
        self.update_speech_bubble_text(self.text_label, time.strftime("It's %D"))
        self.speech_bubble_label_3.place_forget()
        self.time_label.place_forget()
        self.update_speech_bubble_text(self.date_label, "Return")
        self.speech_bubble_label_2.bind("<Button-1>", self.on_return_click)

    def on_speech_bubble_3_click(self, event):
        self.update_speech_bubble_text(self.text_label, "It's " + get_time())
        self.speech_bubble_label_3.place_forget()
        self.time_label.place_forget()
        self.update_speech_bubble_text(self.date_label, "Return")
        self.speech_bubble_label_2.bind("<Button-1>", self.on_return_click)

    def on_return_click(self, event):
        self.reset_ui()

def get_time():
    return time.strftime("%I:%M:%S %p", time.localtime())

def main():
    ClockImageImport()

if __name__ == "__main__":
    main()