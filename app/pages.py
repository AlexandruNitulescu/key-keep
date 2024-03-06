from tkinter import *
from tkinter import messagebox
from sqlalchemy import Table, MetaData, Column
from sqlalchemy.sql import select
from models import KeyKeeper
#from tkmacosx import Button
import authentication as auth
from db import get_db
import asyncio
from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import select
import pyperclip  # For copying to clipboard
import csv
from customtkinter import *
import settings
from authentication import generate_secret_key, generate_static_key, encrypt_data, decrypt_data



BACKGROUND_COLOR = '#09090b'
FRAME_COLOR = '#18181b'
ENTRY_COLOR = '#3f3f46'
LIGHTER_COLOR = '#27272a'


SECONDARY_COLOR = '#1b263b'
THIRD_COLOR = '#415a77'
FOURTH_COLOR = '#778da9'
TEXT_COLOR = '#f4f4f5'
MAIN_COLOR = '#3a86ff'
BASE_COLOR = '#1d4ed8'
DARK_COLOR = '#121212'
HOVER_COLOR = '#1e3a8a'

FAIL_BG_COLOR = '#fee2e2'
FAIL_BORDER_COLOR = '#f87171'
FAIL_TEXT_COLOR = '#b91c1c'

SUCCESS_BG_COLOR = '#ccfbf1'
SUCCESS_BORDER_COLOR = '#14b8a6'

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
        self.login_frame = Frame(self.screen, background=FRAME_COLOR, padx=32, pady=32,)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title = Label(self.login_frame, text="Log In", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 24, 'bold'), )

        self.username_label = Label(self.login_frame, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), )
        self.username_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                            font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)

        self.password_label= Label(self.login_frame, text="Password", fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), background=FRAME_COLOR)
        self.password_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), show='*', fg_color=ENTRY_COLOR)

        self.login_btn = CTkButton(master=self.login_frame, text='Sign In', font=('yu gothic ui', 16, 'bold'), fg_color='#1d4ed8', hover_color= HOVER_COLOR, corner_radius=32,
                                    width=340, height=48,
                                    command=self.login)
        self.register_btn = CTkButton(master=self.login_frame, text='Register Now', font=('yu gothic ui', 16, 'bold'), fg_color=FRAME_COLOR, hover_color=ENTRY_COLOR, border_color=ENTRY_COLOR, border_width=2, corner_radius=32,
                                    width=340, height=48,
                                    command=self.open_register_page)

        # self.register_btn = Button(self.login_frame, text="Not registered? Signup here!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9),
        #                         #    borderless=True,
        #                            command=self.open_register_page)
        self.title.grid(row=0, column=0, padx=0, pady=32, sticky="w")
        self.username_label.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.username_entry.grid(row=2, column=0, padx=0, pady=8, sticky="w")

        self.password_label.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.password_entry.grid(row=4, column=0, padx=0, pady=8, sticky="w")

        self.login_btn.grid(row=5, column=0, padx=0, pady=8, sticky="w")
        self.register_btn.grid(row=6, column=0, padx=0, pady=8, sticky="w")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        db = next(get_db())
        authenticated_user = auth.authenticate_user(username=username, password=password, db=db)

        if authenticated_user:
            print("Login successful")
            self.show_success_frame()
            self.navigate_to_vault(authenticated_user.id, password=password, db=db)
        else:
            print("Login failed")
            self.show_error_frame()

    def open_register_page(self):
        self.clear_page()
        self.screen.after(0, self.login_frame.destroy)
        register_page = RegisterPage(self.screen)

    def navigate_to_vault(self, user_id: int, password, db: Session):
        self.clear_page()
        vault_page = VaultPage(self.screen, user_id=user_id, user_password=password, db=db)

    def show_success_frame(self):
        success_frame = Frame(self.screen, background="green")
        success_label = Label(success_frame, text="Login successful!", fg='#134e4a', bg='#ccfbf1', font=('Lato', 16), padx=16, pady=16,
                              highlightthickness=1, borderwidth=1, bd=1, highlightcolor='#10b981')
        success_label.pack()
        success_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.screen.after(3000, success_frame.destroy)

    def show_error_frame(self):
        error_frame = Frame(self.screen)
        error_label = Label(error_frame, text="Wrong username or password!", fg=FAIL_TEXT_COLOR, bg=FAIL_BG_COLOR, font=('yu gothic ui', 16, 'bold'), padx=16, pady=32,
                            highlightthickness=2, borderwidth=2, bd=2, highlightcolor=FAIL_BORDER_COLOR, highlightbackground=FAIL_BORDER_COLOR)
        error_label.pack()
        error_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.screen.after(3000, error_frame.destroy)


class RegisterPage(BaseModel):
    def __init__(self, screen: Tk):
        super().__init__(screen)
        self.create_register_form()
        self.id = 2

    def create_register_form(self):
        self.register_frame = Frame(self.screen, background=FRAME_COLOR, padx=32, pady=0)
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.title = Label(self.register_frame, text="Sign Up", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 24, 'bold'), )
        self.username_label = Label(self.register_frame, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), )

        # self.username_entry = Entry(self.register_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
        #                             highlightthickness=0, borderwidth=0, bd=0,
        #                             width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat')
        self.username_entry = CTkEntry(self.register_frame, border_width=0, width=340, height=40, corner_radius=2,
                            font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)

        self.password_label = Label(self.register_frame, text="Password", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'),)

        self.password_entry = CTkEntry(self.register_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), show='*', fg_color=ENTRY_COLOR)

        self.password_repeat_label = Label(self.register_frame, text="Repeat your password", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'),)

        # self.password_repeat_entry = Entry(self.register_frame, background=THIRD_COLOR, selectbackground=MAIN_COLOR,
        #                             highlightthickness=0, borderwidth=0, bd=0,
        #                             width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat', show='*')

        self.password_repeat_entry = CTkEntry(self.register_frame, border_width=0, width=340, height=40, corner_radius=2,
                            font=('yu gothic ui', 14), show='*', fg_color=ENTRY_COLOR)

        # self.login_btn = Button(self.register_frame, padx=16, pady=4, text="REGISTER", bg=MAIN_COLOR, border=0, fg=TEXT_COLOR,
        #                         highlightthickness=0, borderwidth=0, bd=0,highlightbackground=BACKGROUND_COLOR,
        #                         # borderless=True,
        #                         command=self.register)
        self.login_btn = CTkButton(master=self.register_frame, text='Sign Up', font=('yu gothic ui', 16, 'bold'), fg_color='#1d4ed8', hover_color= HOVER_COLOR, corner_radius=32,
                                    width=340, height=48,
                                    command=self.register)
        # self.go_back_btn = Button(self.register_frame, text="Go back!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 16),
        #                         #    borderless=True,
        #                            command=self.open_home_page)
        self.go_back_btn = CTkButton(master=self.register_frame, text='Go back', font=('yu gothic ui', 16, 'bold'), fg_color=FRAME_COLOR, hover_color=ENTRY_COLOR, border_color=ENTRY_COLOR, border_width=2, corner_radius=32,
                                    width=120, height=48,
                                    command=self.open_home_page)

        self.title.grid(row=0, column=0, padx=0, pady=48, sticky="w")
        self.username_label.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.username_entry.grid(row=2, column=0, padx=0, pady=8, sticky="e")

        self.password_label.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.password_entry.grid(row=4, column=0, padx=0, pady=8, sticky="e")


        self.password_repeat_label.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.password_repeat_entry.grid(row=6, column=0, padx=0, pady=8, sticky="e")

        self.login_btn.grid(row=7, column=0, padx=0, pady=48, sticky="w")
        self.go_back_btn.grid(row=0, column=2, padx=0, pady=0, sticky="w")

    def open_home_page(self):
        self.clear_page()
        self.register_frame.destroy()
        home_page = HomePage(self.screen)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        password_repeat = self.password_repeat_entry.get()

        db = next(get_db())

        success, result = auth.register_user(username, password, password_repeat, db)

        if success:
            self.show_success_frame(result)
        else:
            self.show_error_frame(result)


    def show_success_frame(self, secret_key):
        self.success_frame = Frame(self.screen, background=BACKGROUND_COLOR)
        self.success_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.success_label = Label(self.success_frame, text="Registration successful!", fg='#134e4a', bg='#ccfbf1',
                              font=('Lato', 16), padx=16, pady=16, highlightthickness=1, borderwidth=1,
                              bd=1, highlightcolor='#10b981')
        self.secret_key_label = Label(self.success_frame, text=f"{secret_key}", font=('Lato', 12), padx=16, pady=16)
        self.copy_button = Button(self.success_frame, text="Copy to Clipboard", command=self.copy_to_clipboard(secret_key))
        self.close_button = Button(self.success_frame, text="Close", command=self.destroy_and_close)

        self.success_label.grid(row=0, column=0, padx=8, pady=4, sticky="w")
        self.secret_key_label.grid(row=1, column=0, padx=8, pady=4, sticky="e")

        self.copy_button.grid(row=2, column=0, padx=8, pady=4, sticky="w")
        self.close_button.grid(row=3, column=0, padx=8, pady=4, sticky="e")

    # def show_success_frame(self, secret_key):
    #     self.success_frame = Frame(self.screen, background=BACKGROUND_COLOR)
    #     self.success_frame.place(relx=0.5, rely=0.5, anchor="center")

    #     self.success_label = Label(self.success_frame, text="Registration successful!", fg='#134e4a', bg='#ccfbf1',
    #                           font=('Lato', 16), padx=16, pady=16, highlightthickness=1, borderwidth=1,
    #                           bd=1, highlightcolor='#10b981')
    #     # self.close_button = Button(self.success_frame, text="Close", command=self.destroy_and_close)
    #     self.screen.after(3000, self.destroy_and_close)


    def show_error_frame(self, error_message: str):
        error_frame = Frame(self.screen)
        error_label = Label(error_frame, text=error_message, fg="#b91c1c", bg=FAIL_BG_COLOR, font=('Lato', 16), padx=16, pady=16,
                            highlightthickness=2, borderwidth=2, bd=2, highlightcolor='#ef4444', highlightbackground='#ef4444')
        error_label.pack()
        error_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.screen.after(3000, error_frame.destroy)

    def copy_to_clipboard(self, secret_key):
        pyperclip.copy(secret_key)

    def destroy_and_close(self):
        self.success_frame.destroy()
        self.register_frame.destroy()
        self.clear_page()
        home_page = HomePage(self.screen)


# class VaultPage(BaseModel):
#     def __init__(self, screen: Tk, user_id: int, user_password: str, db: Session):
#         super().__init__(screen)
#         self.user_id = user_id
#         self.user_password = user_password
#         self.db = db
#         self.static_key = auth.generate_static_key(user_password)
#         self.create_vault_page()
#         self.id = 3
#         self.generate_table()  # Generate table upon initialization

#     def copy_to_clipboard(self, secret_key):
#         pyperclip.copy(secret_key)

#     def create_vault_page(self):
#             self.table_frame = Frame(self.screen, background=FRAME_COLOR, padx=32, pady=32,)
#             self.table_frame.pack(expand=True, fill="both")

#             self.canvas = Canvas(self.table_frame, background=FRAME_COLOR,
#                                 highlightthickness=0, relief='ridge')
#             self.canvas.pack(side="left", fill="both", expand=True)

#             scrollbar = Scrollbar(self.table_frame, orient="vertical", command=self.canvas.yview)
#             scrollbar.pack(side="right", fill="y")
#             self.canvas.configure(yscrollcommand=scrollbar.set)

#             self.table_container = Frame(self.canvas, background=FRAME_COLOR)
#             self.canvas.create_window((0, 0), window=self.table_container, anchor="nw")

#             add_button = Button(self.table_frame, text="Add Data", command=self.add_data)
#             add_button.pack(side="top", pady=5)

#     def generate_table(self):
#         for widget in self.table_container.winfo_children():
#             widget.destroy()

#         columns = ("#", "WEBSITE", 'USERNAME', "PASSWORD", "ACTIONS")

#         for col_idx, col_name in enumerate(columns):
#             self.header = Label(self.table_container, text=col_name, background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 10, 'bold'))
#             if col_name == "ACTIONS":
#                 self.header.grid(row=0, column=col_idx, padx=8, pady=16, sticky='w', columnspan=3)  # Spanning across 3 columns for "ACTIONS"
#             else:
#                 self.header.grid(row=0, column=col_idx, padx=8, pady=16, sticky='w')

#         key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

#         rows = 1
#         for row_idx, key_keeper in enumerate(key_keepers, start=1):
#             decrypted_website = auth.decrypt_data(key_keeper.hashed_place, self.static_key)
#             decrypted_keys = auth.decrypt_data(key_keeper.hashed_name, self.static_key)  # Decrypt using Fernet key
#             decrypted_password = auth.decrypt_data(key_keeper.hashed_password, self.static_key)  # Decrypt using Fernet key

#             self.index = Label(self.table_container, text=str(row_idx)+'.', background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#             self.website = Label(self.table_container, text=decrypted_website, background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#             self.decrypted_keys = Label(self.table_container, text=decrypted_keys, background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#             self.decrypted_password = Label(self.table_container, text=decrypted_password, background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))

#             copy_button = CTkButton(self.table_container, width=32, text="Copy", font=('yu gothic ui', 12, 'bold'), fg_color=FRAME_COLOR, hover_color=ENTRY_COLOR, border_color=ENTRY_COLOR, border_width=2, corner_radius=32, command=self.copy_to_clipboard(decrypted_password))
#             edit_button = CTkButton(self.table_container, width=32, text="Edit", font=('yu gothic ui', 12, 'bold'), fg_color=FRAME_COLOR, hover_color=SUCCESS_BORDER_COLOR, border_color=SUCCESS_BORDER_COLOR, border_width=2, corner_radius=32, command=lambda key=key_keeper.id: self.edit_data(key))
#             delete_button = CTkButton(self.table_container, width=32, text="Delete", font=('yu gothic ui', 12, 'bold'), fg_color=FRAME_COLOR, hover_color=FAIL_BORDER_COLOR, border_color=FAIL_BORDER_COLOR, border_width=2, corner_radius=32, command=lambda key=key_keeper.id: self.delete_data(key))

#             self.index.grid(row=rows, column=0, padx=4, pady=4, sticky='w')
#             self.website.grid(row=rows, column=1, padx=4, pady=4, sticky='w')
#             self.decrypted_keys.grid(row=rows, column=2, padx=4, pady=4, sticky='w')
#             self.decrypted_password.grid(row=rows, column=3, padx=4, pady=4, sticky='w')

#             copy_button.grid(row=rows, column=4, padx=2, pady=2)
#             edit_button.grid(row=rows, column=5, padx=2, pady=2)
#             delete_button.grid(row=rows, column=6, padx=2, pady=2)

#             rows += 1

#         add_button = CTkButton(master=self.table_container, text='+', font=('yu gothic ui', 20, 'bold'), fg_color='#1d4ed8', hover_color=HOVER_COLOR, corner_radius=8, width=48, height=48, command=self.add_data)
#         add_button.grid(row=rows, column=0, columnspan=len(columns), pady=(20, 0))

#         backup_btn = Button(self.table_container, text="Backup your data", command=self.save_encrypted_data_to_csv)
#         backup_btn.grid(row=rows, column=2, columnspan=len(columns) - 2, pady=(20, 0))

#         self.canvas.update_idletasks()
#         self.canvas.config(scrollregion=self.canvas.bbox("all"))

#     def add_data(self):
#         add_window = Tk()
#         add_window.title("Add Data")
#         add_window.configure(background=FRAME_COLOR)  # Set background color

#         self.login_frame = Frame(add_window, background=FRAME_COLOR, padx=32, pady=32)
#         self.title = Label(self.login_frame, text="Add data to your database", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))

#         self.website_label = Label(self.login_frame, text="Website", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#         self.website_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)

#         self.username_label = Label(self.login_frame, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#         self.username_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)

#         self.password_label = Label(self.login_frame, text="Password", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
#         self.password_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)

#         save_button = CTkButton(master=self.login_frame, text='Save', font=('yu gothic ui', 16, 'bold'), fg_color='#1d4ed8', hover_color= HOVER_COLOR, corner_radius=32,
#                                     width=340, height=48,
#                                     command=lambda: self.save_data(self.website_entry.get(), self.username_entry.get(), self.password_entry.get(), add_window))

#         self.title.grid(row=0, column=0, padx=0, pady=32, sticky="w")
#         self.website_label.grid(row=1, column=0, padx=0, pady=0, sticky="w")
#         self.website_entry.grid(row=2, column=0, padx=0, pady=8, sticky="w")

#         self.username_label.grid(row=3, column=0, padx=0, pady=0, sticky="w")
#         self.username_entry.grid(row=4, column=0, padx=0, pady=8, sticky="w")

#         self.password_label.grid(row=5, column=0, padx=0, pady=0, sticky="w")
#         self.password_entry.grid(row=6, column=0, padx=0, pady=8, sticky="w")

#         save_button.grid(row=7, column=0, columnspan=2)

#         self.login_frame.pack()  # Adjust placement of login frame as needed

#     def save_data(self, form_website, form_name, form_password, add_window):
#         encrypted_website = auth.encrypt_data(form_website, self.static_key)
#         encrypted_name = auth.encrypt_data(form_name, self.static_key)
#         encrypted_password = auth.encrypt_data(form_password, self.static_key)

#         new_key_keeper = KeyKeeper(hashed_place= encrypted_website,hashed_name=encrypted_name, hashed_password=encrypted_password, user_id=self.user_id)
#         self.db.add(new_key_keeper)
#         self.db.commit()
#         self.db.close()
#         self.generate_table()
#         add_window.destroy()

#     # def edit_data(self, key_keeper_id):
#     #     # Retrieve the key keeper object from the database
#     #     key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()
#     #     edit_window = Tk()
#     #     edit_window.title("Edit Data")
#     #     edit_window.configure(background=FRAME_COLOR)  # Set background color

#     #     # Labels and entry fields for input
#     #     self.edit_frame = Frame(edit_window, background=FRAME_COLOR, padx=32, pady=32)
#     #     self.title = Label(edit_window, text="Edit your data entry", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#     #     self.website_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#     #                                 font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)
#     #     self.website_entry.insert(0,auth.decrypt_data(key_keeper.hashed_place, self.static_key))

#     #     self.username_title = Label(edit_window, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#     #     self.username_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#     #                                 font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)
#     #     self.username_entry.insert(0,auth.decrypt_data(key_keeper.hashed_name, self.static_key))

#     #     self.password_title = Label(edit_window, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#     #     self.password_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#     #                                 font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)


#     #     Label(edit_window, text="New Password:").grid(row=1, column=0)
#     #     password_entry = Entry(edit_window)
#     #     password_entry.grid(row=1, column=1)
#     #     password_entry.insert(0, auth.decrypt_data(key_keeper.hashed_password, self.static_key))  # Prefill with existing password

#     #     # Button to save edited data
#     #     save_button = Button(edit_window, text="Save", command=lambda: self.save_edited_data(key_keeper, name_entry.get(), password_entry.get(), edit_window))
#     #     save_button.grid(row=2, column=0, columnspan=2)

#     def edit_data(self, key_keeper_id):
#         # Retrieve the key keeper object from the database
#         key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()
#         edit_window = Tk()
#         edit_window.title("Edit Data")
#         edit_window.configure(background=FRAME_COLOR)  # Set background color

#         # Labels and entry fields for input
#         self.edit_frame = Frame(edit_window, background=FRAME_COLOR, padx=32, pady=32)
#         self.title = Label(edit_window, text="Edit your data entry", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#         self.website_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)
#         self.website_entry.insert(0,auth.decrypt_data(key_keeper.hashed_place, self.static_key))

#         self.username_title = Label(edit_window, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#         self.username_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)
#         self.username_entry.insert(0,auth.decrypt_data(key_keeper.hashed_name, self.static_key))

#         self.password_title = Label(edit_window, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
#         self.password_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
#                                     font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)


#         Label(edit_window, text="New Password:").grid(row=1, column=0)
#         password_entry = Entry(edit_window)
#         password_entry.grid(row=1, column=1)
#         password_entry.insert(0, auth.decrypt_data(key_keeper.hashed_password, self.static_key))  # Prefill with existing password

#         # Button to save edited data
#         save_button = Button(edit_window, text="Save", command=lambda: self.save_edited_data(key_keeper, susername_entry.get(), password_entry.get(), edit_window))
#         save_button.grid(row=2, column=0, columnspan=2)



#     def delete_data(self, key_keeper_id):
#         key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()

#         confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this entry?")
#         if confirmation:
#             self.db.delete(key_keeper)
#             self.db.commit()
#             print(f'Key keeper of id: {key_keeper_id} has been deleted.')
#             self.generate_table()

#     def save_edited_data(self, key_keeper, new_name, new_password, edit_window):
#         # Encrypt the edited data using the user's password
#         encrypted_name = auth.encrypt_data(new_name, self.static_key)
#         encrypted_password = auth.encrypt_data(new_password, self.static_key)

#         # Update the key keeper object with edited data
#         key_keeper.hashed_name = encrypted_name
#         key_keeper.hashed_password = encrypted_password

#         # Commit changes to the database
#         self.db.commit()

#         # Close the edit window
#         edit_window.destroy()

#         # Update the table to reflect the changes
#         self.generate_table()

#     def save_encrypted_data_to_csv(self):
#             # Retrieve key keepers data from the database
#             key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

#             # Open a CSV file in write mode
#             with open("encrypted_data.csv", "w", newline="") as csvfile:
#                 writer = csv.writer(csvfile)

#                 # Write header row
#                 writer.writerow(["ID", "Encrypted Name", "Encrypted Password"])

#                 # Write encrypted data rows
#                 for key_keeper in key_keepers:
#                     writer.writerow([key_keeper.id, key_keeper.hashed_name, key_keeper.hashed_password])

#             messagebox.showinfo("Backup", "Encrypted data has been saved to encrypted_data.csv")


class VaultPage(BaseModel):
    def __init__(self, screen: Tk, user_id: int, user_password: str, db: Session):
        super().__init__(screen)
        self.user_id = user_id
        self.user_password = user_password
        self.db = db
        self.static_key = generate_static_key(user_password)
        self.create_vault_page()
        self.id = 3
        self.generate_table()  # Generate table upon initialization

    def copy_to_clipboard(self, secret_key):
        pyperclip.copy(secret_key)

    def create_vault_page(self):
        self.table_frame = Frame(self.screen, background=settings.FRAME_COLOR, padx=32, pady=32,)
        self.table_frame.pack(expand=True, fill="both")

        self.canvas = Canvas(self.table_frame, background=settings.FRAME_COLOR,
                            highlightthickness=0, relief='ridge')
        self.canvas.pack(side="left", fill="both", expand=True)

        scrollbar = Scrollbar(self.table_frame, orient="vertical", command=self.canvas.yview)
        scrollbar.pack(side="right", fill="y")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.table_container = Frame(self.canvas, background=settings.FRAME_COLOR)
        self.canvas.create_window((0, 0), window=self.table_container, anchor="nw")

        # add_button = Button(self.table_frame, text="Add Data", command=self.add_data)
        add_button = CTkButton(master=self.table_frame, text='+', font=('yu gothic ui', 20, 'bold'), fg_color='#1d4ed8', hover_color=settings.HOVER_COLOR, corner_radius=8, width=48, height=48, command=self.add_data)

        backup_btn = Button(self.table_container, text="Backup your data", command=self.save_encrypted_data_to_csv)
        # backup_btn.grid(row=rows, column=2, columnspan=len(columns) - 2, pady=(20, 0))

        add_button.pack(side="top", pady=16, padx=16)


    def generate_table(self):
        for widget in self.table_container.winfo_children():
            widget.destroy()

        columns = ("#", "WEBSITE", 'USERNAME', "PASSWORD", "ACTIONS")

        for col_idx, col_name in enumerate(columns):
            self.header = Label(self.table_container, text=col_name, background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 10, 'bold'))
            if col_name == "ACTIONS":
                # Calculate the middle column index for centering the header
                middle_col_idx = col_idx + 1
                self.header.grid(row=0, column=col_idx, padx=8, pady=16, sticky='nsew', columnspan=3)  # Spanning across 3 columns for "ACTIONS"
                self.table_container.grid_columnconfigure(middle_col_idx, weight=1)  # Make middle column expandable
            else:
                self.header.grid(row=0, column=col_idx, padx=8, pady=16, sticky='nsew')

        key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

        rows = 1
        for row_idx, key_keeper in enumerate(key_keepers, start=1):
            decrypted_website = decrypt_data(key_keeper.hashed_place, self.static_key)
            decrypted_keys = decrypt_data(key_keeper.hashed_name, self.static_key)  # Decrypt using Fernet key
            decrypted_password = decrypt_data(key_keeper.hashed_password, self.static_key)  # Decrypt using Fernet key

            self.index = Label(self.table_container, text=str(row_idx)+'.', background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
            self.website = Label(self.table_container, text=decrypted_website, background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
            self.decrypted_keys = Label(self.table_container, text=decrypted_keys, background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
            self.decrypted_password = Label(self.table_container, text=decrypted_password, background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))

            copy_button = CTkButton(self.table_container, width=32, text="Copy", font=('yu gothic ui', 12, 'bold'), fg_color=settings.FRAME_COLOR, hover_color=settings.ENTRY_COLOR, border_color=settings.ENTRY_COLOR, border_width=2, corner_radius=32, command=self.copy_to_clipboard(decrypted_password))
            edit_button = CTkButton(self.table_container, width=32, text="Edit", font=('yu gothic ui', 12, 'bold'), fg_color=settings.FRAME_COLOR, hover_color=settings.SUCCESS_BORDER_COLOR, border_color=settings.SUCCESS_BORDER_COLOR, border_width=2, corner_radius=32, command=lambda key=key_keeper.id: self.edit_data(key))
            delete_button = CTkButton(self.table_container, width=32, text="Delete", font=('yu gothic ui', 12, 'bold'), fg_color=settings.FRAME_COLOR, hover_color=settings.FAIL_BORDER_COLOR, border_color=settings.FAIL_BORDER_COLOR, border_width=2, corner_radius=32, command=lambda key=key_keeper.id: self.delete_data(key))

            self.index.grid(row=rows, column=0, padx=4, pady=4, sticky='nsew')
            self.website.grid(row=rows, column=1, padx=4, pady=4, sticky='nsew')
            self.decrypted_keys.grid(row=rows, column=2, padx=4, pady=4, sticky='nsew')
            self.decrypted_password.grid(row=rows, column=3, padx=4, pady=4, sticky='nsew')

            copy_button.grid(row=rows, column=4, padx=2, pady=2)
            edit_button.grid(row=rows, column=5, padx=2, pady=2)
            delete_button.grid(row=rows, column=6, padx=2, pady=2)

            rows += 1

        self.canvas.update_idletasks()
        self.canvas.config(scrollregion=self.canvas.bbox("all"))

    def add_data(self):
        add_window = Tk()
        add_window.title("Add Data")
        add_window.configure(background=settings.FRAME_COLOR)  # Set background color

        self.login_frame = Frame(add_window, background=settings.FRAME_COLOR, padx=32, pady=32)
        self.title = Label(self.login_frame, text="Add data to your database", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))

        self.website_label = Label(self.login_frame, text="Website", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
        self.website_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)

        self.username_label = Label(self.login_frame, text="Username", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
        self.username_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)

        self.password_label = Label(self.login_frame, text="Password", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 12, 'bold'))
        self.password_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)

        save_button = CTkButton(master=self.login_frame, text='Save', font=('yu gothic ui', 16, 'bold'), fg_color='#1d4ed8', hover_color= settings.HOVER_COLOR, corner_radius=32,
                                    width=340, height=48,
                                    command=lambda: self.save_data(self.website_entry.get(), self.username_entry.get(), self.password_entry.get(), add_window))

        self.title.grid(row=0, column=0, padx=0, pady=32, sticky="w")
        self.website_label.grid(row=1, column=0, padx=0, pady=0, sticky="w")
        self.website_entry.grid(row=2, column=0, padx=0, pady=8, sticky="w")

        self.username_label.grid(row=3, column=0, padx=0, pady=0, sticky="w")
        self.username_entry.grid(row=4, column=0, padx=0, pady=8, sticky="w")

        self.password_label.grid(row=5, column=0, padx=0, pady=0, sticky="w")
        self.password_entry.grid(row=6, column=0, padx=0, pady=8, sticky="w")

        save_button.grid(row=7, column=0, columnspan=2)

        self.login_frame.pack()  # Adjust placement of login frame as needed

    def save_data(self, form_website, form_name, form_password, add_window):
        encrypted_website = encrypt_data(form_website, self.static_key)
        encrypted_name = encrypt_data(form_name, self.static_key)
        encrypted_password = encrypt_data(form_password, self.static_key)

        new_key_keeper = KeyKeeper(hashed_place= encrypted_website,hashed_name=encrypted_name, hashed_password=encrypted_password, user_id=self.user_id)
        self.db.add(new_key_keeper)
        self.db.commit()
        self.db.close()
        self.generate_table()
        add_window.destroy()

    def edit_data(self, key_keeper_id):
        key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()
        edit_window = Tk()
        edit_window.title("Edit Data")
        edit_window.configure(background=settings.FRAME_COLOR)

        self.edit_frame = Frame(edit_window, background=settings.FRAME_COLOR, padx=32, pady=32)
        edit_title = Label(edit_window, text="Edit your data entry", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))

        self.website_title = Label(edit_window, text="Website", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
        self.website_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)
        self.website_entry.insert(0,decrypt_data(key_keeper.hashed_place, self.static_key))

        self.username_title = Label(edit_window, text="Username", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
        self.username_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)
        self.username_entry.insert(0,decrypt_data(key_keeper.hashed_name, self.static_key))

        self.password_title = Label(edit_window, text="Password", background=settings.FRAME_COLOR, fg=settings.TEXT_COLOR, font=('yu gothic ui', 18, 'bold'))
        self.password_entry = CTkEntry(edit_window, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), fg_color=settings.ENTRY_COLOR)
        self.password_entry.insert(0,decrypt_data(key_keeper.hashed_password, self.static_key))

        save_button = CTkButton(master=edit_window, text='Save', font=('yu gothic ui', 20, 'bold'), fg_color='#1d4ed8', hover_color=settings.HOVER_COLOR, corner_radius=8, width=48, height=48,
        command=lambda: self.save_edited_data(key_keeper, self.website_entry.get(), self.username_entry.get(), self.password_entry.get(), edit_window))

        edit_title.grid(row=0, column=0)
        self.website_title.grid(row=1, column=0)
        self.website_entry.grid(row=2, column=0)
        self.username_title.grid(row=3, column=0)
        self.username_entry.grid(row=4, column=0)
        self.password_title.grid(row=5, column=0)
        self.password_entry.grid(row=6, column=0)
        save_button.grid(row=7, column=0)

    def delete_data(self, key_keeper_id):
        key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()

        confirmation = messagebox.askyesno(f"Confirmation", "Are you sure you want to delete this entry?")
        if confirmation:
            self.db.delete(key_keeper)
            self.db.commit()
            self.db.close()
            self.generate_table()

    def save_edited_data(self, key_keeper, new_website, new_name, new_password, edit_window):
        # Encrypt the edited data using the user's password
        encrypted_website = encrypt_data(new_website, self.static_key)
        encrypted_name = encrypt_data(new_name, self.static_key)
        encrypted_password = encrypt_data(new_password, self.static_key)

        # Update the key keeper object with edited data
        key_keeper.hashed_place = encrypted_website
        key_keeper.hashed_name = encrypted_name
        key_keeper.hashed_password = encrypted_password

        # Commit changes to the database
        self.db.commit()

        # Close the edit window
        edit_window.destroy()

        # Update the table to reflect the changes
        self.generate_table()

    def save_encrypted_data_to_csv(self):
            # Retrieve key keepers data from the database
            key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

            # Open a CSV file in write mode
            with open("encrypted_data.csv", "w", newline="") as csvfile:
                writer = csv.writer(csvfile)

                # Write header row
                writer.writerow(["ID", "Encrypted Name", "Encrypted Password"])

                # Write encrypted data rows
                for key_keeper in key_keepers:
                    writer.writerow([key_keeper.id, key_keeper.hashed_name, key_keeper.hashed_password])

            messagebox.showinfo("Backup", "Encrypted data has been saved to encrypted_data.csv")








