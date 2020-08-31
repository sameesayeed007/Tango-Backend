from django.core.mail import EmailMessage


class Util:
    @staticmethod
    def send_email(data):
        values={
            'name' : 'intense',
            'template' : 'email_template.html',
            'subject' : 'Thank you for purchasing',
            'sender' : 'mkaf10imran@gmail.com',
            'receiver': ['mkaf10imran@gmail.com']
        }
        email = EmailMessage(
            data['email_subject'], 
            data['email_body'], 
            values['sender'],
            [data['to_email']])
            
        email.send()