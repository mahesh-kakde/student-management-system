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
    find_student_btn_indicator.config(bg = '#c3c3c3')
    announcements_btn_indicator.config(bg = '#c3c3c3')
    indicator.config(bg = bg_color)
    for child in pages_fm.winfo_children():
        child.destroy()
        root.update()
    page()

dashboard_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

options_fm = tk.Frame(dashboard_fm, bg = '#c3c3c3', highlightbackground = bg_color, highlightthickness = 2)
options_fm.place(x = 0, y = 0, width = 120, height = 539)

home_btn = tk.Button(options_fm, text = "Home", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, command = lambda: switch(indicator = home_btn_indicator, page = home_page))
home_btn.place(x = 10, y = 50)
home_btn_indicator = tk.Label(options_fm, bg = bg_color)
home_btn_indicator.place(x = 5, y = 48, width = 3, height = 40)

find_student_btn = tk.Button(options_fm, text = "\U0001F50D Find\nStudent", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = find_student_btn_indicator, page = find_student_page))
find_student_btn.place(x = 10, y = 100)
find_student_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
find_student_btn_indicator.place(x = 5, y = 102, width = 3, height = 55)

announcements_btn = tk.Button(options_fm, text = "\U0001F4E2 Annou-\nncements", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, justify = tk.LEFT, command = lambda: switch(indicator = announcements_btn_indicator, page = announcements_page))
announcements_btn.place(x = 10, y = 170)
announcements_btn_indicator = tk.Label(options_fm, bg = '#c3c3c3')
announcements_btn_indicator.place(x = 5, y = 172, width = 3, height = 55)

logout_btn = tk.Button(options_fm, text = "Logout", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color)
logout_btn.place(x = 10, y = 236)

def home_page():
    home_page_fm = tk.Frame(pages_fm)
    home_page_lb = tk.Label(home_page_fm, text = "Home Page", font = ('bold', 15))
    home_page_lb.place(x = 100, y = 200)
    home_page_fm.pack(fill = tk.BOTH, expand = True)

def find_student_page():
    find_student_page_fm = tk.Frame(pages_fm)
    find_student_page_lb = tk.Label(find_student_page_fm, text = "Find Student Page", font = ('bold', 15))
    find_student_page_lb.place(x = 100, y = 200)
    find_student_page_fm.pack(fill = tk.BOTH, expand = True)

def announcements_page():
    announcements_page_fm = tk.Frame(pages_fm)
    announcements_page_lb = tk.Label(announcements_page_fm, text = "Announcements Page", font = ('bold', 15))
    announcements_page_lb.place(x = 100, y = 200)
    announcements_page_fm.pack(fill = tk.BOTH, expand = True)

pages_fm = tk.Frame(dashboard_fm)
pages_fm.place(x = 122, y = 5, width = 350, height = 515)

dashboard_fm.pack(pady = 5)
dashboard_fm.pack_propagate(False)
dashboard_fm.configure(width = 480, height = 545)

home_page()

root.mainloop()