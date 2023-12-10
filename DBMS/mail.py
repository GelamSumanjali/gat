import smtplib

def email(recv, reg, pswd):
    sender = 'iamvengeance816@gmail.com'
    receivers = recv
    message = """
    Subject: Registration Details
    Registration Id:"""+str(reg)+"""
    Password:"""+pswd+"""
    """
    smtp = smtplib.SMTP("smtp.gmail.com",587)
    smtp.starttls()
    smtp.login('iamvengeance816@gmail.com', 'batman@1234')
    smtp.sendmail(sender, receivers, message)
