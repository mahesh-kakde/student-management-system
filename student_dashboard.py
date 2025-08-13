import tkinter as tk # type: ignore

root = tk.Tk()
root.geometry('500x600')
root.title("Student Registration and Management System")
root.resizable(False, False)
root.iconbitmap('icons/silly_cat.ico')
footer_lb = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_lb.pack(side = 'bottom')

bg_color = '#273b7a'

def switch(indicator, page):
    home_btn_indicator.config(bg = '#c3c3c3')
    student_card_btn_indicator.config(bg = '#c3c3c3')
    security_btn_indicator.config(bg = '#c3c3c3')
    edit_data_btn_indicator.config(bg = '#c3c3c3')
    delete_account_btn_indicator.config(bg = '#c3c3c3')
    indicator.config(bg = bg_color)
    for child in pages_fm.winfo_children():
        child.destroy()
        root.update()
    page()

dashboard_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

options_fm = tk.Frame(dashboard_fm, bg = '#c3c3c3', highlightbackground = bg_color, highlightthickness = 2)
options_fm.place(x = 0, y = 0, width = 120, height = 539)

home_btn = tk.Button(options_fm, text = "Home", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, command = lambda: switch(indicator = home_btn_indicator, page = home_page))
home_btn.place(x = 4, y = 50)
home_btn_indicator = tk.Label(options_fm, bg = bg_color)
home_btn_indicator.place(x = 2, y = 48, width = 3, height = 40)

student_card_btn = tk.Button(options_fm, text = "\U0001F4C4 Student\nCard", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = student_card_btn_indicator, page = dashboard_student_card_page))
student_card_btn.place(x = 4, y = 100)
student_card_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
student_card_btn_indicator.place(x = 2, y = 102, width = 3, height = 55)

security_btn = tk.Button(options_fm, text = "\U0001F512 Account\n Safety", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = security_btn_indicator, page = security_page))
security_btn.place(x = 4, y = 170)
security_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
security_btn_indicator.place(x = 2, y = 172, width = 3, height = 55)

edit_data_btn = tk.Button(options_fm, text = "\U0001F4DD Edit\nData", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = edit_data_btn_indicator, page = edit_data_page))
edit_data_btn.place(x = 4, y = 240)
edit_data_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
edit_data_btn_indicator.place(x = 2, y = 242, width = 3, height = 55)

delete_account_btn = tk.Button(options_fm, text = "\U0001F6A8 Delete\nAccount", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = delete_account_btn_indicator, page = delete_account_page))
delete_account_btn.place(x = 4, y = 310)
delete_account_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
delete_account_btn_indicator.place(x = 2, y = 312, width = 3, height = 55)

logout_btn = tk.Button(options_fm, text = "Logout", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color)
logout_btn.place(x = 4, y = 380)

def home_page():
    home_page_fm = tk.Frame(pages_fm)
    home_page_lb = tk.Label(home_page_fm, text = "Home Page", font = ('bold', 15))
    home_page_lb.place(x = 100, y = 200)
    home_page_fm.pack(fill = tk.BOTH, expand = True)

def dashboard_student_card_page():
    dashboard_student_card_page_fm = tk.Frame(pages_fm)
    dashboard_student_card_page_lb = tk.Label(dashboard_student_card_page_fm, text = "Student Card Page", font = ('bold', 15))
    dashboard_student_card_page_lb.place(x = 100, y = 200)
    dashboard_student_card_page_fm.pack(fill = tk.BOTH, expand = True)

def security_page():
    security_page_fm = tk.Frame(pages_fm)
    security_page_lb = tk.Label(security_page_fm, text = "Account Safety Page", font = ('bold', 15))
    security_page_lb.place(x = 100, y = 200)
    security_page_fm.pack(fill = tk.BOTH, expand = True)

def edit_data_page():
    edit_data_page_fm = tk.Frame(pages_fm)
    edit_data_page_lb = tk.Label(edit_data_page_fm, text = "Edit Data Page", font = ('bold', 15))
    edit_data_page_lb.place(x = 100, y = 200)
    edit_data_page_fm.pack(fill = tk.BOTH, expand = True)

def delete_account_page():
    delete_account_page_fm = tk.Frame(pages_fm)
    delete_account_page_lb = tk.Label(delete_account_page_fm, text = "Delete Account Page", font = ('bold', 15))
    delete_account_page_lb.place(x = 100, y = 200)
    delete_account_page_fm.pack(fill = tk.BOTH, expand = True)

pages_fm = tk.Frame(dashboard_fm)
pages_fm.place(x = 122, y = 5, width = 350, height = 515)

dashboard_fm.pack(pady = 5)
dashboard_fm.pack_propagate(False)
dashboard_fm.configure(width = 480, height = 545)

home_page()

root.mainloop()