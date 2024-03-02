from tkinter import Tk
from pages import HomePage, RegisterPage
from db import engine
from models import Base


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title('Key Keep | Save your passwords secretly!')
        self.geometry('600x360')
        self.resizable(0, 0)
        self.configure(background='#0d1b2a')

    #     self.frames = {}  # Dictionary to hold instances of all frames

    #     # Create instances of all frames and store them in the dictionary
    #     for FrameClass in (HomePage, RegisterPage):
    #         frame_instance = FrameClass(self)
    #         self.frames[FrameClass] = frame_instance
    #         frame_instance.grid(row=0, column=0, sticky="nsew")
    #         print('somewhere here is happening')
    #     # Show the home page by default
    #     self.show_frame(HomePage)

    # def show_frame(self, frame_class):
    #     # Raise the requested frame
    #     frame_instance = self.frames[frame_class]
    #     frame_instance.tkraise()

if __name__ == "__main__":
    app = App()
    Base.metadata.create_all(bind=engine)
    home_page = HomePage(app)
    app.mainloop()
