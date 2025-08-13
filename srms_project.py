import tkinter as tk # type: ignore
from PIL import Image, ImageTk, ImageDraw, ImageFont, ImageOps # type: ignore
from tkinter.filedialog import askopenfilename, askdirectory # type: ignore
from email.mime.multipart import MIMEMultipart # type: ignore
from tkinter.scrolledtext import ScrolledText # type: ignore
from tkinter.ttk import Combobox, Treeview # type: ignore
from email.mime.text import MIMEText # type: ignore
from io import BytesIO # type: ignore
import threading # type: ignore
import win32api # type: ignore
import smtplib # type: ignore
import sqlite3 # type: ignore
import random # type: ignore
import sys # type: ignore
import os # type: ignore
import re # type: ignore
import admin_data # type: ignore

root = tk.Tk()
root.geometry('500x600')
root.title("Student Registration and Management System")
root.resizable(False, False)
root.iconbitmap(admin_data.root_icon_path)
footer_lb = tk.Label(root, text = "Developed by Mahesh Kakde", font = ('arial', 10, 'italic'))
footer_lb.pack(side = 'bottom')

bg_color = '#273b7a'
student_login_icon = tk.PhotoImage(file = admin_data.student_login_icon_path)
admin_login_icon = tk.PhotoImage(file = admin_data.admin_login_icon_path)
add_student_icon = tk.PhotoImage(file = admin_data.add_student_icon_path)
locked_icon = tk.PhotoImage(file = admin_data.locked_icon_path)
unlocked_icon = tk.PhotoImage(file = admin_data.unlocked_icon_path)
add_student_pic_icon = tk.PhotoImage(file = admin_data.add_student_pic_icon_path)

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

def init_database():
    if not os.path.exists(admin_data.db_path):
        connection = sqlite3.connect(admin_data.db_path)
        cursor = connection.cursor()
        cursor.execute("""
                        CREATE TABLE student_accounts (
                        id_number INT PRIMARY KEY,
                        name VARCHAR(100),
                        gender VARCHAR(6),
                        age INT,
                        branch VARCHAR(3),
                        email VARCHAR(254),
                        contact VARCHAR(20),
                        password VARCHAR(15),
                        image BLOB)
                        """)
        connection.commit()
        connection.close()

def check_duplicate_student_id(id_number):
    connection = sqlite3.connect(admin_data.db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT id_number FROM student_accounts WHERE id_number = ?", (id_number,))
    response = cursor.fetchall()
    connection.close()
    return response

def check_valid_password(id_number, password):
    connection = sqlite3.connect(admin_data.db_path)
    cursor = connection.cursor()
    cursor.execute("SELECT id_number, password FROM student_accounts WHERE id_number = ? AND password = ?", (id_number, password))
    response = cursor.fetchall()
    connection.close()
    return response

def add_data(id_number, name, gender, age, branch, email, contact, password, pic_data):
    connection = sqlite3.connect(admin_data.db_path)
    cursor = connection.cursor()
    cursor.execute("""
                    INSERT INTO student_accounts
                    (id_number, name, gender, age, branch, email, contact, password, image)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (id_number, name, gender, age, branch, email, contact, password, pic_data))
    connection.commit()
    connection.close()

def confirmation_box(message, lines):
    answer = tk.BooleanVar()
    answer.set(False)

    def action(ans):
        answer.set(ans)
        confirmation_box_fm.destroy()

    confirmation_box_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    y_offset = {1: 70, 2: 55, 3: 40}.get(lines, 70)

    message_lb = tk.Label(confirmation_box_fm, text = message, font = ('bold', 15), justify = tk.CENTER)
    message_lb.pack(pady = y_offset)

    cancel_btn = tk.Button(confirmation_box_fm, text = "Cancel", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white', command = lambda: action(False))
    cancel_btn.place(x = 53, y = 160, width = 80, height = 35)
    yes_btn = tk.Button(confirmation_box_fm, text = "Yes", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white', command = lambda: action(True))
    yes_btn.place(x = 187, y = 160, width = 80, height = 35)

    confirmation_box_fm.place(x = 90, y = 90, width = 320, height = 220)

    root.wait_window(confirmation_box_fm)
    return answer.get()

def message_box(message):
    message_box_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    close_btn = tk.Button(message_box_fm, text = "X", font = ('bold', 13), bd = 0, fg = bg_color, command = lambda: message_box_fm.destroy())
    close_btn.place(x = 291, y = 0)

    message_lb = tk.Label(message_box_fm, text = message, font = ('bold', 15), justify = tk.CENTER)
    message_lb.pack(expand = True)

    message_box_fm.place(x = 90, y = 100, width = 320, height = 200)

def draw_student_card(student_pic_path, student_data):
    labels = """
Student ID:
Name:
Gender:
Age:
Branch:
Email:
Contact:
            """

    student_card = Image.open(admin_data.student_card_frame_path)
    pic = Image.open(student_pic_path).resize((100, 100))
    student_card.paste(pic, (15, 25))
    draw = ImageDraw.Draw(student_card)

    heading_font = ImageFont.truetype('bahnschrift', 20)
    labels_font = ImageFont.truetype('arial', 15)
    data_font = ImageFont.truetype('bahnschrift', 13)

    draw.text(xy = (130, 75), text = "Student ID Card", font = heading_font, fill = (0, 0, 0))
    draw.multiline_text(xy = (15, 120), text = labels, font = labels_font, fill = (0, 0, 0), spacing = 6)
    draw.multiline_text(xy = (90, 123), text = student_data, font = data_font, fill = (0, 0, 0), spacing = 9)

    return student_card

def student_card_page(student_card_obj, bypass_login_page = False):

    def save_student_card():
        path = askdirectory()
        if path:
            abs_path = os.path.abspath(path)
            student_card_obj.save(f"{abs_path}/student_card.png")
            print("Student Card image saved at: ", abs_path)

    def print_student_card():
        path = askdirectory()
        if path:
            abs_path = os.path.abspath(path)
            win32api.ShellExecute(0, 'print', f"{abs_path}/student_card.png", None, '.', 0)
            print("Student Card Printed.")

    def close_page():
        student_card_page_fm.destroy()
        if not bypass_login_page:
            root.update()
            student_login_page()

    student_card_img = ImageTk.PhotoImage(student_card_obj)
    student_card_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(student_card_page_fm, text = "Student ID Card", font = ('bold', 18), bg = bg_color, fg = 'white')
    heading_lb.place(x = 0, y = 0, width = 400)

    close_btn = tk.Button(student_card_page_fm, text = "X", font = ('bold', 13), bd = 0, bg = bg_color, fg = 'white', command = close_page)
    close_btn.place(x = 370, y = 0)

    student_card_lb = tk.Label(student_card_page_fm, image = student_card_img)
    student_card_lb.place(x = 50, y = 50)
    student_card_lb.image = student_card_img

    save_student_card_btn = tk.Button(student_card_page_fm, text = "Save ID", font = ('bold', 15), bd = 1, bg = bg_color, fg = 'white', command = save_student_card)
    save_student_card_btn.place(x = 120, y = 381)

    print_student_card_btn = tk.Button(student_card_page_fm, text = "\U0001F5A8", font = ('bold', 18), bd = 1, bg = bg_color, fg = 'white', command = print_student_card)
    print_student_card_btn.place(x = 230, y = 377)

    student_card_page_fm.place(x = 50, y = 30, width = 400, height = 450)

def welcome_page():

    def forward_to_student_page():
        welcome_page_fm.destroy()
        root.update()
        student_login_page()

    def forward_to_admin_page():
        welcome_page_fm.destroy()
        root.update()
        admin_login_page()

    def forward_to_add_account_page():
        welcome_page_fm.destroy()
        root.update()
        add_account_page()

    def forward_to_help_page():
        welcome_page_fm.destroy()
        root.update()
        help_page()

    welcome_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(welcome_page_fm, text = "Student Registration\nand Management System", font = ('bold', 18), bg = bg_color, fg = 'white')
    heading_lb.place(x = 0, y = 0, width = 400)

    student_login_btn = tk.Button(welcome_page_fm, text = "Student Login", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white', command = forward_to_student_page)
    student_login_btn.place(x = 150, y = 125, width = 200)
    student_login_img = tk.Button(welcome_page_fm, image = student_login_icon, bd = 0)
    student_login_img.place(x = 60, y = 100)

    admin_login_btn = tk.Button(welcome_page_fm, text = "Admin Login", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white', command = forward_to_admin_page)
    admin_login_btn.place(x = 150, y = 250, width = 200)
    admin_login_img = tk.Button(welcome_page_fm, image = admin_login_icon, bd = 0)
    admin_login_img.place(x = 60, y = 225)

    add_student_btn = tk.Button(welcome_page_fm, text = "Sign Up", font = ('bold', 15), bd = 0, bg = bg_color, fg = 'white', command = forward_to_add_account_page)
    add_student_btn.place(x = 150, y = 375, width = 200)
    add_student_img = tk.Button(welcome_page_fm, image = add_student_icon, bd = 0)
    add_student_img.place(x = 60, y = 350)

    help_btn = tk.Button(welcome_page_fm, text = "?", font = ('bold', 10, 'italic'), fg = bg_color, command = forward_to_help_page)
    help_btn.place(x = 370, y = 445, height = 25, width = 25)

    welcome_page_fm.pack(pady = 30)
    welcome_page_fm.pack_propagate(False)
    welcome_page_fm.configure(width = 400, height = 475)

def help_page():

    def forward_to_welcome_page():
        help_page_fm.destroy()
        root.update()
        welcome_page()

    help_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(help_page_fm, text = "Help & About", font = ('bold', 18), bg = bg_color, fg = 'white')
    heading_lb.place(x = 0, y = 0, width = 400)

    help_content = (
                    "Thank you for trying out this system!\n\n"
                    "This project is part of my learning journey as I explore\nPython and GUI development using the Tkinter library.\n\n"
                    "It's not a full-fledged commercial project but something\nI'm building alongside my studies to enhance my skills.\n\n"
                    "I truly appreciate any feedback or suggestions you\nmight have. If you encounter any issues or have ideas\nfor improvement, I'd be glad to hear from you!\n\n"
                    "Developer: Mahesh Kakde\n"
                    "Email: mahesh.kakde.165@gmail.com\n\n"
                    "Thanks again for checking it out,\nI hope you find it useful!\n\n"
                    )

    help_text_lb = tk.Label(help_page_fm, text = help_content, font = ('arial', 12), justify = tk.LEFT)
    help_text_lb.place(x = 8, y = 40)

    back_btn = tk.Button(help_page_fm, text = "Home", font = ('bold', 15), bg = bg_color, fg = 'white', command = forward_to_welcome_page)
    back_btn.place(x = 160, y = 410, width = 80, height = 35)

    help_page_fm.pack(pady = 30)
    help_page_fm.pack_propagate(False)
    help_page_fm.configure(width = 400, height = 500)

def send_mail_to_student(email, message, subject):
    smtp_server = 'smtp.gmail.com'
    smtp_port = 587

    username = admin_data.my_email
    password = admin_data.my_password

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = username
    msg['To'] = email
    msg.attach(MIMEText(_text = message, _subtype = 'html'))

    smtp_connection = smtplib.SMTP(host = smtp_server, port = smtp_port)
    smtp_connection.starttls()
    smtp_connection.login(user = username, password = password)
    smtp_connection.sendmail(from_addr = username, to_addrs = email, msg = msg.as_string())
    smtp_connection.quit()

def fetch_student_data(query):
    connection = sqlite3.connect(admin_data.db_path)
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    response = cursor.fetchall()
    connection.close()
    return response

def forgot_password_page():

    def recover_password():

        def send_email_in_background(recovered_email, message):
            send_mail_to_student(email = recovered_email, message = message, subject = "Your Student Account Details and Login Credentials")
            print("Mail Sent Successfully.")

        if check_duplicate_student_id(id_number = student_id_ent.get()):
            print("Success: Valid ID Number.")
            connection = sqlite3.connect(admin_data.db_path)
            cursor = connection.cursor()
            cursor.execute("""SELECT id_number, name, email, password FROM student_accounts WHERE id_number = ?""", (student_id_ent.get(),))
            connection.commit()
            result = cursor.fetchall()
            recovered_id = result[0][0]
            recovered_name = result[0][1]
            recovered_email = result[0][2]
            recovered_password = result[0][3]
            connection.close()
            confirmation = confirmation_box(message = f"Your password will be sent to:\n{recovered_email}\nDo you wish to proceed?", lines = 3)
            if confirmation:
                message = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style>
                                body {{
                                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                    background-color: #f3f4f6;
                                    margin: 0;
                                    padding: 10px;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }}
                                .email-container {{
                                    max-width: 450px;
                                    width: 100%;
                                    background-color: #ffffff;
                                    border-radius: 16px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
                                    border: 1px solid #e0e0e0;
                                }}
                                .header {{
                                    background-color: #0078d4;
                                    color: #ffffff;
                                    padding: 15px;
                                    text-align: center;
                                    border-top-left-radius: 16px;
                                    border-top-right-radius: 16px;
                                }}
                                .header h1 {{
                                    margin: 0;
                                    font-size: 1.4em;
                                }}
                                .content {{
                                    padding: 15px;
                                }}
                                .content h3 {{
                                    color: #444;
                                    margin: 0 0 5px 5px;
                                    font-size: 1.0em;
                                }}
                                .content p {{
                                    color: #444;
                                    font-size: 0.9em;
                                    margin: 0 0 10px 5px;
                                }}
                                .content .description {{
                                    margin-top: 15px;
                                }}
                                .table-container {{
                                    background-color: #f9f9f9;
                                    padding: 15px;
                                    border-radius: 12px;
                                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                                    border: 1px solid #e0e0e0;
                                }}
                                .details-table {{
                                    width: 100%;
                                    border-collapse: collapse;
                                    border-radius: 10px;
                                    overflow: hidden;
                                    background-color: #e0e0e0;
                                    border: 1px solid #dcdcdc;
                                }}
                                .details-table th, .details-table td {{
                                    padding: 8px;
                                    text-align: left;
                                    font-size: 0.85em;
                                }}
                                .details-table th {{
                                    background-color: #f0f0f0;
                                    color: #333;
                                    border-right: 1px solid #dcdcdc;
                                }}
                                .details-table td {{
                                    background-color: #ffffff;
                                    border-top: 1px solid #f0f0f0;
                                    border-left: 1px solid #dcdcdc;
                                }}
                                .details-table td:first-child {{
                                    background-color: #f5f5f5;
                                    font-weight: bold;
                                }}
                                .details-table tr:last-child td {{
                                    border-bottom: none;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 12px;
                                    background-color: #f7f7f7;
                                    color: #888;
                                    font-size: 0.75em;
                                    border-bottom-left-radius: 16px;
                                    border-bottom-right-radius: 16px;
                                    border-top: 1px solid #e0e0e0;
                                }}
                                .footer a {{
                                    color: #0078d4;
                                    text-decoration: none;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>Account Recovery</h1>
                                </div>
                                <div class="content">
                                    <h3>Hello {recovered_name},</h3>
                                    <p>You requested to retrieve your password. Below are your account details:</p>
                                    <div class="description">
                                        <div class="table-container">
                                            <table class="details-table">
                                                <tr><th>Username</th><td>{recovered_id}</td></tr>
                                                <tr><th>Password</th><td>{recovered_password}</td></tr>
                                            </table>
                                        </div>
                                    </div>
                                    <p style="margin-top: 20px; color: red;">Note: Please keep your password safe and secure.</p>
                                </div>
                                <div class="footer">
                                    &copy; Mahesh Kakde
                                </div>
                            </div>
                        </body>
                        </html>
                        """
                email_thread = threading.Thread(target = send_email_in_background, args = (recovered_email, message))
                email_thread.start()
                message_box(message = "Password sent successfully.")
        else:
            print("Error: Invalid ID Number.")
            message_box(message = "Invalid Student ID Number.\nPlease try again.")

    forgot_password_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(forgot_password_page_fm, text = "Password Recovery", font = ('bold', 15), bg = bg_color, fg = 'White')
    heading_lb.place(x = 0 , y = 0 , width = 350)

    close_btn = tk.Button(forgot_password_page_fm, text = "X", font = ('bold', 13), bd = 0, bg = bg_color, fg = 'white', command = lambda: forgot_password_page_fm.destroy())
    close_btn.place(x = 320, y = 0)

    student_id_lb = tk.Label(forgot_password_page_fm, text = "Student ID Number:", font = ('bold', 13))
    student_id_lb.place(x = 70 , y = 40)
    student_id_ent = tk.Entry(forgot_password_page_fm, font = ('bold', 15), justify = tk.CENTER)
    student_id_ent.place(x = 70 , y = 70, width = 180)

    info_lb = tk.Label(forgot_password_page_fm, text = "Note: Your account password will\nbe sent to your registered email\naddress.", justify = tk.LEFT)
    info_lb.place(x = 70 , y = 110)

    next_btn = tk.Button(forgot_password_page_fm, text = "Next", font = ('bold', 13), bg = bg_color, fg = 'white', command = recover_password)
    next_btn.place(x = 130, y = 200, width = 80, height = 35)

    forgot_password_page_fm.place(x = 75, y = 120, width = 350, height = 250)

def student_dashboard(student_id):

    get_student_details = fetch_student_data("""SELECT name, gender, age, branch, email, contact FROM student_accounts WHERE id_number = '%s'""" % student_id)
    get_student_pic = fetch_student_data("""SELECT image FROM student_accounts WHERE id_number = '%s'""" % student_id)
    student_pic = BytesIO(get_student_pic[0][0])

    def logout():
        confirm = confirmation_box(message = "Do you want to Logout?", lines = 1)
        if confirm:
            dashboard_fm.destroy()
            student_login_page()
            root.update()
            message_box("Logged Out Successfully.")

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

    logout_btn = tk.Button(options_fm, text = "Logout", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, command = logout)
    logout_btn.place(x = 4, y = 380)

    def home_page():

        student_pic_img_obj = Image.open(student_pic)
        size = 100
        mask = Image.new(mode = 'L', size = (size, size))
        draw_circle = ImageDraw.Draw(im = mask)
        draw_circle.ellipse(xy = (0, 0, size, size), fill = 255, outline = True)
        output = ImageOps.fit(image = student_pic_img_obj, size = mask.size, centering = (1, 1))
        output.putalpha(mask)
        student_picture = ImageTk.PhotoImage(output)

        home_page_fm = tk.Frame(pages_fm)

        student_pic_lb = tk.Label(home_page_fm, image = student_picture)
        student_pic_lb.image = student_picture
        student_pic_lb.place(x = 10, y = 10)

        hi_lb = tk.Label(home_page_fm, text = f"Welcome, {get_student_details[0][0]}!", font = ('arial', 13))
        hi_lb.place(x = 130, y = 50)

        border = tk.Frame(home_page_fm, highlightbackground = bg_color, highlightthickness = 3)
        border.place(x = 0, y = 130, width = 350, height = 2)

        student_details = f"""
Student ID: {student_id}\n
Name: {get_student_details[0][0]}\n
Gender: {get_student_details[0][1]}\n
Age: {get_student_details[0][2]}\n
Branch: {get_student_details[0][3]}\n
Email: {get_student_details[0][4]}\n
Contact: {get_student_details[0][5]}
                        """

        student_details_lb = tk.Label(home_page_fm, text = student_details, font = ('bold', 13), justify = tk.LEFT)
        student_details_lb.place(x = 15, y = 135)

        home_page_fm.pack(fill = tk.BOTH, expand = True)

    def dashboard_student_card_page():
        student_details = f"""
{student_id}
{get_student_details[0][0]}
{get_student_details[0][1]}
{get_student_details[0][2]}
{get_student_details[0][3]}
{get_student_details[0][4]}
{get_student_details[0][5]}
                        """

        student_card_img_obj = draw_student_card(student_pic_path = student_pic, student_data = student_details)

        def save_student_card():
            path = askdirectory()
            if path:
                print("Student Card image saved at: ", path)
                student_card_img_obj.save(f"{path}/{student_id}.png")

        def print_student_card():
            path = askdirectory()
            if path:
                student_card_img_obj.save(f"{path}/{student_id}.png")
                win32api.ShellExecute(0, 'print', f"{path}/{student_id}.png", None, '.', 0)
                print("Student Card Printed.")

        student_card_img = ImageTk.PhotoImage(student_card_img_obj)
        dashboard_student_card_page_fm = tk.Frame(pages_fm)

        card_lb = tk.Label(dashboard_student_card_page_fm, image = student_card_img)
        card_lb.image = student_card_img
        card_lb.place(x = 20, y = 50)

        save_student_card_btn = tk.Button(dashboard_student_card_page_fm, text = "Save ID", font = ('bold', 15), bd = 1, bg = bg_color, fg = 'white', command = save_student_card)
        save_student_card_btn.place(x = 90, y = 390)

        print_student_card_btn = tk.Button(dashboard_student_card_page_fm, text = "\U0001F5A8", font = ('bold', 18), bd = 1, bg = bg_color, fg = 'white', command = print_student_card)
        print_student_card_btn.place(x = 200, y = 386)

        dashboard_student_card_page_fm.pack(fill = tk.BOTH, expand = True)

    def security_page():

        def show_hide_password():
            if current_password_ent['show'] == "*":
                current_password_ent.config(show = '')
                show_hide_btn.config(image = unlocked_icon)
            else:
                current_password_ent.config(show = "*")
                show_hide_btn.config(image = locked_icon)

        def check_invalid_password(password):
            if not (8 <= len(password) <= 15):
                return False
            if not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[!@#$%^&*()-_=+\[\]{}|;:\'",.<>?/]', password)):
                return False
            return True

        def set_password():
            new_password = new_password_ent.get()
            if new_password != '':
                if not check_invalid_password(new_password):
                    new_password_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                    new_password_ent.focus()
                    message_box(message = "Invalid new password format.")
                    return
                confirm = confirmation_box(message = "Do you want to change\nyour password?", lines = 2)
                if confirm:
                    connection = sqlite3.connect(admin_data.db_path)
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE student_accounts SET password = ? WHERE id_number = ?""", (new_password, student_id))
                    connection.commit()
                    connection.close()
                    print("User Password Updated.")
                    message_box(message = "Password Updated Successfully.")
                    current_password_ent.config(state = tk.NORMAL)
                    current_password_ent.delete(0, tk.END)
                    current_password_ent.insert(0, new_password)
                    current_password_ent.config(state = 'readonly')
                    new_password_ent.delete(0, tk.END)
            else:
                message_box(message = "New password is required.")

        security_page_fm = tk.Frame(pages_fm)

        change_password_lb = tk.Label(security_page_fm, text = "Update Password", font = ('bold', 15), bg = 'red', fg = 'white')
        change_password_lb.place(x = 30, y = 80, width = 290)

        current_password_lb = tk.Label(security_page_fm, text = "Current Password:", font = ('bold', 12))
        current_password_lb.place(x = 45, y = 155)
        current_password_ent = tk.Entry(security_page_fm, font = ('bold', 15), justify = tk.CENTER, show = "*")
        current_password_ent.place(x = 45, y = 190)
        student_current_password = fetch_student_data("""SELECT password FROM student_accounts WHERE id_number = '%s'""" % student_id)
        current_password_ent.insert(tk.END, student_current_password[0][0])
        current_password_ent.config(state = 'readonly')
        show_hide_btn = tk.Button(security_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
        show_hide_btn.place(x = 272, y = 180)

        new_password_lb = tk.Label(security_page_fm, text = "New Password:", font = ('bold', 12))
        new_password_lb.place(x = 45, y = 250)
        new_password_ent = tk.Entry(security_page_fm, font = ('bold', 15), justify = tk.CENTER)
        new_password_ent.place(x = 45, y = 285)

        change_password_btn = tk.Button(security_page_fm, text = "Update", font = ('bold', 13), bg = bg_color, fg = 'white', command = set_password)
        change_password_btn.place(x = 135, y = 375, width = 80, height = 35)

        security_page_fm.pack(fill = tk.BOTH, expand = True)

    def edit_data_page():
        edit_data_page_fm = tk.Frame(pages_fm)

        pic_path = tk.StringVar()
        pic_path.set(admin_data.add_student_pic_icon_path)

        def open_pic():
            path = askopenfilename()
            if path:
                img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
                pic_path.set(path)
                add_pic_btn.config(image = img)
                add_pic_btn.image = img

        def remove_highlight_warning(entry):
            if entry['highlightbackground'] != 'gray':
                if entry.get() != '':
                    entry.config(highlightcolor = bg_color, highlightbackground = 'gray')

        def check_invalid_name(name):
            return (2 <= len(name) <= 100) and all(char.isalpha() or char in " -'" for char in name) and \
                name.strip() == name and "  " not in name

        def check_invalid_age(age):
            return age.isdigit() and (int(age) <= 120)

        def check_invalid_email(email):
            if len(email) > 254:
                return False
            try:
                local_part, domain_part = email.split('@')
            except ValueError:
                return False
            if len(local_part) > 64 or len(domain_part) > 253:
                return False
            if len(local_part) == 0:
                return False
            if '.' not in domain_part:
                return False
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            match = re.match(pattern, email)
            return bool(match)

        def check_invalid_contact(contact):
            pattern = r'^\+?[\d]{1,3}[-\s]?(\(?\d+\)?[-\s]?){6,14}$'
            match = re.match(pattern, contact)
            return match

        def check_inputs():
            nonlocal get_student_details, get_student_pic, student_pic
            if student_name_ent.get() == '':
                student_name_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_name_ent.focus()
                message_box(message = "Student Name is required.")
            elif not check_invalid_name(name = student_name_ent.get()):
                student_name_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_name_ent.focus()
                message_box(message = "Enter a valid Student Name.")
            elif student_age_ent.get() == '':
                student_age_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_age_ent.focus()
                message_box(message = "Student Age is required.")
            elif not check_invalid_age(age = student_age_ent.get()):
                student_age_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_age_ent.focus()
                message_box(message = "Enter a valid Student Age.")
            elif student_email_ent.get() == '':
                student_email_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_email_ent.focus()
                message_box(message = "Student Email address\nis required.")
            elif not check_invalid_email(email = student_email_ent.get()):
                student_email_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_email_ent.focus()
                message_box(message = "Enter a valid Student\nEmail address.")
            elif student_contact_ent.get() == '':
                student_contact_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_contact_ent.focus()
                message_box(message = "Student Contact number\nis required.")
            elif not check_invalid_contact(contact = student_contact_ent.get()):
                student_contact_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                student_contact_ent.focus()
                message_box(message = "Enter a valid Student\nContact number.")
            else:
                if pic_path.get() != '':
                    new_student_picture = Image.open(pic_path.get()).resize((100, 100))
                    new_student_picture.save(admin_data.temp_pic)
                    with open(admin_data.temp_pic, 'rb') as read_new_pic:
                        new_picture_binary = read_new_pic.read()
                        read_new_pic.close()

                    connection = sqlite3.connect(admin_data.db_path)
                    cursor = connection.cursor()
                    cursor.execute("""UPDATE student_accounts SET image = ? WHERE id_number = ?""", (new_picture_binary, student_id))
                    connection.commit()
                    connection.close()

                name  = student_name_ent.get()
                age = student_age_ent.get()
                contact_number = student_contact_ent.get()
                email_address = student_email_ent.get()

                connection = sqlite3.connect(admin_data.db_path)
                cursor = connection.cursor()
                cursor.execute("""UPDATE student_accounts SET name = ?, age = ?, email = ?, contact = ? WHERE id_number = ?""", (name, age, email_address, contact_number, student_id))
                connection.commit()
                connection.close()

                get_student_details = fetch_student_data("""SELECT name, gender, age, branch, email, contact FROM student_accounts WHERE id_number = '%s'""" % student_id)
                get_student_pic = fetch_student_data("""SELECT image FROM student_accounts WHERE id_number = '%s'""" % student_id)
                student_pic = BytesIO(get_student_pic[0][0])
                print("User Details Updated.")
                message_box(message = "Data Updated Successfully.")

        student_current_pic = ImageTk.PhotoImage(Image.open(student_pic))

        add_pic_section_fm = tk.Frame(edit_data_page_fm, highlightbackground = bg_color, highlightthickness = 2)
        add_pic_btn = tk.Button(add_pic_section_fm, image = student_current_pic, command = open_pic)
        add_pic_btn.image = student_current_pic
        add_pic_btn.pack()
        add_pic_section_fm.place(x = 3, y = 0, width = 105, height = 105)

        student_name_lb = tk.Label(edit_data_page_fm, text = "Student Full Name:", font = ('bold', 12))
        student_name_lb.place(x = 5, y = 130)
        student_name_ent = tk.Entry(edit_data_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, justify = tk.LEFT)
        student_name_ent.place(x = 5, y = 160, width = 190)
        student_name_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_name_ent))
        student_name_ent.insert(tk.END, get_student_details[0][0])

        student_age_lb = tk.Label(edit_data_page_fm, text = "Student Age:", font = ('bold', 12))
        student_age_lb.place(x = 5, y = 210)
        student_age_ent = tk.Entry(edit_data_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, justify = tk.LEFT)
        student_age_ent.place(x = 5, y = 235, width = 190)
        student_age_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_age_ent))
        student_age_ent.insert(tk.END, get_student_details[0][2])

        student_branch_lb = tk.Label(edit_data_page_fm, text = "Student Branch:", font = ('bold', 12))
        student_branch_lb.place(x = 5, y = 285)
        select_branch_btn = Combobox(edit_data_page_fm, font = ('bold', 15), state = 'readonly', values = branch_list)
        select_branch_btn.place(x = 5, y = 310, width = 190, height = 30)
        select_branch_btn.set(get_student_details[0][3])
        select_branch_btn.config(state = 'disabled')
        select_branch_info_lb = tk.Label(edit_data_page_fm, text = "Note: Contact admin\nfor branch update.", justify = tk.LEFT)
        select_branch_info_lb.place(x = 196, y = 307)

        student_email_lb = tk.Label(edit_data_page_fm, text = "Student Email:", font = ('bold', 12))
        student_email_lb.place(x = 5, y = 360)
        student_email_ent = tk.Entry(edit_data_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, justify = tk.LEFT)
        student_email_ent.place(x = 5, y = 390, width = 190)
        student_email_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_email_ent))
        student_email_ent.insert(tk.END, get_student_details[0][4])

        student_contact_lb = tk.Label(edit_data_page_fm, text = "Student Contact:", font = ('bold', 12))
        student_contact_lb.place(x = 5, y = 440)
        student_contact_ent = tk.Entry(edit_data_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, justify = tk.LEFT)
        student_contact_ent.place(x = 5, y = 470, width = 190)
        student_contact_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_contact_ent))
        student_contact_ent.insert(tk.END, get_student_details[0][5])

        update_data_btn = tk.Button(edit_data_page_fm, text = "Update", font = ('bold', 15), bd = 0, bg = 'green', fg = 'white', command = check_inputs)
        update_data_btn.place(x = 242, y = 467, width = 80)

        edit_data_page_fm.pack(fill = tk.BOTH, expand = True)

    def delete_account_page():

        def confirm_delete_account():
            confirm = confirmation_box(message="Do you want to delete\nyour account?", lines = 2)
            if confirm:
                connection = sqlite3.connect(admin_data.db_path)
                cursor = connection.cursor()
                cursor.execute("""DELETE FROM student_accounts WHERE id_number = ?""", (student_id,))
                connection.commit()
                connection.close()
                dashboard_fm.destroy()
                student_login_page()
                root.update()
                print("User Account Deleted.")
                message_box(message = "Account Deleted Successfully.")

        delete_account_page_fm = tk.Frame(pages_fm)

        delete_account_lb = tk.Label(delete_account_page_fm, text = "Account Termination", font = ('bold', 15), bg = 'red', fg = 'white')
        delete_account_lb.place(x = 30, y = 100, width = 290)
        delete_account_info_lb = tk.Label(delete_account_page_fm, text = "Warning: This action is irreversible.\nOnce deleted, all your data will\nbe permanently removed.", justify = tk.LEFT)
        delete_account_info_lb.place(x = 30, y = 135)
        delete_account_btn = tk.Button(delete_account_page_fm, text = "Delete Account", font = ('bold', 13), bg = 'red', fg = 'white', command = confirm_delete_account)
        delete_account_btn.place(x = 110, y = 220)

        delete_account_page_fm.pack(fill = tk.BOTH, expand = True)

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x = 122, y = 5, width = 350, height = 515)

    home_page()

    dashboard_fm.pack(pady = 5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width = 480, height = 545)

def student_login_page():

    def show_hide_password():
        if password_ent['show'] == "*":
            password_ent.config(show = '')
            show_hide_btn.config(image = unlocked_icon)
        else:
            password_ent.config(show = "*")
            show_hide_btn.config(image = locked_icon)

    def forward_to_welcome_page():
        student_login_page_fm.destroy()
        root.update()
        welcome_page()

    def forward_to_forgot_password_page():
        forgot_password_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'gray':
            if entry.get() != '':
                entry.config(highlightcolor = bg_color, highlightbackground = 'gray')

    def login_account():
        verify_id_number = check_duplicate_student_id(id_number = id_number_ent.get())
        if verify_id_number:
            print("Success: Valid ID Number.")
            verify_password = check_valid_password(id_number = id_number_ent.get(), password = password_ent.get())
            if verify_password:
                id_number = id_number_ent.get()
                print("Success: Correct Password.")
                print("Access Granted: User Verified Successfully.")
                student_login_page_fm.destroy()
                student_dashboard(student_id = id_number)
                root.update()
            else:
                print("Error: Incorrect Password.")
                print("Access Denied: User Verification Failed.")
                password_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                password_ent.focus()
                message_box(message = "Incorrect Password.\nPlease try again.")
        else:
            print("Error: Invalid ID Number.")
            print("Access Denied: User Verification Failed.")
            id_number_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            id_number_ent.focus()
            message_box(message = "Invalid Student ID Number.\nPlease try again.")

    student_login_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(student_login_page_fm, text = "Student Portal Login", font = ('bold', 18), bg = bg_color, fg = 'white')
    heading_lb.place(x = 0, y = 0, width = 400)

    back_btn = tk.Button(student_login_page_fm, text = "←", font = ('bold', 20), bd = 0, fg = bg_color, command = forward_to_welcome_page)
    back_btn.place(x = 5, y = 40)

    student_icon_lb = tk.Label(student_login_page_fm, image = student_login_icon)
    student_icon_lb.place(x = 150, y = 40)

    id_number_lb = tk.Label(student_login_page_fm, text = "Student ID Number:", font = ('bold', 15), fg = bg_color)
    id_number_lb.place(x = 80, y = 150)
    id_number_ent = tk.Entry(student_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
    id_number_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = id_number_ent))
    id_number_ent.place(x = 80, y = 185)

    password_lb = tk.Label(student_login_page_fm, text = "Password:", font = ('bold', 15), fg = bg_color)
    password_lb.place(x = 80, y = 245)
    password_ent = tk.Entry(student_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, show = "*")
    password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = password_ent))
    password_ent.place(x = 80, y = 280)
    show_hide_btn = tk.Button(student_login_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
    show_hide_btn.place(x = 310, y = 273)

    login_btn = tk.Button(student_login_page_fm, text = "Login", font = ('bold', 15), bg = bg_color, fg = 'white', command = login_account)
    login_btn.place(x = 120, y = 340, width = 160, height = 35)

    forget_password_btn = tk.Button(student_login_page_fm, text = "\u26A0\nForgot Password?", bd = 0, fg = bg_color, command = forward_to_forgot_password_page)
    forget_password_btn.place(x = 150, y = 390)

    student_login_page_fm.pack(pady = 30)
    student_login_page_fm.pack_propagate(False)
    student_login_page_fm.configure(width = 400, height = 450)

def admin_dashboard():

    def logout():
        confirm = confirmation_box(message = "Do you want to Logout?", lines = 1)
        if confirm:
            dashboard_fm.destroy()
            admin_login_page()
            root.update()
            message_box("Logged Out Successfully.")

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

    logout_btn = tk.Button(options_fm, text = "Logout", font = ('bold', 15), bd = 0, bg = '#c3c3c3', fg = bg_color, command = logout)
    logout_btn.place(x = 10, y = 236)

    def home_page():
        home_page_fm = tk.Frame(pages_fm)
        admin_icon_lb = tk.Label(home_page_fm, image = admin_login_icon)
        admin_icon_lb.image = admin_login_icon
        admin_icon_lb.place(x = 10, y = 5)

        hi_lb = tk.Label(home_page_fm, text = f"Welcome, {admin_data.admin_name}!", font = ('arial', 12))
        hi_lb.place(x = 120, y = 35)

        border = tk.Frame(home_page_fm, highlightbackground = bg_color, highlightthickness = 3)
        border.place(x = 0, y = 100, width = 350, height = 2)

        branch_list_lb = tk.Label(home_page_fm, text = "Student Count by Branch:", font = ('bold', 15), bg = bg_color, fg = 'white')
        branch_list_lb.place(x = 15, y = 120, width = 315)

        midpoint = len(branch_list) // 2
        students_numbers_left_lb = tk.Label(home_page_fm, text = '', font = ('bold', 12), justify = tk.LEFT)
        students_numbers_left_lb.place(x = 35, y = 160)
        students_numbers_right_lb = tk.Label(home_page_fm, text = '', font = ('bold', 12), justify = tk.LEFT)
        students_numbers_right_lb.place(x = 195, y = 160)
        for i in branch_list[:midpoint]:
            result = fetch_student_data(query = f"""SELECT COUNT (*) FROM student_accounts WHERE branch == '{i}'""")
            students_numbers_left_lb['text'] += f"{i} Branch: {result[0][0]}\n\n"
        for i in branch_list[midpoint:]:
            result = fetch_student_data(query=f"""SELECT COUNT(*) FROM student_accounts WHERE branch = '{i}'""")
            students_numbers_right_lb['text'] += f"{i} Branch: {result[0][0]}\n\n"

        home_page_fm.pack(fill = tk.BOTH, expand = True)

    def find_student_page():

        def find_student():

            found_data  = ''

            if find_by_option_btn.get() == 'ID':
                found_data = fetch_student_data(query = """SELECT id_number, name, gender, branch FROM student_accounts WHERE id_number = '%s'""" % search_input.get())
            elif find_by_option_btn.get() == 'Name':
                found_data = fetch_student_data(query = """SELECT id_number, name, gender, branch FROM student_accounts WHERE name LIKE '%%%s%%'""" % search_input.get())
            elif find_by_option_btn.get() == 'Branch':
                found_data = fetch_student_data(query = """SELECT id_number, name, gender, branch FROM student_accounts WHERE branch = '%s'""" % search_input.get())
            else:
                found_data = fetch_student_data(query = """SELECT id_number, name, gender, branch FROM student_accounts WHERE gender = '%s'""" % search_input.get())     

            if found_data:
                for item in record_table.get_children():
                    record_table.delete(item)
                for details in found_data:
                    record_table.insert(parent = '', index = 'end', values = details)
            else:
                for item in record_table.get_children():
                    record_table.delete(item)

        def generate_student_card():
            selection = record_table.selection()
            selection_id = record_table.item(item = selection, option = 'values')[0]
            get_student_details = fetch_student_data("""SELECT name, gender, age, branch, email, contact FROM student_accounts WHERE id_number = '%s'""" % selection_id)

            get_student_pic = fetch_student_data("""SELECT image FROM student_accounts WHERE id_number = '%s'""" % selection_id)
            student_pic = BytesIO(get_student_pic[0][0])

            student_details = f"""
  {selection_id}
  {get_student_details[0][0]}
  {get_student_details[0][1]}
  {get_student_details[0][2]}
  {get_student_details[0][3]}
  {get_student_details[0][4]}
  {get_student_details[0][5]}
                        """

            student_card_img_obj = draw_student_card(student_pic_path = student_pic, student_data = student_details)
            student_card_page(student_card_obj = student_card_img_obj, bypass_login_page = True)

        def clear_result():
            find_by_option_btn.set('ID')
            search_input.delete(0, tk.END)
            for item in record_table.get_children():
                record_table.delete(item)
            generate_student_card_btn.config(state = tk.DISABLED)

        find_student_page_fm = tk.Frame(pages_fm)

        search_filters = ['ID', 'Name', 'Branch', 'Gender']

        find_student_page_fm = tk.Frame(pages_fm)
        find_student_record_lb = tk.Label(find_student_page_fm, text = "Search Student Records", font = ('bold', 13), bg = bg_color, fg = 'white')
        find_student_record_lb.place(x = 20, y = 10, width = 300)
        find_student_page_fm.pack(fill = tk.BOTH, expand = True)

        find_by_lb = tk.Label(find_student_page_fm, text = "Search By:", font = ('bold', 12))
        find_by_lb.place(x = 15, y = 50)
        find_by_option_btn = Combobox(find_student_page_fm, font = ('bold', 12), state = 'readonly', values = search_filters)
        find_by_option_btn.place(x = 100, y = 50, width = 80)
        find_by_option_btn.set('ID')

        search_input = tk.Entry(find_student_page_fm, font = ('bold', 12))
        search_input.place(x = 20, y = 90)
        search_input.bind('<KeyRelease>', lambda e: find_student())
        search_input_lb = tk.Label(find_student_page_fm, text = "Note: Case sensitive.", justify = tk.LEFT)
        search_input_lb.place(x = 210, y = 90)

        record_table_lb = tk.Label(find_student_page_fm, text = "Search Results", font = ('bold', 13), fg = 'white', bg = bg_color)
        record_table_lb.place(x = 20, y = 160, width = 300)

        record_table = Treeview(find_student_page_fm)
        record_table.place(x = 0, y = 200, width = 350)
        record_table.bind('<<TreeviewSelect>>', lambda e: generate_student_card_btn.config(state = tk.NORMAL))

        record_table['columns'] = ("ID", "Name",  "Gender", "Branch")

        record_table.column('#0', stretch = tk.NO, width = 0)
        record_table.heading('ID', text = "ID Number", anchor = tk.W)
        record_table.column('ID', width = 50, anchor = tk.W)
        record_table.heading('Name', text = "Name", anchor = tk.W)
        record_table.column('Name', width = 90, anchor = tk.W)
        record_table.heading('Gender', text = "Gender", anchor = tk.W)
        record_table.column('Gender', width = 40, anchor = tk.W)
        record_table.heading('Branch', text = "Branch", anchor = tk.W)
        record_table.column('Branch', width = 40, anchor = tk.W)

        generate_student_card_btn = tk.Button(find_student_page_fm, text = "Generate ID Card", font = ('bold', 13), bg = bg_color, fg = 'white', state = tk.DISABLED, command = generate_student_card)
        generate_student_card_btn.place(x = 195, y = 450)
        clear_btn = tk.Button(find_student_page_fm, text = "Clear Search", font = ('bold', 13), bg = bg_color, fg = 'white', command = clear_result)
        clear_btn.place(x = 10, y = 450)

        find_student_page_fm.pack(fill = tk.BOTH, expand = True)

    def announcements_page():
        selected_branches = []

        def add_branch(name):
            if selected_branches.count(name):
                selected_branches.remove(name)
            else:
                selected_branches.append(name)

        def toggle_all_branches():
            state = master_var.get()
            for branch, var in branch_vars.items():
                var.set(state)
                if state == 1 and branch not in selected_branches:
                    selected_branches.append(branch)
                elif state == 0 and branch in selected_branches:
                    selected_branches.remove(branch)

        def check_input_validation():
            if not announcement_subject.get().strip():
                announcement_subject.focus()
                message_box(message = "Please enter the\nannouncement subject.")
                return
            if not announcement_message.get("1.0", tk.END).strip():
                announcement_message.focus()
                message_box(message = "Please enter the\nannouncement message.")
                return
            if not selected_branches:
                message_box(message = "Please select at least one\nbranch to proceed.")
                return
            collect_emails()

        def collect_emails():
            fetched_emails = []
            for _branch in selected_branches:
                emails = fetch_student_data(f"""SELECT email FROM student_accounts WHERE branch == '{_branch}'""")
                for email_address in emails:
                    fetched_emails.append(*email_address)
            thread = threading.Thread(target = send_announcement, args = [fetched_emails])
            thread.start()

        def send_announcement(email_addresses):
            box_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)
            heading_lb = tk.Label(box_fm, text = "Sending Email", font = ('bold', 15), bg = bg_color, fg = 'white')
            heading_lb.place(x = 0, y = 0, width = 300)
            sending_lb = tk.Label(box_fm, font = ('bold', 12), justify = tk.LEFT)
            sending_lb.pack(pady = 50)
            box_fm.place(x = 110, y = 110, width = 300, height = 200)

            message = f"""<!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style>
                                body {{
                                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                    background-color: #f3f4f6;
                                    margin: 0;
                                    padding: 10px;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }}
                                .email-container {{
                                    max-width: 450px;
                                    width: 100%;
                                    background-color: #ffffff;
                                    border-radius: 16px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
                                    border: 1px solid #e0e0e0;
                                }}
                                .header {{
                                    background-color: #0078d4;
                                    color: #ffffff;
                                    padding: 15px;
                                    text-align: center;
                                    border-top-left-radius: 16px;
                                    border-top-right-radius: 16px;
                                }}
                                .header h1 {{
                                    margin: 0;
                                    font-size: 1.4em;
                                }}
                                .content {{
                                    padding: 15px;
                                }}
                                .content h3 {{
                                    color: #444;
                                    margin: 0 0 5px 5px;
                                    font-size: 1.0em;
                                }}
                                .content p {{
                                    color: #444;
                                    font-size: 0.9em;
                                    margin: 0 0 10px 5px;
                                }}
                                .content .description {{
                                    margin-top: 15px;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 12px;
                                    background-color: #f7f7f7;
                                    color: #888;
                                    font-size: 0.75em;
                                    border-bottom-left-radius: 16px;
                                    border-bottom-right-radius: 16px;
                                    border-top: 1px solid #e0e0e0;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>{announcement_subject.get()}</h1>
                                </div>
                                <div class="content">
                                    <p>{announcement_message.get('1.0', tk.END).replace('\n', '<br>')}</p>
                                </div>
                                <div class="footer">
                                    &copy; Mahesh Kakde
                                </div>
                            </div>
                        </body>
                        </html>
                        """
            sent_count = 1

            for email in email_addresses:
                sending_lb.config(text = f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")
                send_mail_to_student(email = email, subject = "Important Announcement Students", message = message)
                sent_count += 1
                sending_lb.config(text = f"Sending To:\n{email}\n\n{sent_count}/{len(email_addresses)}")
            box_fm.destroy()
            print("Mail Sent Successfully.")
            message_box(message = "Announcement Sent Successfully.")

        announcements_page_fm = tk.Frame(pages_fm)

        subject_lb = tk.Label(announcements_page_fm, text = "Announcement Subject:", font = ('bold', 12))
        subject_lb.place(x = 10, y = 5)

        announcement_subject = tk.Entry(announcements_page_fm, font = ('bold', 12))
        announcement_subject.place(x = 10, y = 35, width = 210, height = 25)
        announcement_message = ScrolledText(announcements_page_fm, font = ('bold', 12))
        announcement_message.place(x = 10, y = 75, width = 300, height = 200)

        branches_list_lb = tk.Label(announcements_page_fm, text = "Select Branches to Announce:", font = ('bold', 12))
        branches_list_lb.place(x = 10, y = 290)

        branch_vars = {}
        x_positions = [15, 125, 235]
        y_position = 320

        for index, branch in enumerate(branch_list):
            col = index // 8
            row = index % 8
            x_position = x_positions[col]
            y_pos = y_position + (row * 25)
            var = tk.IntVar()
            branch_vars[branch] = var
            branch_check_btn = tk.Checkbutton(announcements_page_fm, text = f"{branch} Branch", variable = var, command = lambda branch = branch: add_branch(name = branch))
            branch_check_btn.place(x = x_position, y = y_pos)

        master_var = tk.IntVar()
        master_checkbox = tk.Checkbutton(announcements_page_fm, text = "Select All", font = ('bold', 12), variable = master_var, command = toggle_all_branches)
        master_checkbox.place(x = 235, y = 430)

        send_announcement_btn = tk.Button(announcements_page_fm, text = "Send", font = ('bold', 12), bg = bg_color, fg = 'white', command = check_input_validation)
        send_announcement_btn.place(x = 247, y = 480, width = 80)

        announcements_page_fm.pack(fill = tk.BOTH, expand = True)

    pages_fm = tk.Frame(dashboard_fm)
    pages_fm.place(x = 122, y = 5, width = 350, height = 515)

    home_page()

    dashboard_fm.pack(pady = 5)
    dashboard_fm.pack_propagate(False)
    dashboard_fm.configure(width = 480, height = 545)

def admin_login_page():

    def show_hide_password():
        if password_ent['show'] == "*":
            password_ent.config(show = '')
            show_hide_btn.config(image = unlocked_icon)
        else:
            password_ent.config(show = "*")
            show_hide_btn.config(image = locked_icon)

    def forward_to_welcome_page():
        admin_login_page_fm.destroy()
        root.update()
        welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'gray':
            if entry.get() != '':
                entry.config(highlightcolor = bg_color, highlightbackground = 'gray')

    def login_account():
        if username_ent.get() == admin_data.admin_username:
            print("Success: Valid Username.")
            if password_ent.get() == admin_data.admin_password:
                print("Success: Correct Password.")
                print("Access Granted: User Verified Successfully.")
                admin_login_page_fm.destroy()
                root.update()
                admin_dashboard()
            else:
                print("Error: Incorrect Password.")
                print("Access Denied: User Verification Failed.")
                password_ent.config(highlightcolor = 'red', highlightbackground = 'red')
                password_ent.focus()
                message_box(message = "Invalid Password.\nPlease try again.")
        else:
            print("Error: Invalid Username.")
            print("Access Denied: User Verification Failed.")
            username_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            username_ent.focus()
            message_box(message = "Invalid Admin ID.\nPlease try again.")

    admin_login_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    heading_lb = tk.Label(admin_login_page_fm, text = "Admin Portal Login", font = ('bold', 18), bg = bg_color, fg = 'white')
    heading_lb.place(x = 0, y = 0, width = 400)

    back_btn = tk.Button(admin_login_page_fm, text = "←", font = ('bold', 20), bd = 0, fg = bg_color, command = forward_to_welcome_page)
    back_btn.place(x = 5, y = 40)

    admin_icon_lb = tk.Label(admin_login_page_fm, image = admin_login_icon)
    admin_icon_lb.place(x = 150, y = 40)

    username_lb = tk.Label(admin_login_page_fm, text = "Admin ID:", font = ('bold', 15), fg = bg_color)
    username_lb.place(x = 80, y = 150)
    username_ent = tk.Entry(admin_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
    username_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = username_ent))
    username_ent.place(x = 80, y = 185)

    password_lb = tk.Label(admin_login_page_fm, text = "Password:", font = ('bold', 15), fg = bg_color)
    password_lb.place(x = 80, y = 245)
    password_ent = tk.Entry(admin_login_page_fm, font = ('bold', 15), justify = tk.CENTER, highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, show = "*")
    password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = password_ent))
    password_ent.place(x = 80, y = 280)
    show_hide_btn = tk.Button(admin_login_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
    show_hide_btn.place(x = 310, y = 273)

    login_btn = tk.Button(admin_login_page_fm, text = "Login", font = ('bold', 15), bg = bg_color, fg = 'white', command = login_account)
    login_btn.place(x = 120, y = 355, width = 160, height = 35)

    admin_login_page_fm.pack(pady = 30)
    admin_login_page_fm.pack_propagate(False)
    admin_login_page_fm.configure(width = 400, height = 450)

student_gender = tk.StringVar()
branch_list = admin_data.branches

def add_account_page():

    def show_hide_password():
        if account_password_ent['show'] == "*":
            account_password_ent.config(show = '')
            show_hide_btn.config(image = unlocked_icon)
        else:
            account_password_ent.config(show = "*")
            show_hide_btn.config(image = locked_icon)

    pic_path = tk.StringVar()
    pic_path.set(admin_data.add_student_pic_icon_path)

    def open_pic():
        path = askopenfilename()
        if path:
            img = ImageTk.PhotoImage(Image.open(path).resize((100, 100)))
            pic_path.set(path)
            add_pic_btn.config(image = img)
            add_pic_btn.image = img

    def forward_to_welcome_page():
        ans = confirmation_box(message="Do you want to leave\nRegistration Form?", lines = 2)
        if ans:
            add_account_page_fm.destroy()
            root.update()
            welcome_page()

    def remove_highlight_warning(entry):
        if entry['highlightbackground'] != 'gray':
            if entry.get() != '':
                entry.config(highlightcolor = bg_color, highlightbackground = 'gray')

    def check_invalid_name(name):
        return (2 <= len(name) <= 100) and all(char.isalpha() or char in " -'" for char in name) and \
            name.strip() == name and "  " not in name

    def check_invalid_age(age):
        return age.isdigit() and (int(age) <= 120)
    
    def check_invalid_email(email):
        if len(email) > 254:
            return False
        try:
            local_part, domain_part = email.split('@')
        except ValueError:
            return False
        if len(local_part) > 64 or len(domain_part) > 253:
            return False
        if len(local_part) == 0:
            return False
        if '.' not in domain_part:
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        match = re.match(pattern, email)
        return bool(match)

    def check_invalid_contact(contact):
        pattern = r'^\+?[\d]{1,3}[-\s]?(\(?\d+\)?[-\s]?){6,14}$'
        match = re.match(pattern, contact)
        return match

    def check_invalid_password(password):
        if not (8 <= len(password) <= 15):
            return False
        if not (re.search(r'[A-Z]', password) and re.search(r'[a-z]', password) and re.search(r'[0-9]', password) and re.search(r'[!@#$%^&*()-_=+\[\]{}|;:\'",.<>?/]', password)):
            return False
        return True

    def generate_id_number():
        generated_id = ''
        for r in range(6):
            generated_id += str(random.randint(0, 9))
        if not check_duplicate_student_id(id_number = generated_id):
            student_id.config(state = tk.NORMAL)
            student_id.delete(0, tk.END)
            student_id.insert(tk.END, generated_id)
            student_id.config(state = 'readonly')
        else:
            generate_id_number()

    def send_email_in_background(student_email, message):
        send_mail_to_student(email = student_email, message = message, subject = "Your Student Account Has Been Successfully Created")
        print("Mail Sent Successfully.")

    def check_input_validation():
        if student_name_ent.get() == '':
            student_name_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_name_ent.focus()
            message_box(message = "Student Name is required.")
        elif not check_invalid_name(name = student_name_ent.get()):
            student_name_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_name_ent.focus()
            message_box(message = "Enter a valid Student Name.")
        elif student_age_ent.get() == '':
            student_age_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_age_ent.focus()
            message_box(message = "Student Age is required.")
        elif not check_invalid_age(age = student_age_ent.get()):
            student_age_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_age_ent.focus()
            message_box(message = "Enter a valid Student Age.")
        elif select_branch_btn.get() == '':
            select_branch_btn.focus()
            message_box(message = "Student Branch selection\nis required.")
        elif student_contact_ent.get() == '':
            student_contact_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_contact_ent.focus()
            message_box(message = "Student Contact number\nis required.")
        elif not check_invalid_contact(contact = student_contact_ent.get()):
            student_contact_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_contact_ent.focus()
            message_box(message = "Enter a valid Student\nContact number.")
        elif student_email_ent.get() == '':
            student_email_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_email_ent.focus()
            message_box(message = "Student Email address\nis required.")
        elif not check_invalid_email(email = student_email_ent.get()):
            student_email_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            student_email_ent.focus()
            message_box(message = "Enter a valid Student\nEmail address.")
        elif account_password_ent.get() == '':
            account_password_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            account_password_ent.focus()
            message_box(message = "Please create a Account\nPassword.")
        elif not check_invalid_password(password = account_password_ent.get()):
            account_password_ent.config(highlightcolor = 'red', highlightbackground = 'red')
            account_password_ent.focus()
            message_box(message = "Invalid password format.")
        else:
            pic_data = b''
            if  pic_path.get() != '':
                resize_pic = Image.open(pic_path.get()).resize((100, 100))
                resize_pic.save(admin_data.temp_pic)
                read_data = open(admin_data.temp_pic, 'rb')
                pic_data = read_data.read()
                read_data.close()
            else:
                read_data = open(admin_data.add_student_pic_icon_path, 'rb')
                pic_data = read_data.read()
                read_data.close()
        add_data(id_number = student_id.get(), name = student_name_ent.get(),  gender = student_gender.get(), age = student_age_ent.get(), branch = select_branch_btn.get(), email = student_email_ent.get(), contact = student_contact_ent.get(), password = account_password_ent.get(), pic_data = pic_data)
        data = f"""
{student_id.get()}
{student_name_ent.get()}
{student_gender.get()}
{student_age_ent.get()}
{select_branch_btn.get()}
{student_email_ent.get()}
{student_contact_ent.get()}
                """
        created_account_data = fetch_student_data("""SELECT id_number, name, gender, age, branch, email, contact, password FROM student_accounts WHERE id_number = '%s'""" % student_id.get())
        student_email = created_account_data[0][5]
        message = f"""
                        <!DOCTYPE html>
                        <html lang="en">
                        <head>
                            <meta charset="UTF-8">
                            <meta name="viewport" content="width=device-width, initial-scale=1.0">
                            <style>
                                body {{
                                    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                                    background-color: #f3f4f6;
                                    margin: 0;
                                    padding: 10px;
                                    display: flex;
                                    justify-content: center;
                                    align-items: center;
                                }}
                                .email-container {{
                                    max-width: 450px;
                                    width: 100%;
                                    background-color: #ffffff;
                                    border-radius: 16px;
                                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.08);
                                    border: 1px solid #e0e0e0;
                                }}
                                .header {{
                                    background-color: #0078d4;
                                    color: #ffffff;
                                    padding: 15px;
                                    text-align: center;
                                    border-top-left-radius: 16px;
                                    border-top-right-radius: 16px;
                                }}
                                .header h1 {{
                                    margin: 0;
                                    font-size: 1.4em;
                                }}
                                .content {{
                                    padding: 15px;
                                }}
                                .content h3 {{
                                    color: #444;
                                    margin: 0 0 5px 5px;
                                    font-size: 1.0em;
                                }}
                                .content p {{
                                    color: #444;
                                    font-size: 0.9em;
                                    margin: 0 0 10px 5px;
                                }}
                                .content .description {{
                                    margin-top: 15px;
                                }}
                                .table-container {{
                                    background-color: #f9f9f9;
                                    padding: 15px;
                                    border-radius: 12px;
                                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.05);
                                    border: 1px solid #e0e0e0;
                                }}
                                .details-table {{
                                    width: 100%;
                                    border-collapse: collapse;
                                    border-radius: 10px;
                                    overflow: hidden;
                                    background-color: #e0e0e0;
                                    border: 1px solid #dcdcdc;
                                }}
                                .details-table th, .details-table td {{
                                    padding: 8px;
                                    text-align: left;
                                    font-size: 0.85em;
                                }}
                                .details-table th {{
                                    background-color: #f0f0f0;
                                    color: #333;
                                    border-right: 1px solid #dcdcdc;
                                }}
                                .details-table td {{
                                    background-color: #ffffff;
                                    border-top: 1px solid #f0f0f0;
                                    border-left: 1px solid #dcdcdc;
                                }}
                                .details-table td:first-child {{
                                    background-color: #f5f5f5;
                                    font-weight: bold;
                                }}
                                .details-table tr:last-child td {{
                                    border-bottom: none;
                                }}
                                .footer {{
                                    text-align: center;
                                    padding: 12px;
                                    background-color: #f7f7f7;
                                    color: #888;
                                    font-size: 0.75em;
                                    border-bottom-left-radius: 16px;
                                    border-bottom-right-radius: 16px;
                                    border-top: 1px solid #e0e0e0;
                                }}
                                .footer a {{
                                    color: #0078d4;
                                    text-decoration: none;
                                }}
                            </style>
                        </head>
                        <body>
                            <div class="email-container">
                                <div class="header">
                                    <h1>New Account Created</h1>
                                </div>
                                <div class="content">
                                    <h3>Hello {created_account_data[0][1]},</h3>
                                    <p>Your new account has been successfully created. Here are your account details:</p>
                                    <div class="description">
                                        <div class="table-container">
                                            <table class="details-table">
                                                <tr><th>Student ID</th><td>{created_account_data[0][0]}</td></tr>
                                                <tr><th>Name</th><td>{created_account_data[0][1]}</td></tr>
                                                <tr><th>Gender</th><td>{created_account_data[0][2]}</td></tr>
                                                <tr><th>Age</th><td>{created_account_data[0][3]}</td></tr>
                                                <tr><th>Branch</th><td>{created_account_data[0][4]}</td></tr>
                                                <tr><th>Email</th><td>{created_account_data[0][5]}</td></tr>
                                                <tr><th>Contact</th><td>{created_account_data[0][6]}</td></tr>
                                                <tr><th>Password</th><td>{created_account_data[0][7]}</td></tr>
                                            </table>
                                        </div>
                                    </div>
                                <p style="margin-top: 20px; color: red;">
                                    Note: Please keep your account data safe and secure.<br>
                                    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;Do not share your login details with anyone.
                                </p>
                                </div>
                                <div class="footer">
                                    &copy; Mahesh Kakde
                                </div>
                            </div>
                        </body>
                        </html>
                        """
        email_thread = threading.Thread(target = send_email_in_background, args = (student_email, message))
        email_thread.start()
        get_student_card = draw_student_card(student_pic_path = pic_path.get(), student_data = data)
        student_card_page(student_card_obj = get_student_card)
        message_box("Success! Your Account is Ready.")
        add_account_page_fm.destroy()
        root.update()

    add_account_page_fm = tk.Frame(root, highlightbackground = bg_color, highlightthickness = 3)

    add_pic_section_fm = tk.Frame(add_account_page_fm, highlightbackground = bg_color, highlightthickness = 2)

    add_pic_btn = tk.Button(add_pic_section_fm, image = add_student_pic_icon, command = open_pic)
    add_pic_btn.pack()
    add_pic_section_fm.place(x = 5, y = 5, width = 105, height = 105)
    pic_info_lb = tk.Label(add_account_page_fm, text = "Click on the icon\nto upload your\nprofile picture.", justify = tk.LEFT)
    pic_info_lb.place(x = 115, y = 30)

    student_id_lb = tk.Label(add_account_page_fm, text = "Student ID Number:", font = ('bold', 12))
    student_id_lb.place(x = 240, y = 20)
    student_id = tk.Entry(add_account_page_fm, font = ('bold', 18), bd = 0)
    student_id.place(x = 380, y = 19, width = 80)
    student_id.config(state = 'readonly')
    generate_id_number()
    id_info_lb = tk.Label(add_account_page_fm, text = "Note: Students will use their auto\ngenerated ID number to log in\nto their accounts.", justify = tk.LEFT)
    id_info_lb.place(x = 240, y = 50)

    student_name_lb = tk.Label(add_account_page_fm, text = "Student Full Name:", font = ('bold', 12))
    student_name_lb.place(x = 5, y = 130)
    student_name_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
    student_name_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_name_ent))
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
    student_age_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_age_ent))
    student_age_ent.place(x = 5, y = 325, width = 190)

    student_branch_lb = tk.Label(add_account_page_fm, text = "Student Branch:", font = ('bold', 12))
    student_branch_lb.place(x = 5, y = 380)
    select_branch_btn = Combobox(add_account_page_fm, font = ('bold', 15), state = 'readonly', values = branch_list)
    select_branch_btn.place(x = 5, y = 410, width = 190, height = 30)

    student_contact_lb = tk.Label(add_account_page_fm, text = "Student Contact:", font = ('bold', 12))
    student_contact_lb.place(x = 5, y = 465)
    student_contact_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
    student_contact_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_contact_ent))
    student_contact_ent.place(x = 5, y = 495, width = 190)

    student_email_lb = tk.Label(add_account_page_fm, text = "Student Email:", font = ('bold', 12))
    student_email_lb.place(x = 240, y = 130)
    student_email_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2)
    student_email_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = student_email_ent))
    student_email_ent.place(x = 240, y = 160, width = 190)
    email_info_lb = tk.Label(add_account_page_fm, text = "Students can recover their account\nvia email. All communications,\nincluding password recovery,\nwill be through email only.", justify = tk.LEFT)
    email_info_lb.place(x = 240, y = 200)

    account_password_lb = tk.Label(add_account_page_fm, text = "Create Account Password:", font = ('bold', 12))
    account_password_lb.place(x = 240, y = 295)
    account_password_ent = tk.Entry(add_account_page_fm, font = ('bold', 15), highlightcolor = bg_color, highlightbackground = 'gray', highlightthickness = 2, show = "*")
    account_password_ent.bind('<KeyRelease>', lambda e: remove_highlight_warning(entry = account_password_ent))
    account_password_ent.place(x = 240, y = 325, width = 190)
    show_hide_btn = tk.Button(add_account_page_fm, image = locked_icon, bd = 0, command = show_hide_password)
    show_hide_btn.place(x = 430, y = 318)
    account_password_info_lb_a = tk.Label(add_account_page_fm, text = "Password Requirements:\n• 8-15 characters.\n• Must include uppercase, lowercase,\n   a number, and a special character.", justify = tk.LEFT)
    account_password_info_lb_a.place(x = 240, y = 365)
    account_password_info_lb_b = tk.Label(add_account_page_fm, text = "Students will use their ID number\nand created password to log in.", justify = tk.LEFT)
    account_password_info_lb_b.place(x = 240, y = 435)

    home_btn = tk.Button(add_account_page_fm, text = "Home", font = ('bold', 15), bd = 0, bg = 'red', fg = 'white', command = forward_to_welcome_page)
    home_btn.place(x = 250, y = 492, width = 80, height = 35)
    submit_btn = tk.Button(add_account_page_fm, text = "Submit", font = ('bold', 15), bd = 0, bg = 'green', fg = 'white', command = check_input_validation)
    submit_btn.place(x = 350, y = 492, width = 80, height = 35)

    add_account_page_fm.pack(pady = 5)
    add_account_page_fm.pack_propagate(False)
    add_account_page_fm.configure(width = 480, height = 580)

init_database()
welcome_page()

root.mainloop()