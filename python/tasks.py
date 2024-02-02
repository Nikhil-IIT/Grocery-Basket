from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from celery import Celery
from app import create_ap
from workers import celery
from app import Users
from celery.schedules import crontab
from datetime import datetime as date, timedelta
from app import Orders


@celery.on_after_finalize.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute=55, hour=16), daily_reminder.s(), name='At evening of everyday ')
    sender.add_periodic_task(crontab(minute=1, hour=17, day_of_month=28), monthy_report.s(), name='At first day of everymonth')
    # sender.add_periodic_task(crontab(minute=10, hour=20, day_of_month=19, month_of_year=11, year=2023), monthy_report.s(), name='At first day of everymonth')
    # sender.add_periodic_task(crontab(minute='*/1'), monthy_report.s(), name='At first day of everymonth')

def send_mail(message, subject, receiver):
    s_mail = 'nikhil0101786@zohomail.in'
    s_pass = 'Nikhil@786'
    
    msg = MIMEMultipart()
    msg['From'] = s_mail
    msg['To'] = receiver
    msg['Subject'] = subject
    
    body = message
    msg.attach(MIMEText(body, 'html'))
    
    server = smtplib.SMTP_SSL('smtp.zoho.in', 465)
    
    # server = smtplib.SMTP('smtp.zoho.in', 465)
    # server.starttls()
    
    try:
        server.login(s_mail, s_pass)
        text = msg.as_string()
        server.sendmail(s_mail, receiver, text)
        print("Email sent successfully")
    except Exception as e:
        print("Error sending email:", str(e))
    finally:
        server.quit()


@celery.task(name='daily_reminder')
def daily_reminder():
    data = {}
    current_time = date.now()
    time_window = current_time - timedelta(days=2)
    send_mail("Hey,Sorry for interupt but you not visited Grocery Basket from Several days,We missing you,Please have a visit Thanks","Daily Reminder","nikhil0101786@gmail.com")
    # users_to_remind = Users.query.filter(Users.last_visited < time_window ).all()
    # for user in users_to_remind:
    #     send_mail("Hey,Sorry for interupt but you not visited Grocery Basket from Several days,We missing you,Please have a visit Thanks","Daily Reminder","nikhil0101786@gmail.com")
    return 'Daily Reminder sent'

@celery.task(name='monthy_report')
def monthy_report():
    data = {}
    current_time = date.now()
    time_window = current_time - timedelta(days=2)
    
    # users_to_remind = Users.query.filter(Users.last_visited < time_window ).all()

    # for user in users_to_remind:
    #     send_mail("Hello,monthly report send","Monthly Report","nikhil0101786@gmail.com")

    orders=Orders.query.filter(Orders.username=="nikhil").all()
    html_report = """
        <html>
        <head>
            <title>Monthly Report From Grocery Basket</title>
        </head>
        <body>
        <h1>Monthly Report For - {month_name} {year}</h1>
        <p>Below is the Products which are ordered by you in the given month:</p>
        <ul>
    """.format(month_name=current_time.strftime('%B'), year=current_time.year)

    for order in orders:
        html_report += f"<li>{order.product_name}</li>"

    html_report += """
        </ul>
    </body>
    </html>
    """
    send_mail(html_report,"Monthly Report","nikhil0101786@gmail.com")    
    return 'Monthly Report sent'
