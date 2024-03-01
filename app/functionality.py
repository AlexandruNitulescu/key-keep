

def clear_input_fields(self):
    self.username_entry.delete(0, 'end')
    self.password_entry.delete(0, 'end')
    self.re_password_entry.delete(0, 'end')
    self.username_entry.focus_set()