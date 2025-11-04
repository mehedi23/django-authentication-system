from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils import timezone
from datetime import timedelta  
import random 
from apps.verification.tasks import send_email_task

class OTPHandler: 
    otp_expiry_minutes = 10  
    otp_length = 6  

    def __init__(self, model, user_field='user', otp_field='otp'):
        """
        model: Django model to store OTP
        user_field: FK to user
        otp_field: field name for OTP
        """
        self.model = model
        self.user_field = user_field
        self.otp_field = otp_field

    def generate_otp(self):
        return str(random.randint(10**(self.otp_length-1), 10**self.otp_length - 1))

    def send_otp(self, user, subject="Your OTP Code", template_name="otp_email.html", from_email="no-reply@example.com"):
        
        otp = self.generate_otp()
        self.model.objects.create(**{self.user_field: user,self.otp_field: otp,'is_verified': False})
   
        message = render_to_string(template_name, {"user": user, "otp": otp})
        email = EmailMessage(
            subject=subject,
            body=message,
            from_email=from_email,
            to=[user.email],
        )
        email.content_subtype = "html"  
        email.send(fail_silently=False)
    
    def send_otp_use_celery(self, user, subject="Your OTP Code", template_name="otp_email.html", from_email="no-reply@example.com"):

        otp = self.generate_otp()
        self.model.objects.create(**{self.user_field: user,self.otp_field: otp,'is_verified': False})

         # Use Celery to send email 
        send_email_task.delay(
            subject=subject,
            template_name=template_name,
            context={"user": user, "otp": otp},
            from_email=from_email,
            to_email=user.email
        )
 
    def verify_otp(self, user, otp):
        try:
            otp_obj = self.model.objects.filter(**{self.user_field: user,self.otp_field: otp,'is_verified': False}).latest('created_at')
        except self.model.DoesNotExist:
            return False, "Invalid OTP"

        if timezone.now() > otp_obj.created_at + timedelta(minutes=self.otp_expiry_minutes):
            return False, "OTP expired"

        otp_obj.is_verified = True
        otp_obj.save()
        
        if hasattr(user, 'is_email_verify'): 
            user.is_email_verify = True
            user.save(update_fields=['is_email_verify'])

        return True, "OTP verified successfully"

    def is_otp_verified(self, user):
        return self.model.objects.filter(**{self.user_field: user},is_verified=True).order_by('-created_at').first()
    
    