# technical-test
### RESTful API with the following functionalities:
- Receives a PDF file.
- Extracts the first 30 lines of the PDF.
- Sends an email with the extracted content to the provided email address.

## Installation
- `pip install Flask`
- `pip install PyPDF2`

## Obtaining Gmail credentials
- Enable Two-factor authentication in [myaccount.google.com/security](myaccount.google.com/security)
- Generate a new password for the app in [myaccount.google.com/apppasswords](myaccount.google.com/apppasswords)

## Running the server
- Configure the sender email and password with `SENDER` and `PASS` environment variables, using `set` or `export` in your terminal.
- Run with `python api.py`

## Performing the request

### Example request:
```
http
POST /upload
Content-Type: multipart/form-data

{
    "file": <pdf-file>,
    "email": "example@example.com"
}
```

### cURL command:
- `curl -X POST http://localhost:5000/upload -F file=@example.pdf -F "email=example@example.com"`