from email.message import EmailMessage
import smtplib

sender="test.maricuricatedra@gmail.com"
recipient="test.andsalo13@gmail.com"
mensaje="Hola funciona esto"
email= EmailMessage()
email["From"] = sender
email["To"] = recipient
email["Subject"] = "Testeo"
email.set_content(mensaje)

smtp= smtplib.SMTP_SSL('smpt.gmail.com')
smtp.login(sender,"pydh ubxz fdiy neuo")
smtp.sendmail(sender,recipient,email.as_string())
smtp.quit()