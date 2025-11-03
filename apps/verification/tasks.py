from celery import shared_task
from django.core.mail import EmailMessage
from django.template.loader import render_to_string

@shared_task
def send_email_task(subject, template_name, context, from_email, to_email):
    message = render_to_string(template_name, context)
    email = EmailMessage(
        subject=subject,
        body=message,
        from_email=from_email,
        to=[to_email],
    )
    email.content_subtype = "html"
    email.send(fail_silently=False)
