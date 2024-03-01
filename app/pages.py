import tkinter as tk
import db as _db
import bcrypt
import sqlite3

BACKGROUND_COLOR = '#09090b'
LOGIN_FRAME_COLOR = '#18181b'
LOGIN_TEXT_COLOR ='#1999ff'
ENTRY_COLOR = '#32353c'
TEXT_COLOR = '#e8eddf'

TEXT_FONT = 'Lato'
SCREEN_DIMENSIONS = '1200x720'
WINDOW_WIDTH, WINDOW_HEIGHT = 600, 600

class StartPage(tk.Frame):
    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

class BaseModel(tk.Tk):
    def __init__(self, display):
        self.display = display
        self.display.resizable(False, False)
        self.display['background']= LOGIN_FRAME_COLOR
        self.create_main_frame()
        
    def create_main_frame(self):
        self.main_frame = tk.Frame(self.display, width=1200, height=720, bg=BACKGROUND_COLOR)
        self.main_frame.place(x=0, y=0)
        self.main_frame.grid(row=0, column=0)
    
    def page_name(self, page_name: str):
        self.title_label = tk.Label(self.main_frame, text=page_name, bg=BACKGROUND_COLOR, fg='white',font=('Lato', 16))
    
    def clear_page(self):
        for widget in self.main_frame.winfo_children():
            widget.destroy()
        print('Widgets cleared.')

class SignupPage(BaseModel):
    def __init__(self, display):
        super().__init__(display)
        self.page_name('CREATE ACCOUNT HERE')
        self.create_signup_frame(self.main_frame)

    def create_signup_frame(self, main_frame):
        self.signup_frame = tk.Frame(main_frame, width=372, height=259, bg=ENTRY_COLOR)
        self.signup_frame.place(x=114, y=50)

        self.username_label = tk.Label(self.signup_frame, text="USERNAME", bg=LOGIN_FRAME_COLOR, fg=LOGIN_TEXT_COLOR, font=('Ubuntu', 9))
        self.username_entry = tk.Entry(self.signup_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 14))
       
        self.password_label = tk.Label(self.signup_frame, text="PASSWORD", bg=LOGIN_FRAME_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9))
        self.password_entry = tk.Entry(self.signup_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 14), show='*')
       
        self.re_password_label = tk.Label(self.signup_frame, text="RE-ENTER PASSWORD", bg=LOGIN_FRAME_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9))
        self.re_password_entry = tk.Entry(self.signup_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 14), show='*')

        self.signup_btn = tk.Button(self.signup_frame, width=36, pady=8, text="Sign Up", bg=LOGIN_TEXT_COLOR, border=1, fg=TEXT_COLOR)
        
        self.username_label.place(x=20, y=20)
        self.username_entry.place(x=20, y=40)
        self.password_label.place(x=20, y=80)
        self.password_entry.place(x=20, y=100)
        self.re_password_label.place(x=20, y=140)
        self.re_password_entry.place(x=20, y=160)
        self.signup_btn.place(x=60 ,y=205)
        self.signup_btn.config(command=self.sign_up)
    def sign_up(self):
        conn = sqlite3.connect('data.db')
        print('Connected to database.')
        c = conn.cursor()
        hashed_password = bcrypt.hashpw(self.password_entry.get().encode('utf-8'), bcrypt.gensalt())
        c.execute("INSERT INTO users (username, password) VALUES (?,?)", (self.username_entry.get(), hashed_password))
        
        conn.commit()
        conn.close()
        
        
class LoginPage(BaseModel):
    def __init__(self, display):
        super().__init__(display)
        self.page_name('LOG IN')
        self.create_login_form(self.main_frame)

    def create_login_form(self, main_frame):
        self.login_frame = tk.Frame(main_frame, width=372, height=259, bg=LOGIN_FRAME_COLOR)
        self.login_frame.place(x=114, y=50)

        self.username_label = tk.Label(self.login_frame, text="USERNAME", bg=LOGIN_FRAME_COLOR, fg=LOGIN_TEXT_COLOR, font=('Ubuntu', 9))
        self.username_entry = tk.Entry(self.login_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 14))
       
        self.password_label = tk.Label(self.login_frame, text="PASSWORD", bg=LOGIN_FRAME_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9))
        self.password_entry = tk.Entry(self.login_frame, width=30, bg=ENTRY_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 14), show='*')

        self.registernow_btn = tk.Button(self.login_frame, text="Not registered? Signup here!", bg=LOGIN_FRAME_COLOR, fg=TEXT_COLOR, font=('Ubuntu', 9))
        self.login_btn = tk.Button(self.login_frame, width=36, pady=8, text="LOGIN", bg=LOGIN_TEXT_COLOR, border=1, fg=TEXT_COLOR)
        self.login_btn.place(x=60 ,y=160)
        self.login_btn.config(command=self.login)
        
        self.username_label.place(x=20, y=20)
        self.username_entry.place(x=20, y=40)
        self.password_label.place(x=20, y=80)
        self.password_entry.place(x=20, y=100)
        self.registernow_btn.place(x=100, y=215)

    def login(self):
        conn = sqlite3.connect("data.db")
        c = conn.cursor()
        c.execute("SELECT id, password FROM users WHERE username = ?", (self.username_entry.get(),))
        user_id, stored_password = c.fetchone()
        if bcrypt.checkpw(self.password_entry.get().encode('utf-8'), stored_password):
            self.login_frame.destroy()
            self.vault_page = VaultPage(self.display, user_id)
        else:
            print("Incorrect username or password.")
            self.vibrate()
        conn.close()
    
class VaultPage(BaseModel):
    def __init__(self, display):
        super().__init__(display)
        self.page_name('WELCOME TO YOUR VAULT')
        self.create_vault_form(self.main_frame)

    def create_vault_form(self, main_frame):
        self.vault_frame = tk.Frame(main_frame, width=372, height=259, bg=LOGIN_FRAME_COLOR)
        self.vault_frame.place(x=114, y=50)
        self.add_btn = tk.Button(self.main_frame, text='Add Password')
        self.add_btn.place(x=300, y=250)
        website_label = tk.Label(self.vault_frame, text='Website')
        username_label = tk.Label(self.vault_frame, text='Username')
        password_label = tk.Label(self.vault_frame, text='Password')

        website_label.grid(row=0, column=0, padx=40)
        username_label.grid(row=0, column=1, padx=40)
        password_label.grid(row=0, column=2, padx=40)