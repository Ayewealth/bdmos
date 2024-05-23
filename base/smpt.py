import smtplib

try:
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login('anwasiprince@gmail.com', 'occoksgxivvjsavy')
    print("Connection successful")
    server.quit()
except Exception as e:
    print(f"Failed to connect: {e}")
