from api.aws import SES
from api.celery import app


@app.task()
def new_post_notification(recipient, page_name, content):
    html_email_content = f"""
                    <html>
                        <head></head>
                        <body style='background-image: url("https://pbs.twimg.com/media/El48RaWXgAAjmB-.png"); 
                                    height: 600px; 
                                    background-size: cover;
                        '>
                        <h1 style='text-align:center'>New Post from {page_name}</h1>
                        <h2 style='text-align:center'>{content}</h1>
                        </body>
                    </html>
                """
    SES().send_email(recipients=recipient, subject=f'Hey! New post from {page_name}', body=html_email_content)
