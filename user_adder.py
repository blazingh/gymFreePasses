import gspread
import re
from barcode.writer import ImageWriter
from barcode import ITF
from PIL import Image
from email.message import EmailMessage
import smtplib
from datetime import date
import os


def phone_valid(phone):
    if phone.isdecimal():
        if phone[0] == "0":
            if len(phone) != 10:
                return False
            return True
        if phone[0] == "5":
            if len(phone) != 9:
                return False
            return True
    return False


def email_valid(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    if(re.fullmatch(regex, email)):
        return True
    return False


def gen_barcode(barcode):
    generated_code = ITF(str(barcode),  writer=ImageWriter())
    generated_code.save('barcode')

    img = Image.open("barcode.png")
    img = img.convert("RGBA")
    datas = img.getdata()
    newData = []
    for item in datas:
        if item[0] == 255 and item[1] == 255 and item[2] == 255:
            newData.append((255, 255, 255, 0))
        else:
            newData.append(item)
    img.putdata(newData)
    img.save("barcode.png", "PNG")

    return str(generated_code)


def send_mail(name, email):

    username1 = os.environ["Email"]
    password1 = os.environ["Password"]

    subject = name + "'s 3 DAYS PASS"
    html = f"""
<!DOCTYPE html>
<html><body>
<div>you only know part of the truth</div>
<div style="background-image: url('https://i.ibb.co/pPrMVKX/cards-back.png'); background-repeat: no-repeat; background-size: cover; width: 100vw; height:180vw; max-width: 300px; max-height: 540px;">
<img src="cid:none" style="width: 100%; height: 20%; padding-top: 143%;"></div>
</body></html>
    """
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(username1, password1)
    msg = EmailMessage()
    msg["From"] = "Lionizer CF"
    msg["To"] = email
    msg["Subject"] = subject
    msg.set_content("submition")
    msg.add_alternative(html, subtype="html")

    with open("barcode.png", "rb") as f:
        file_data = f.read()

    msg.add_attachment(file_data, maintype="image",
                       subtype="png", filename=name, cid="<none>")

    try:
        server.send_message(msg)
        print("A Mail has been sent to " + name)

    except:
        return "error"

    server.quit

    return True


def user_pass(name, phone, email):

    if not phone_valid(phone):
        return "phone"
    if not email_valid(email):
        return "email"

    st = []
    row_value = 1
    base_barcode = 100700
    name = name.title()
    today = str(date.today())

    if phone[0] == 0:
        phone = phone[1:]

    try:
        # connectimg to gspread
        token = gspread.service_account(
            filename="/home/Lionizer/mysite/tok.json")
        sheet = token.open("Free Trial Codes")
        wrk_sheet = sheet.worksheet("Sheet1")

        st.append("connected to gspread")

        # checking if user already exists and getting the last barcode used
        for i in wrk_sheet.col_values(4):
            if i == email:
                return "exists"
        for i in wrk_sheet.col_values(3):
            if i == phone:
                return "exists"
            row_value += 1

        st.append("fetched last code")

        # generating the barcode adn adding the user to the sheet
        wrk_sheet.update_cell(
            row_value, 1, gen_barcode(base_barcode + row_value))
        wrk_sheet.update_cell(row_value, 2, name)
        wrk_sheet.update_cell(row_value, 3, phone)
        wrk_sheet.update_cell(row_value, 4, email)
        wrk_sheet.update_cell(row_value, 5, 0)  # visit count
        wrk_sheet.update_cell(row_value, 6, today)

    except:
        return "error"

    if send_mail(name, email):
        return "done"

    return "error"
