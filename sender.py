import streamlit as st
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Configuración inicial de la app
st.title("Sender Pro (Mondongo Frio V.1)")

# Configuración del servidor SMTP
st.subheader("Configuración del servidor SMTP")
smtp_server = st.text_input("Servidor SMTP:")
smtp_port = st.number_input("Puerto SMTP (ej. 587):", value=587, step=1)
smtp_user = st.text_input("Usuario SMTP:")
smtp_password = st.text_input("Contraseña SMTP:", type="password")

# Configuración del correo
st.subheader("Información del correo")
sender_email = st.text_input("Correo remitente (tu correo):")
subject = st.text_input("Asunto del correo:")

# Destinatarios
st.subheader("Destinatarios")
recipient_type = st.radio("¿Cómo quieres agregar los destinatarios?", ("Ingresar manualmente", "Cargar desde archivo .txt"))
if recipient_type == "Ingresar manualmente":
    receiver_emails = st.text_area("Correos destinatarios (separados por comas):")
else:
    uploaded_file = st.file_uploader("Sube un archivo .txt con los correos (uno por línea)", type="txt")
    if uploaded_file is not None:
        receiver_emails = uploaded_file.read().decode("utf-8").replace('\n', ', ')
    else:
        receiver_emails = ""

# Mensaje
st.subheader("Contenido del mensaje")
message_type = st.radio("Selecciona el tipo de mensaje:", ("Texto", "HTML"))
message_content = st.text_area("Contenido del mensaje (Texto o HTML):")

# Previsualización si es HTML
if message_type == "HTML" and message_content:
    st.subheader("Previsualización del mensaje HTML")
    st.markdown(message_content, unsafe_allow_html=True)

# Botón para enviar el correo
if st.button("Enviar correo"):
    if smtp_server and smtp_port and smtp_user and smtp_password and sender_email and receiver_emails and subject and message_content:
        try:
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = ", ".join(receiver_emails.split(", "))
            msg['Subject'] = subject

            # Adjuntar contenido
            if message_type == "HTML":
                msg.attach(MIMEText(message_content, 'html'))
            else:
                msg.attach(MIMEText(message_content, 'plain'))

            # Enviar correo
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_user, smtp_password)
                server.sendmail(sender_email, receiver_emails.split(", "), msg.as_string())
            st.success("Correo enviado exitosamente, eres una Lacrita vale...")
        except Exception as e:
            st.error(f"Error al enviar el correo: {e}")
    else:
        st.warning("Por favor, completa todos los campos.")
