# Student Registration and Management System
> A Tkinter + Python based project, created as part of my learning journey.

## Description
This application provides a GUI-based student registration and management system using **Python’s Tkinter library**.  
It supports secure student and admin logins, full records management, and automatic generation of student ID cards (with save/print capability).  
Data is stored locally in an SQLite database, and users can recover passwords via email.

## Features
- Admin and Student login interfaces
- Add, edit, and delete student records
- Student ID card generator (save or print)
- Password recovery via registered email
- All logic/data storage runs locally
- GUI engineered with Tkinter for learning clarity

## Technologies Used
- Python 3.x
- Tkinter
- SQLite3 (database)
- Pillow (image processing)
- smtplib (email sending for password recovery)

## Project Structure (Required Files Only)
```
student-management-system/
├── srms_project.py # Main standalone application file
├── admin_data.py # Configuration, DB paths, & default admin creds
├── icons/ # Icon and image assets for the GUI
├── temp_data/ # SQLite database & temporary images
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```
*Any additional `.py` files are optional, for learning only — not required for using the app.*

## Installation & Usage
1. **Clone this repository:**
```
git clone https://github.com/mahesh-kakde/student-management-system.git
cd student-management-system
```
2. **Install dependencies:**
```
pip install -r requirements.txt
```
3. **Set up email configuration:**

Open `admin_data.py` and set:
```
my_email = 'email_here'
my_password = 'password_here'
```
For Gmail, you must use an App Password (https://myaccount.google.com/apppasswords).  
For other providers, use your account password or an app password as required.

4. **Run the application:**
```
python srms_project.py
```
**Important:**
- Make sure the `icons/` and `temp_data/` folders are present in the main directory before running.
- For admin login, use:
    - Username: `admin`
    - Password: `admin`

## License
This project is licensed under the MIT License. See `LICENSE` for details.

## Author
Mahesh Kakde  
[LinkedIn](https://linkedin.com/in/mahesh-kakde)  
[GitHub](https://github.com/mahesh-kakde)