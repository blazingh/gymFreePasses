import gspread
from datetime import date


def append_user(barcode, name, phone):

    row_value = 1
    today = str(date.today())

    st = []

    try:
        #connectimg to gspread
        token = gspread.service_account(filename="/home/Lionizer/mysite/tok.json")
        sheet = token.open("Free Trial Codes")
        wrk_sheet = sheet.worksheet("Sheet1")

        st.append("connected to gspread")

        #checking if user already exists and getting the last barcode used
        for i in wrk_sheet.col_values(1):
            if i == barcode:
                return "exists"
            row_value += 1

        st.append("validated")

        #generating the barcode adn adding the user to the sheet
        wrk_sheet.update_cell(row_value, 1, barcode)
        wrk_sheet.update_cell(row_value, 2, name)
        wrk_sheet.update_cell(row_value, 3, phone)
        wrk_sheet.update_cell(row_value, 5, 0)# visit count
        wrk_sheet.update_cell(row_value, 6, today)

    except: return "error"

    return "append"
