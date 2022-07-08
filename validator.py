import gspread
from datetime import date

def validate(code):

    row = 1

    token = gspread.service_account(filename="/home/Lionizer/mysite/tok.json")
    sheet = token.open("Free Trial Codes")
    wrk_sheet = sheet.worksheet("Sheet1")

    for i in wrk_sheet.col_values(1):
        if i == code:
            name = wrk_sheet.cell(row, 2).value
            phone = wrk_sheet.cell(row, 3).value
            email = wrk_sheet.cell(row, 4).value
            visit = int(wrk_sheet.cell(row, 5).value)
            if visit < 3:
                today = date.today()
                wrk_sheet.update_cell(row, 5, visit + 1)
                wrk_sheet.update_cell(row, 7 + visit, str(today))
                return True, True, "WELCOME", name, f"Number Of Visits: {str(int(visit) + 1)}"
            return True, False, "Out Of Passes"
        row += 1

    return False, "User Not Found"
