import tkinter as tk # type: ignore
from tkinter.ttk import Combobox # type: ignore

root = tk.Tk()
root.geometry('500x600')
root.title("Student Registration and Management System")
root.resizable(False, False)
root.iconbitmap('icons/silly_cat.ico')
footer_lb = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_lb.pack(side = 'bottom')

bg_color = '#273b7a'
add_student_pic_icon = tk.PhotoImage(file = 'icons/add_img.png')
locked_icon = tk.PhotoImage(file = 'icons/locked_img.png')
unlocked_icon = tk.PhotoImage(file = 'icons/unlocked_img.png')

student_gender = tk.StringVar()
branch_list = ['BAI', 'BAS', 'BBA', 'BCE', 'BCG', 'BCY', 'BEC', 'BET', 'BEY', 'BHI', 'BME', 'BMR', 'BOE', 'BSA', 'MBA', 'MCA', 'MEI', 'MIM', 'MIP', 'MSI']

def show_hide_password():
        if account_password_ent['show'] == "*":
            account_password_ent.config(show = '')
            show_hide_btn.config(image = unlocked_icon)
        else:
            account_password_ent.config(show = "*")
            show_hide_btn.config(image = locked_icon)

add_account_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground = bg_color, highlightthickness = 2)

add_pic_btn = tk.Button(add_pic_section_fm, image = add_student_pic_icon)
add_pic_btn.pack()
add_pic_section_fm.place(x = 5, y = 5, width = 105, height = 105)
pic_info_lb = tk.Label(add_account_page_fm, text = "Click on the icon\nto upload your\nprofile picture.", justify = tk.LEFT)
pic_info_lb.place(x = 115, y = 30)

student_id_lb = tk.Label(add_account_page_fm, text = "Student ID Number:", font = ('bold', 12))
student_id_lb.place(x = 240, y = 20)
student_id = tk.Entry(add_account_page_fm, font = ('bold', 18), bd = 0)
student_id.place(x = 380, y = 19, width = 80)
student_id.insert(tk.END, 'xxxxxx')
student_id.config(state = 'readonly')
id_info_lb = tk.Label(add_account_page_fm, text = "Note: Students will use their auto\ngenerated ID number to log in\nto their accounts.", justify = tk.LEFT)
id_info_lb.place(x = 240, y = 50)

student_name_lb = tk.Label(add_account_page_fm, text = "Student Full Name:", font = ('bold', 12))
student_name_lb.place(x = 5, y = 130)
student_name_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
student_name_ent.place(x = 5, y = 160, width = 190)

student_gender_lb = tk.Label(add_account_page_fm, text = "Student Gender:", font = ('bold', 12))
student_gender_lb.place(x = 5, y = 210)
male_gender_btn = tk.Radiobutton(add_account_page_fm, text = "Male", font = ('bold', 12), variable = student_gender, value = "Male")
male_gender_btn.place(x = 5, y = 235)
female_gender_btn = tk.Radiobutton(add_account_page_fm, text = "Female", font = ('bold', 12), variable = student_gender, value = "Female")
female_gender_btn.place(x = 65, y = 235)
others_gender_btn = tk.Radiobutton(add_account_page_fm, text = "Others", font = ('bold', 12), variable = student_gender, value = "Others")
others_gender_btn.place(x = 5, y = 260)
student_gender.set("Male")

student_age_lb = tk.Label(add_account_page_fm, text = "Student Age:", font = ('bold', 12))
student_age_lb.place(x = 5, y = 295)
student_age_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
student_age_ent.place(x = 5, y = 325, width = 190)

student_branch_lb = tk.Label(add_account_page_fm, text = "Student Branch:", font = ('bold', 12))
student_branch_lb.place(x = 5, y = 380)
select_branch_btn = Combobox(add_account_page_fm, font = ('bold', 15), state = 'readonly', values = branch_list)
select_branch_btn.place(x = 5, y = 410, width = 190, height = 30)

student_contact_lb = tk.Label(add_account_page_fm, text = "Student Contact:", font = ('bold', 12))
student_contact_lb.place(x = 5, y = 465)
student_contact_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
student_contact_ent.place(x = 5, y = 495, width = 190)

student_email_lb = tk.Label(add_account_page_fm, text = "Student Email:", font = ('bold', 12))
student_email_lb.place(x = 240, y = 130)
student_email_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
student_email_ent.place(x = 240, y = 160, width = 190)
email_info_lb = tk.Label(add_account_page_fm, text = "Students can recover their account\nvia email. All communications,\nincluding password recovery,\nwill be through email only.", justify = tk.LEFT)
email_info_lb.place(x = 240, y = 200)

account_password_lb = tk.Label(add_account_page_fm, text = "Create Account Password:", font = ('bold', 12))
account_password_lb.place(x = 240, y = 295)
account_password_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, show = "*")
account_password_ent.place(x = 240, y = 325, width = 190)
show_hide_btn = tk.Button(add_account_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
show_hide_btn.place(x = 430, y = 318)
account_password_info_lb_a = tk.Label(add_account_page_fm, text = "Password Requirements:\n• 8-15 characters.\n• Must include uppercase, lowercase,\n   a number, and a special character.", justify = tk.LEFT)
account_password_info_lb_a.place(x = 240, y = 365)
account_password_info_lb_b = tk.Label(add_account_page_fm, text = "Students will use their ID number\nand created password to log in.", justify = tk.LEFT)
account_password_info_lb_b.place(x = 240, y = 435)

home_btn = tk.Button(add_account_page_fm, text = "Home", font = ('bold', 15), bd = 0, bg = 'red', fg = 'white')
home_btn.place(x = 250, y = 492, width = 80, height = 35)
submit_btn = tk.Button(add_account_page_fm, text = "Submit", font = ('bold', 15), bd = 0, bg = 'green', fg = 'white')
submit_btn.place(x = 350, y = 492, width = 80, height = 35)

add_account_page_fm.pack(pady = 5)
add_account_page_fm.pack_propagate(False)
add_account_page_fm.configure(width = 480, height = 580)

root.mainloop()