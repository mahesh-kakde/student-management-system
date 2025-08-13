import tkinter as tk # type: ignore

root = tk.Tk()
root.geometry('500x600')
root.title("Student Registration and Management System")
root.resizable(False, False)
root.iconbitmap('icons/silly_cat.ico')
footer_lb = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_lb.pack(side = 'bottom')

bg_color = '#273b7a'
admin_login_icon = tk.PhotoImage(file = 'icons/admin_img.png')
locked_icon = tk.PhotoImage(file = 'icons/locked_img.png')
unlocked_icon = tk.PhotoImage(file = 'icons/unlocked_img.png')

def show_hide_password():
    if password_ent['show'] == "*":
        password_ent.config(show = '')
        show_hide_btn.config(image = unlocked_icon)
    else:
        password_ent.config(show = "*")
        show_hide_btn.config(image = locked_icon)

admin_login_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

heading_lb = tk.Label(admin_login_page_fm, text = "Admin Portal Login", font = ('bold', 18), bg = bg_color, fg = 'white')
heading_lb.place(x = 0, y = 0, width = 400)

back_btn = tk.Button(admin_login_page_fm, text = "←", font = ('bold', 20), bd = 0, fg = bg_color)
back_btn.place(x = 5, y = 40)

admin_icon_lb = tk.Label(admin_login_page_fm, image = admin_login_icon)
admin_icon_lb.place(x = 150, y = 40)

username_lb = tk.Label(admin_login_page_fm, text = "Admin ID:", font = ('bold', 15), fg = bg_color)
username_lb.place(x = 80, y = 150)
username_ent = tk.Entry(admin_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
username_ent.place(x = 80, y = 185)

password_lb = tk.Label(admin_login_page_fm, text = "Password:", font = ('bold', 15), fg = bg_color)
password_lb.place(x = 80, y = 245)
password_ent = tk.Entry(admin_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, show = "*")
password_ent.place(x = 80, y = 280)
show_hide_btn = tk.Button(admin_login_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
show_hide_btn.place(x = 310, y = 273)

login_btn = tk.Button(admin_login_page_fm, text = "Login", font = ('bold', 15), bg = bg_color, fg = 'white')
login_btn.place(x = 120, y = 355, width = 160, height = 35)

admin_login_page_fm.pack(pady = 30)
admin_login_page_fm.pack_propagate(False)
admin_login_page_fm.configure(width = 400, height = 450)

root.mainloop()