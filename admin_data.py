import sys # type: ignore
import os # type: ignore

def resource_path(relative_path):
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

branches = ['BAI', 'BAS', 'BBA', 'BCE', 'BCG',
            'BCY', 'BEC', 'BET', 'BEY', 'BHI',
            'BME', 'BMR', 'BOE', 'BSA', 'MBA',
            'MCA', 'MEI', 'MIM', 'MIP', 'MSI']

# === EMAIL CONFIGURATION ===
# Enter your email address and password/app password below.

# For Gmail: You MUST enable 2-Step Verification and generate an App Password
#   - (https://myaccount.google.com/apppasswords) — your normal Gmail password will not work.
# For other email providers:
#   - Many also require an app-specific password if 2FA is enabled.
#   - Some may still allow your normal account password, but using an app password is safer.
my_email = 'email_here'
my_password = 'password_here'

admin_username = 'admin'
admin_password = 'admin'
admin_name = 'Mahesh Kakde'

root_icon_path = resource_path('icons/silly_cat.ico')
student_login_icon_path = resource_path('icons/login_student_img.png')
admin_login_icon_path = resource_path('icons/admin_img.png')
add_student_icon_path = resource_path('icons/add_student_img.png')
locked_icon_path = resource_path('icons/locked_img.png')
unlocked_icon_path = resource_path('icons/unlocked_img.png')
add_student_pic_icon_path = resource_path('icons/add_img.png')
student_card_frame_path = resource_path('icons/student_card_frame_img.png')
temp_pic = resource_path('temp_data/temp_pic.png')
db_path = resource_path('temp_data/srms_database.db')