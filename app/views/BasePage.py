from tkinter import *


class BaseModel(Frame):
    def __init__(self, screen: Tk):
        super().__init__(screen)
        self.screen = screen
        self.screen.resizable(False, False)

    def clear_page(self):
        for widget in self.winfo_children():
            widget.destroy()

    def switch_frame(self, frame_id: int):
        for frame_class, frame in self.master.frames.items():
            if frame.id == frame_id:
                frame.tkraise()
                break