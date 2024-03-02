# from tkinter import Frame, Label, Entry, Tk
from tkinter import *
from sqlalchemy import Table, MetaData, Column
from sqlalchemy.sql import select
from models import KeyKeeper
from tkmacosx import Button
import authentication as auth
from db import get_db
import asyncio
from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import select



BACKGROUND_COLOR = '#0d1b2a'
SECONDARY_COLOR = '#1b263b'
THIRD_COLOR = '#415a77'
FOURTH_COLOR = '#778da9'
TEXT_COLOR = '#e0e1dd'
MAIN_COLOR = '#3a86ff'


FAIL_COLOR = '#fee2e2'

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

class HomePage(BaseModel):
    def __init__(self, screen: Tk):
        super().__init__(screen)
        self.create_login_form()
        self.id = 1

    def create_login_form(self):
        self.login_frame = Frame(self.screen, background=BACKGROUND_COLOR)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username_label = Label(self.login_frame, text="USERNAME", fg=TEXT_COLOR, font=('Lato', 16, 'bold'), background=BACKGROUND_COLOR)
        self.username_entry = Entry(self.login_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
                                    highlightthickness=0, borderwidth=0, bd=0,
                                    width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat')

        self.password_label = Label(self.login_frame, text="PASSWORD", fg=TEXT_COLOR, font=('Lato', 16, 'bold'), background=BACKGROUND_COLOR)
        self.password_entry = Entry(self.login_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
                                    highlightthickness=0, borderwidth=0, bd=0,
                                    width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat', show='*')
        
        self.login_btn = Button(self.login_frame, padx=16, pady=4, text="LOGIN", bg=MAIN_COLOR, border=0, fg=TEXT_COLOR,
                                highlightthickness=0, borderwidth=0, bd=0,highlightbackground=BACKGROUND_COLOR,
                                borderless=True, command=self.login)
       
        self.register_btn = Button(self.login_frame, text="Not registered? Signup here!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9),
                                   borderless=True, command=self.open_register_page)

        self.username_label.grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.username_entry.grid(row=1, column=0, padx=8, pady=4, sticky="e")

        self.password_label.grid(row=2, column=0, padx=8, pady=4, sticky="w")
        self.password_entry.grid(row=3, column=0, padx=8, pady=4, sticky="e")

        self.login_btn.grid(row=4, column=0, padx=8, pady=4, sticky="w")
        self.register_btn.grid(row=5, column=0, padx=8, pady=4, sticky="w")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = next(get_db())
        authenticated_user = auth.authenticate_user(username=username, password=password,db=db)

        if authenticated_user:
            print("Login successful")
            self.show_success_frame()
            self.navigate_to_vault(authenticated_user.id, authenticated_user.hashed_password, db=db)
        else:
            print("Login failed")
            self.show_error_frame()

    def open_register_page(self):
        self.clear_page()
        register_page = RegisterPage(self.screen)

    def navigate_to_vault(self, user_id: int, hashed_password: str,db: Session):
        self.clear_page()
        vault_page = VaultPage(self.screen, user_id=user_id, user_password=hashed_password, db=db)

    def show_success_frame(self):
        # Create a success message frame
        success_frame = Frame(self.screen, background="green")
        success_label = Label(success_frame, text="Login successful!", fg='#134e4a', bg='#ccfbf1', font=('Lato', 16), padx=16, pady=16,
                              highlightthickness=1, borderwidth=1, bd=1, highlightcolor='#10b981')
        success_label.pack()
        success_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Schedule the frame to be destroyed after 3 seconds
        self.screen.after(3000, success_frame.destroy)

    def show_error_frame(self):
        error_frame = Frame(self.screen)
        error_label = Label(error_frame, text="Wrong username or password!", fg="#b91c1c", bg=FAIL_COLOR, font=('Lato', 16), padx=16, pady=16,
                            highlightthickness=2, borderwidth=2, bd=2, highlightcolor='#ef4444', highlightbackground='#ef4444')
        error_label.pack()
        error_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.screen.after(3000, error_frame.destroy)


class RegisterPage(BaseModel):
    def __init__(self, screen: Tk):
        super().__init__(screen)
        self.create_register_form()
        self.id = 2

    def create_register_form(self):
        self.register_frame = Frame(self.screen, background=BACKGROUND_COLOR)
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username_label = Label(self.register_frame, text="USERNAME", fg=TEXT_COLOR, font=('Lato', 16, 'bold'), background=BACKGROUND_COLOR)
        self.username_entry = Entry(self.register_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
                                    highlightthickness=0, borderwidth=0, bd=0,
                                    width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat')

        self.password_label = Label(self.register_frame, text="PASSWORD", fg=TEXT_COLOR, font=('Lato', 16, 'bold'), background=BACKGROUND_COLOR)
        self.password_entry = Entry(self.register_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
                                    highlightthickness=0, borderwidth=0, bd=0,
                                    width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat', show='*')
        self.password_repeat_label = Label(self.register_frame, text="PASSWORD", fg=TEXT_COLOR, font=('Lato', 16, 'bold'), background=BACKGROUND_COLOR)
        self.password_repeat_entry = Entry(self.register_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
                                    highlightthickness=0, borderwidth=0, bd=0,
                                    width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat', show='*')
        
        self.login_btn = Button(self.register_frame, padx=16, pady=4, text="REGISTER", bg=MAIN_COLOR, border=0, fg=TEXT_COLOR,
                                highlightthickness=0, borderwidth=0, bd=0,highlightbackground=BACKGROUND_COLOR,
                                borderless=True, command=self.register)
       
        self.go_back_btn = Button(self.register_frame, text="Go back!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 16),
                                   borderless=True, command=self.open_home_page)

        self.username_label.grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.username_entry.grid(row=1, column=0, padx=8, pady=4, sticky="e")

        self.password_label.grid(row=2, column=0, padx=8, pady=4, sticky="w")
        self.password_entry.grid(row=3, column=0, padx=8, pady=4, sticky="e")


        self.password_repeat_label.grid(row=4, column=0, padx=8, pady=4, sticky="w")
        self.password_repeat_entry.grid(row=5, column=0, padx=8, pady=4, sticky="e")

        self.login_btn.grid(row=6, column=0, padx=8, pady=4, sticky="w")
        self.go_back_btn.grid(row=6, column=1, padx=8, pady=4, sticky="w")

    def open_home_page(self):
        self.clear_page()
        self.register_frame.destroy()
        home_page = HomePage(self.screen)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_repeat = self.password_repeat_entry.get()

        db = next(get_db())
        registration_result = auth.register_user(username, password, password_repeat, db)

        if registration_result is True:
            self.show_success_frame()
        else:
            self.show_error_frame(registration_result)

    def show_success_frame(self):
        # Create a success message frame
        self.open_home_page()
        success_frame = Frame(self.screen, background="green")
        success_label = Label(success_frame, text="Registration successful!", fg='#134e4a', bg='#ccfbf1', font=('Lato', 16), padx=16, pady=16,
                              highlightthickness=1, borderwidth=1, bd=1, highlightcolor='#10b981')
        success_label.pack()
        success_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.screen.after(3000, success_frame.destroy)

    def show_error_frame(self, error_message: str):
        error_frame = Frame(self.screen)
        error_label = Label(error_frame, text=error_message, fg="#b91c1c", bg=FAIL_COLOR, font=('Lato', 16), padx=16, pady=16,
                            highlightthickness=2, borderwidth=2, bd=2, highlightcolor='#ef4444', highlightbackground='#ef4444')
        error_label.pack()
        error_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Schedule the frame to be destroyed after 3 seconds
        self.screen.after(3000, error_frame.destroy)

# from tkinter import ttk
# from sqlalchemy.orm import Session
# from sqlalchemy import Table, MetaData, Column
# from sqlalchemy.sql import select
# from models import KeyKeeper
# class VaultPage(BaseModel):
#     def __init__(self, screen: Tk, user_id: int, db: Session):
#         super().__init__(screen)
#         self.user_id = user_id
#         self.db = db
#         self.create_vault_page()
#         self.id = 3

#     def create_vault_page(self):
#         self.tree = ttk.Treeview(self.screen)
#         self.tree.pack(expand=True, fill="both")
        
#         # Generate table data
#         self.generate_table()

#         # Button to add new data
#         add_button = Button(self.screen, text="Add Data", command=self.add_data)
#         add_button.pack()

#     def generate_table(self):
#         # Define columns for the table
#         columns = ("ID", "Hashed Keys", "Hashed Password")

#         # Configure existing Treeview widget
#         self.tree["columns"] = columns
#         self.tree["show"] = "headings"
        
#         # Define column headings
#         for col in columns:
#             self.tree.heading(col, text=col)

#         # Retrieve key keepers data from the database
#         key_keepers = self.db.query(KeyKeeper).all()

#         # Populate the table with key keepers data
#         for key_keeper in key_keepers:
#             self.tree.insert("", "end", values=(key_keeper.id, key_keeper.hashed_keys, key_keeper.hashed_password))

#     def add_data(self):
#         # Create a new window for adding data
#         add_window = Tk()
#         add_window.title("Add Data")

#         # Labels and entry fields for input
#         Label(add_window, text="Hashed Keys:").grid(row=0, column=0)
#         hashed_keys_entry = Entry(add_window)
#         hashed_keys_entry.grid(row=0, column=1)

#         Label(add_window, text="Hashed Password:").grid(row=1, column=0)
#         hashed_password_entry = Entry(add_window)
#         hashed_password_entry.grid(row=1, column=1)

#         # Button to save data
#         save_button = Button(add_window, text="Save", command=lambda: self.save_data(hashed_keys_entry.get(), hashed_password_entry.get(), add_window))
#         save_button.grid(row=2, column=0, columnspan=2)

#     def save_data(self, hashed_keys, hashed_password, add_window):
#         # Create a new KeyKeeper instance and add it to the database
#         new_key_keeper = KeyKeeper(hashed_keys=hashed_keys, hashed_password=hashed_password, user_id=self.user_id)
#         self.db.add(new_key_keeper)
#         self.db.commit()

#         # Update the table to reflect the changes
#         self.generate_table()

#         # Close the add data window
#         add_window.destroy()



class VaultPage(BaseModel):
    def __init__(self, screen: Tk, user_id: int, user_password: str, db: Session):
        super().__init__(screen)
        self.user_id = user_id
        self.user_password = user_password
        self.db = db
        self.key, _ = auth.generate_fernet_key(user_password)  # Generate Fernet key based on user password
        self.create_vault_page()
        self.id = 3

    def create_vault_page(self):
        self.tree = ttk.Treeview(self.screen)
        self.tree.pack(expand=True, fill="both")
        
        # Generate table data
        self.generate_table()

        # Button to add new data
        add_button = Button(self.screen, text="Add Data", command=self.add_data)
        add_button.pack()

    def generate_table(self):
        # Define columns for the table
        columns = ("ID", "Hashed Keys", "Hashed Password")

        # Configure existing Treeview widget
        self.tree["columns"] = columns
        self.tree["show"] = "headings"
        
        # Define column headings
        for col in columns:
            self.tree.heading(col, text=col)

        # Retrieve key keepers data from the database
        key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

        # Populate the table with key keepers data
        for key_keeper in key_keepers:
            decrypted_keys = auth.decrypt_data(key_keeper.hashed_keys, self.key)  # Decrypt using Fernet key
            decrypted_password = auth.decrypt_data(key_keeper.hashed_password, self.key)  # Decrypt using Fernet key
            self.tree.insert("", "end", values=(key_keeper.id, decrypted_keys, decrypted_password))

    def add_data(self):
        # Create a new window for adding data
        add_window = Tk()
        add_window.title("Add Data")

        # Labels and entry fields for input
        Label(add_window, text="Hashed Keys:").grid(row=0, column=0)
        hashed_keys_entry = Entry(add_window)
        hashed_keys_entry.grid(row=0, column=1)

        Label(add_window, text="Hashed Password:").grid(row=1, column=0)
        hashed_password_entry = Entry(add_window)
        hashed_password_entry.grid(row=1, column=1)

        # Button to save data
        save_button = Button(add_window, text="Save", command=lambda: self.save_data(hashed_keys_entry.get(), hashed_password_entry.get(), add_window))
        save_button.grid(row=2, column=0, columnspan=2)

    def save_data(self, hashed_keys, hashed_password, add_window):
        # Encrypt the data using the Fernet key
        encrypted_keys = auth.encrypt_data(hashed_keys, self.key)
        encrypted_password = auth.encrypt_data(hashed_password, self.key)

        # Create a new KeyKeeper instance and add it to the database
        new_key_keeper = KeyKeeper(hashed_keys=encrypted_keys, hashed_password=encrypted_password, user_id=self.user_id)
        self.db.add(new_key_keeper)
        self.db.commit()

        # Update the table to reflect the changes
        self.generate_table()

        # Close the add data window
        add_window.destroy()





