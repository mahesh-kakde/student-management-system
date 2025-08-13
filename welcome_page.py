import tkinter as tk # type: ignore

root = tk.Tk()
root.geometry('500x600')
root.title("Student Registration and Management System")
root.resizable(False, False)
root.iconbitmap('icons/silly_cat.ico')
footer_lb = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_lb.pack(side = 'bottom')

bg_color = '#273b7a'
student_login_icon = tk.PhotoImage(file = 'icons/login_student_img.png')
admin_login_icon = tk.PhotoImage(file = 'icons/admin_img.png')
add_student_icon = tk.PhotoImage(file = 'icons/add_student_img.png')

welcome_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

heading_lb = tk.Label(welcome_page_fm, text = "Student Registration\nand Management System", font = ('bold', 18), bg = bg_color, fg = 'white')
heading_lb.place(x = 0, y = 0, width = 400)

student_login_btn = tk.Button(welcome_page_fm, text = "Student Login", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white')
student_login_btn.place(x = 150, y = 125, width = 200)
student_login_img = tk.Button(welcome_page_fm, image = student_login_icon, bd = 0)
student_login_img.place(x = 60, y = 100)

admin_login_btn = tk.Button(welcome_page_fm, text = "Admin Login", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white')
admin_login_btn.place(x = 150, y = 250, width = 200)
admin_login_img = tk.Button(welcome_page_fm, image = admin_login_icon, bd = 0)
admin_login_img.place(x = 60, y = 225)

add_student_btn = tk.Button(welcome_page_fm, text = "Sign Up", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white')
add_student_btn.place(x = 150, y = 375, width = 200)
add_student_img = tk.Button(welcome_page_fm, image = add_student_icon, bd = 0)
add_student_img.place(x = 60, y = 350)

help_btn = tk.Button(welcome_page_fm, text = "?", font = ('bold', 10, 'italic'), fg = bg_color)
help_btn.place(x = 370, y = 445, height = 25, width = 25)

welcome_page_fm.pack(pady = 30)
welcome_page_fm.pack_propagate(False)
welcome_page_fm.configure(width = 400, height = 475)

root.mainloop()