from django.dispatch import receiver
from store.signals import order_created


@receiver(order_created) # وقتی سندر اینجا تعریف نکردم یعنی هر کس فرستاد این کار رو بکن.
def send_email_and_sms(sender, **kwargs):
    # print(f"New order created with id {kwargs.get('order').id}")
    
    # این رو خودم ادامه دادم 😊
    import smtplib, ssl
    order = kwargs.get('order')
    sender_email = "shookooljooni254@gmail.com"
    password = "tvsr oqip wylo ykcl"
    receiver_email = ["mohammad.pfallah@gmail.com", "shookooljooni254@gmail.com"]
    message_body = f"Thanks dear {order.customer}. Your order has been created successfully with id {order.id} and will be sent ASAP.\nبا تشکر\nمحمد پورمحمدی فلاح"
    message = f"Subject: Order Created\n{message_body}".encode('utf-8')
    smtp_server = "smtp.gmail.com"
    port = 465  # For SSL
    # port = 587  # For starttls
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL(smtp_server, port, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
        print('Email Sent!!!')
    import ghasedakpack
    sms = ghasedakpack.Ghasedak("f889f4f2754a67771b17e6bed88477d582b594f844ff6b4c7b62db2679d98f5d")
    message = f'{order.customer} عزیز. سفارش شما با موفقیت و آی دی {order.id} ثبت شد. لغو۱۱'
    my_number = '09198004498'
    line_number = '30005006009956'
    sms.send({'message': message, 'receptor' : my_number, 'linenumber': line_number})