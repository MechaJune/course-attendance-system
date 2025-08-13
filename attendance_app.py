from flask import Flask, request, render_template_string
from datetime import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials

app = Flask(__name__)

# Google API setup
SCOPE = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
CREDS_FILE = "credentials.json"  # Your Google API credentials file
credentials = ServiceAccountCredentials.from_json_keyfile_name(CREDS_FILE, SCOPE)
gc = gspread.authorize(credentials)

# Name of your existing Google Sheet
SHEET_NAME = "Course Attendance"  # <-- Must match exactly
worksheet = gc.open(SHEET_NAME).sheet1  # Open the first worksheet

# Set header row if sheet is empty
if not worksheet.get_all_values():
    worksheet.append_row(["Date", "Course", "Student ID", "Name"])

# HTML form for students
form_html = """
<!doctype html>
<title>Course Attendance</title>
<h2>Enter your attendance</h2>
<form method="POST">
    <label>Course Name: <input type="text" name="course_name" required></label><br><br>
    <label>3-digit ID: <input type="text" name="student_id" maxlength="3" required></label><br><br>
    <label>Name: <input type="text" name="name" required></label><br><br>
    <input type="submit" value="Submit">
</form>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        course_name = request.form["course_name"].strip()
        student_id = request.form["student_id"].strip()
        name = request.form["name"].strip()
        date = datetime.now().strftime("%Y-%m-%d")
        
        # Append to Google Sheet
        worksheet.append_row([date, course_name, student_id, name])
        
        return "<h3>Attendance recorded for {} in {}. You can close this page.</h3>".format(name, course_name)
    return render_template_string(form_html)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
