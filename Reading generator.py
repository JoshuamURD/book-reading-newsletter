# Dependencies to extract book pages
import PyPDF2
import ebooklib
from ebooklib import epub

#Dependency for gemeni
import google.generativeai as genai

#Dependencies to send email
import email, smtplib, ssl
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# Managing progress using SQLITE
import sqlite3

def send_email(subject, message, from_addr, to_addr, password, filename):
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    
    body = message
    msg.attach(MIMEText(body, 'plain'))
    
    attachment = open(filename, 'rb')
    part = MIMEBase('application', 'octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition', "attachment; filename= %s" % filename)
    
    msg.attach(part)
    
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login(from_addr, password)
    text = msg.as_string()
    server.sendmail(from_addr, to_addr, text)
    server.quit()
    

def extract_pdf_pages(input_file_path, output_file_path, start_page, end_page):
    """
    Extracts a range of pages from a PDF file and saves them as a new PDF file.

    Args:
        input_file_path (str): The path to the input PDF file.
        output_file_path (str): The path to the output PDF file.
        start_page (int): The first page to extract (1-indexed).
        end_page (int): The last page to extract (1-indexed).
    """
    with open(input_file_path, 'rb') as input_file:
        pdf_reader = PyPDF2.PdfReader(input_file)
        pdf_writer = PyPDF2.PdfWriter()

        for page_num in range(start_page-1, end_page):
            page = pdf_reader.pages[page_num]
            pdf_writer.add_page(page)

        with open(output_file_path, 'wb') as output_file:
            pdf_writer.write(output_file)
         
# A function to read a pdf   
def readPdf(pdf="document.pdf"):
    # Create a PyPDF2 reader object
    pdf_reader = PyPDF2.PdfReader(pdf)

    # Extract the text from the PDF
    text = ""
    for page in range(len(pdf_reader.pages)):
        text += pdf_reader.pages[page].extract_text()

    return text

# a function to generate questions
def generate_questions(text):
    GOOGLE_API_KEY=input("Please input GemininAPI key: ")
    genai.configure(api_key=GOOGLE_API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
    response = model.generate_content("Generate questions for this text: " + text)
    questions = response.text
    return questions


def main():
    #file_path = r"C:\Users\clerk\Downloads\PLT Program Requirements.pdf"
    #output_path= r"C:\Users\clerk\Downloads\test.pdf"
    #start_page=2
    #end_page=3
    #extract_pdf_pages(file_path, output_path, start_page, end_page)
    
    text = readPdf()
    
    subject = "Test Email"
    message = generate_questions(text)
    from_addr = ""
    to_addr = ""
    password = input("input email password: ")
    filename = "document.pdf"
    
    send_email(subject, message, from_addr, to_addr, password, filename)


if __name__ == "__main__":
    main()