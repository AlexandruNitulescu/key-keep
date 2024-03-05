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
        self.login_frame = Frame(self.screen, background=FRAME_COLOR, padx=32, pady=64,)
        self.login_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username_label = Label(self.login_frame, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), )
        # self.username_entry = Entry(self.login_frame, background=BASE_COLOR, selectbackground=MAIN_COLOR,
        #                             highlightthickness=0, borderwidth=0, bd=0,
        #                             width=30, fg=TEXT_COLOR, font=('Lato', 16), relief='flat')
        # self.username_entry = Entry(self.login_frame, background='#f3f4f6', selectbackground=MAIN_COLOR,
        #                             highlightthickness=0, borderwidth=0, bd=0,
        #                             width=40, fg='#334155', relief='flat',
        #                             font=('yu gothic ui', 14))
        
        self.username_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                            font=('yu gothic ui', 14), fg_color=ENTRY_COLOR)


        self.password_label= Label(self.login_frame, text="Password", fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), background=FRAME_COLOR)
        # self.password_entry = Entry(self.login_frame, background='#f3f4f6', selectbackground=MAIN_COLOR,
        #                             highlightthickness=0, borderwidth=0, bd=0,
        #                             fg='#334155', font=('yu gothic ui', 14), relief='flat', show='*')
        self.password_entry = CTkEntry(self.login_frame, border_width=0, width=340, height=40, corner_radius=2,
                                    font=('yu gothic ui', 14), show='*', fg_color=ENTRY_COLOR)
        
        # self.login_btn = Button(self.login_frame, text="LOGIN", bg=MAIN_COLOR, border=0, fg=TEXT_COLOR,
        #                         highlightthickness=0, borderwidth=0, bd=0,highlightbackground=BACKGROUND_COLOR,
        #                         # borderless=True, 
        #                         width=40,
        #                         command=self.login)
        self.login_btn = CTkButton(master=self.login_frame, text='Sign In', font=('yu gothic ui', 16, 'bold'), fg_color='#1d4ed8', hover_color= HOVER_COLOR, corner_radius=32,
                                    width=340, height=48,
                                    command=self.login)
        
        self.register_btn = CTkButton(master=self.login_frame, text='Register Now', font=('yu gothic ui', 16, 'bold'), fg_color=FRAME_COLOR, hover_color=FRAME_COLOR, border_color=ENTRY_COLOR, border_width=2, corner_radius=32,
                                    width=340, height=48,
                                    command=self.open_register_page)
        
        # self.register_btn = Button(self.login_frame, text="Not registered? Signup here!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9),
        #                         #    borderless=True, 
        #                            command=self.open_register_page)

        self.username_label.grid(row=0, column=0, padx=0, pady=0, sticky="w")
        self.username_entry.grid(row=1, column=0, padx=0, pady=8, sticky="w")

        self.password_label.grid(row=2, column=0, padx=0, pady=0, sticky="w")
        self.password_entry.grid(row=3, column=0, padx=0, pady=8, sticky="w")

        self.login_btn.grid(row=4, column=0, padx=0, pady=32, sticky="w")
        self.register_btn.grid(row=5, column=0, padx=0, pady=0, sticky="w")

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
        register_page = RegisterPage(self.screen)

    def navigate_to_vault(self, user_id: int, password, db: Session):
        self.clear_page()
        vault_page = VaultPage(self.screen, user_id=user_id, user_password=password, db=db)

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
        self.register_frame = Frame(self.screen, background=FRAME_COLOR, padx=32, pady=64)
        self.register_frame.place(relx=0.5, rely=0.5, anchor="center")

        self.username_label = Label(self.register_frame, text="Username", background=FRAME_COLOR, fg=TEXT_COLOR, font=('yu gothic ui', 12, 'bold'), )
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
                                # borderless=True, 
                                command=self.register)
       
        self.go_back_btn = Button(self.register_frame, text="Go back!", bg=BACKGROUND_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 16),
                                #    borderless=True, 
                                   command=self.open_home_page)

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


    def show_error_frame(self, error_message: str):
        error_frame = Frame(self.screen)
        error_label = Label(error_frame, text=error_message, fg="#b91c1c", bg=FAIL_COLOR, font=('Lato', 16), padx=16, pady=16,
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


class VaultPage(BaseModel):
    def __init__(self, screen: Tk, user_id: int, user_password: str, db: Session):
        super().__init__(screen)
        self.user_id = user_id
        self.user_password = user_password  # Encode the password properly
        self.db = db
        self.static_key = auth.generate_static_key(user_password)
        self.create_vault_page()
        self.id = 3
        self.generate_table()  # Generate table upon initialization
        scrollbar = Scrollbar(screen)
        scrollbar.pack( side = RIGHT, fill=Y )

    def copy_to_clipboard(self, secret_key):
        pyperclip.copy(secret_key)


    def create_vault_page(self):
            # Create a frame to hold the table and buttons
            self.table_frame = ttk.Frame(self.screen)
            self.table_frame.pack(expand=True, fill="both")

            # Button to add new data
            add_button = Button(self.table_frame, text="Add Data", command=self.add_data)
            add_button.pack(side="top", pady=5)  # Use pack here instead of grid


    def generate_table(self):
        for widget in self.table_frame.winfo_children():
            widget.destroy()

        # Define columns for the table
        columns = ("ID", "Name", "Password", "Actions")

        # Define column headings
        for col_idx, col_name in enumerate(columns):
            Label(self.table_frame, text=col_name).grid(row=1, column=col_idx, padx=5, pady=5)

        # Retrieve key keepers data from the database
        key_keepers = self.db.query(KeyKeeper).filter_by(user_id=self.user_id).all()

        # Populate the table with key keepers data
        rows = 0
        for row_idx, key_keeper in enumerate(key_keepers, start=2):
            decrypted_keys = auth.decrypt_data(key_keeper.hashed_name, self.static_key)  # Decrypt using Fernet key
            decrypted_password = auth.decrypt_data(key_keeper.hashed_password, self.static_key)  # Decrypt using Fernet key
            
            Label(self.table_frame, text=key_keeper.id,
                font=('Lato', 11)).grid(row=row_idx, column=0, padx=2, pady=2)
            Label(self.table_frame, text=decrypted_keys,
                  font=('Lato', 11)).grid(row=row_idx, column=1, padx=2, pady=2)
            Label(self.table_frame, text=decrypted_password,
                  font=('Lato', 11)).grid(row=row_idx, column=2, padx=2, pady=2)

            copy_button = Button(self.table_frame, text="Copy", command=self.copy_to_clipboard(decrypted_password))
            copy_button.grid(row=row_idx, column=3, padx=1, pady=1)
            # Create buttons for actions (edit and delete)
            edit_button = Button(self.table_frame, text="Edit", command=lambda key=key_keeper.id: self.edit_data(key))
            edit_button.grid(row=row_idx, column=4, padx=5, pady=5)

            delete_button = Button(self.table_frame, text="Delete", command=lambda key=key_keeper.id: self.delete_data(key))
            delete_button.grid(row=row_idx, column=5, padx=5, pady=5)
            rows +=1


        add_button = Button(self.table_frame, text="Add Data", command=self.add_data)
        add_button.grid(row=rows+2,column=0)

        backup_btn = Button(self.table_frame, text="Backup", command=self.save_encrypted_data_to_csv)
        backup_btn.grid(row=rows+2,column=2)

    def add_data(self):
        # Create a new window for adding data
        add_window = Tk()
        add_window.title("Add Data")

        # Labels and entry fields for input
        Label(add_window, text="Name:").grid(row=0, column=0)
        name_entry = Entry(add_window)
        name_entry.grid(row=0, column=1)

        Label(add_window, text="Password:").grid(row=1, column=0)
        password_entry = Entry(add_window)
        password_entry.grid(row=1, column=1)

        # Button to save data
        save_button = Button(add_window, text="Save", command=lambda: self.save_data(name_entry.get(), password_entry.get(), add_window))
        save_button.grid(row=2, column=0, columnspan=2)

    def save_data(self, form_name, form_password, add_window):
        # Encrypt the data using the user's password
        encrypted_name = auth.encrypt_data(form_name, self.static_key)
        encrypted_password = auth.encrypt_data(form_password, self.static_key)

        # Create a new KeyKeeper instance and add it to the database
        new_key_keeper = KeyKeeper(hashed_name=encrypted_name, hashed_password=encrypted_password, user_id=self.user_id)
        self.db.add(new_key_keeper)
        self.db.commit()

        # Close the add data window
        add_window.destroy()

        # Update the table to reflect the changes
        self.generate_table()


    def edit_data(self, key_keeper_id):
        # Retrieve the key keeper object from the database
        key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()
        
        # Create a new window for editing data
        edit_window = Tk()
        edit_window.title("Edit Data")

        # Labels and entry fields for input
        Label(edit_window, text="New Name:").grid(row=0, column=0)
        name_entry = Entry(edit_window)
        name_entry.grid(row=0, column=1)
        name_entry.insert(0, auth.decrypt_data(key_keeper.hashed_name, self.static_key))  # Prefill with existing name
        
        Label(edit_window, text="New Password:").grid(row=1, column=0)
        password_entry = Entry(edit_window)
        password_entry.grid(row=1, column=1)
        password_entry.insert(0, auth.decrypt_data(key_keeper.hashed_password, self.static_key))  # Prefill with existing password

        # Button to save edited data
        save_button = Button(edit_window, text="Save", command=lambda: self.save_edited_data(key_keeper, name_entry.get(), password_entry.get(), edit_window))
        save_button.grid(row=2, column=0, columnspan=2)

    def delete_data(self, key_keeper_id):
        # Retrieve the key keeper object from the database
        key_keeper = self.db.query(KeyKeeper).filter_by(id=key_keeper_id).first()
        
        # Confirm deletion with a message box
        confirmation = messagebox.askyesno("Confirmation", "Are you sure you want to delete this entry?")
        if confirmation:
            # Delete the key keeper object from the database
            self.db.delete(key_keeper)
            self.db.commit()
            # Update the table to reflect the changes
            self.generate_table()

    def save_edited_data(self, key_keeper, new_name, new_password, edit_window):
        # Encrypt the edited data using the user's password
        encrypted_name = auth.encrypt_data(new_name, self.static_key)
        encrypted_password = auth.encrypt_data(new_password, self.static_key)

        # Update the key keeper object with edited data
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


