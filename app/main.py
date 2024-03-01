from tkinter import *
from pages import LoginPage, SignupPage, VaultPage
import db as _db

window = Tk()
window.eval("tk::PlaceWindow . center")
window.title('Key Keep | Save your passwords secretly!')
login = LoginPage(window)
_db.database_instance()
window.mainloop()    
