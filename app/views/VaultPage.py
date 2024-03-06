from tkinter import *
from .BasePage import BaseModel
from customtkinter import *
from sqlalchemy.orm import Session
from authentication import generate_static_key, decrypt_data, encrypt_data
import settings
from models import KeyKeeper
from tkinter import messagebox 
import csv
import pyperclip



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





