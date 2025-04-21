from mailersend import emails
import ast
from dotenv import load_dotenv
import os
import smtplib
from email.message import EmailMessage
import os.path
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import base64
from email.message import EmailMessage
# from auth_gmail import get_gmail_service


load_dotenv()

# mailer = emails.NewEmail(os.getenv('MAILERSEND_API_KEY'))

def enviar_correo_to(function_args):
    text = function_args["text"]
    from_t = function_args["from"]
    contenido = function_args["contenido"]
    subject = function_args["subject"]
    to = function_args["to"]
    # suscribers = ast.literal_eval(to)
    cleaned = to.replace('"', '')
    email_list = [email.strip() for email in cleaned.split(",")]
    service = get_gmail_service()

    for email_receptor in email_list:
        mensaje = EmailMessage()
        mensaje.set_content(contenido)
        mensaje['To'] = email_receptor
        mensaje['From'] = from_t  # Esto se ignora si no está verificado por Gmail
        mensaje['Subject'] = subject

        raw = base64.urlsafe_b64encode(mensaje.as_bytes()).decode()

        try:
            message = service.users().messages().send(
                userId="me",
                body={'raw': raw}
            ).execute()
            print(f"Correo enviado a {email_receptor}. ID: {message['id']}")
        except Exception as e:
            print(f"Error enviando a {email_receptor}: {e}")

    return f"from: {from_t}, to: {to}, content: {contenido}"


# def enviar_correo_to(function_args):
#     text = function_args["text"]
#     from_t = function_args["from"]
#     contenido = function_args["contenido"]
#     subject = function_args["subject"]
#     to = function_args["to"]
#     # suscribers = ast.literal_eval(to)
#     cleaned = to.replace('"', '')
#     email_list = [email.strip() for email in cleaned.split(",")]

#     email_emisor = 'thedovekeeper22@gmail.com'
#     email_contraseña = '130399mcr'

#     for email in email_list:
#         email_receptor = email
#         mensaje = EmailMessage()
#         mensaje['Subject'] = subject
#         mensaje['From'] = email_emisor
#         mensaje['To'] = email_receptor
#         mensaje.set_content(contenido)

#     with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
#         smtp.login(email_emisor, email_contraseña)
#         smtp.send_message(mensaje)

#     return f"from: {from_t}, to: {to}, content: {contenido}"

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def get_gmail_service():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/vivianavera03/Desktop/Bco Guayaquil/ai-agent/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('gmail', 'v1', credentials=creds)

# def enviar_correo_to(function_args):
#     text = function_args["text"]
#     from_t = function_args["from"]
#     contenido = function_args["contenido"]
#     subject = function_args["subject"]
#     to = function_args["to"]
#     # suscribers = ast.literal_eval(to)
#     cleaned = to.replace('"', '')
#     email_list = [email.strip() for email in cleaned.split(",")]

#     mailer = emails.NewEmail()
#     mail_body = {}
#     mail_from = {"name": from_t,"email": from_t}
#     recipients = []
#     for email in email_list:
#         recipients.append({"name": email, "email": email})

#     mailer.set_mail_from(mail_from, mail_body)
#     mailer.set_mail_to(recipients, mail_body)
#     mailer.set_subject(subject, mail_body)
#     mailer.set_plaintext_content(contenido, mail_body)
#     mailer.send(mail_body)
#     return f"from: {from_t}, to: {to}, content: {contenido}"