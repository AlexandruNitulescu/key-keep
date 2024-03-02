from tkinter import ttk
from sqlalchemy.orm import Session
from sqlalchemy import Table, MetaData

def generate_table(table_window, db: Session, table_name: str):
    # Reflect the table from the database
    metadata = MetaData()
    table = Table(table_name, metadata, autoload=True, autoload_with=db.bind)

    # Get column names from the reflected table
    columns = [column.name for column in table.columns]

    # Create the Treeview widget with the dynamic columns
    tree = ttk.Treeview(table_window, columns=columns, show="headings")
    
    # Define column headings
    for col in columns:
        tree.heading(col, text=col)

    # Retrieve data from the reflected table
    data = db.query(table).all()

    # Populate the table with data
    for row in data:
        tree.insert("", "end", values=[getattr(row, col) for col in columns])

    # Pack the Treeview widget to display it
    tree.pack(expand=True, fill="both")

    return tree
