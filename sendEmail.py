import smtplib
from email.mime.text import MIMEText
import os

def send_email(subject, body, to_email):

    sender_email = os.environ.get("SENDER_EMAIL")
    password = os.environ.get("EMAIL_PASSWORD")
    
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = sender_email
    msg['To'] = to_email

    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, password)
        server.sendmail(sender_email, to_email, msg.as_string())
        server.quit()
        print("Email was sent!")
        return True
    except Exception as e:
        # Aqui, você pode registrar o erro em um log, se for o caso
        print(e)
        return False

def send_notification_email(valor_atual, variacao):
    """Envia o e-mail de notificação de variação do dólar."""
    subject = "ALERTA: Variação Relevante do Dólar!"
    body = f"""
    Prezado time,
    
    O dólar (USD/BRL) teve uma variação de {variacao:.2f}% nas últimas 24h.
    O valor atual é de R${valor_atual:.2f}.
    
    Atenciosamente,
    Equipe de Automação
    """
    to_email = os.environ.get("SENDER_EMAIL")
    return send_email(subject, body, to_email)

def send_weekly_summary_email(cotacoes):
    """Envia o e-mail semanal com um resumo das cotações."""
    subject = "Resumo Semanal de Cotações de Moedas"
    body = f"""
    Prezado time,
    
    Segue o resumo semanal das cotações de moedas:
    
    Dólar (USD/BRL): R${cotacoes['USD-BRL']:.2f}
    Euro (EUR/BRL): R${cotacoes['EUR-BRL']:.2f}
    
    Atenciosamente,
    Equipe de Automação
    """
    to_email = os.environ.get("SENDER_EMAIL")
    return send_email(subject, body, to_email)
