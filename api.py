from flask import Flask, jsonify, request
import PyPDF2
from email.message import EmailMessage
import ssl
import smtplib
from os import environ

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 16 * (1024*1024) #megabytes
sender_email = environ.get("SENDER")
password = environ.get("PASS")
with open('README.md', 'r') as file: readme = file.read()

@app.route('/', methods=['GET'])
def home():
    return jsonify({'readme': readme})

@app.route('/upload', methods=['POST'])
def upload():
    if not request.files.get('file', None): return jsonify({'success': False, 'error': 'Missing file field'}), 400
    file = request.files['file']
    if (file.filename.rsplit('.', 1)[1].lower() != "pdf"): return jsonify({'success': False, 'error': 'File is not .pdf'}), 400
    to = request.form.get("email")
    if not to: return jsonify({'success': False, 'error': 'Missing email field'}), 400
    
    title = "Here is a preview of the file: \n\n"
    body = title + extract_pdf_30(file)
    
    send_email(body, to)
    return jsonify({'success': True, 'message': f"The email has been successfully sent to {to}", 'debug': body})


def extract_pdf_30(file):
    pdf_reader = PyPDF2.PdfReader(file)
    my_lines = []

    for page_num in range(len(pdf_reader.pages)):
        if len(my_lines) >= 30:
            break
        
        page = pdf_reader.pages[page_num]
        text = page.extract_text()
        text = text.split("\n")
        my_lines.extend(text)
    
    preview = "\n".join(my_lines[:30])
    return preview

def send_email(body, to):
    em = EmailMessage()
    em['From'] = sender_email
    em['To'] = to
    em['Subject'] = '[Not spam] Check out my new PDF'
    em.set_content(body)
    
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(em['From'], password)
        smtp.sendmail(em['From'], em['To'], em.as_string())

if __name__ == '__main__':
    app.run()#debug=True)