from celery import shared_task
from django.core.mail import EmailMessage,send_mail
from recruitmentportal.settings import DEFAULT_FROM_EMAIL as me

@shared_task(bind=True)
def application_confirmation_mail(self,user):
    email = user.email
    subject = 'Subject: Confirmation of Submitted Application'
    content = ''' Hi {},

This email is to confirm that the we have received your application for the Microsoft Innovations Club. We appreciate your interest and enthusiasm for the program, and we are impressed by your passion for technology.

Your application has been thoroughly reviewed, and we are pleased to inform you that it has been successfully submitted. Thank you for taking the time to complete and submit your application.

Please be advised that the review process may take few days, and we will keep you updated on the status of your application. Kindly, Check for the Status of Application in Recruitment Portal.In the meantime, if you have any questions or concerns, please don't hesitate to reach out to us.

We look forward to reviewing your application and getting to know you better.

Best regards,
Microsoft Innovations Club 
    '''.format(user.username)
    message = EmailMessage(subject,content,me,[email])
    message.send()

@shared_task(bind=True)
def shortlist_mail(self,user):
    email = user.email
    subject = "Microsoft Innovations Club Interview Invitation"
    content = ''' Hi {},

Your application for the Microsoft Innovations Club has been shortlisted, and we'd like to invite you to the next round of interviews. We will contact you soon regarding the timings and mode of interviews.

Please come prepared to talk about your passion for technology and innovation.

If you have any questions, feel free to ask.

Looking forward to meeting you,
Microsoft Innovations Club
    '''.format(user.username)
    message = EmailMessage(subject,content,me,[email])
    message.send()

@shared_task(bind=True)
def mentorship_mail(self,user):
    email = user.email
    subject = 'Join the Microsoft Innovations Club Mentorship Program'
    content = ''' Hi {},

We're inviting you to join our mentorship program at the Microsoft Innovations Club. As a member, you'll be paired with an experienced mentor to help guide you in your tech journey.

This is a great chance to learn from others, expand your network, and gain insights into the industry. Your mentor will be there to support you and answer questions.

Let us know if you're interested and we'll send more information.

Best,
[Technical Team Name]
Microsoft Innovations Club Technical Team
    '''.format(user.username)
    message = EmailMessage(subject,content,me,[email])
    message.send()
@shared_task(bind = True)
def acceptance_mail(self,user):
    email = user.email
    subject = 'Acceptance to Microsoft Innovations Club!'
    content = ''' Hi {},

Congratulations! Your application for the Microsoft Innovations Club has been accepted, and we're excited to have you join our community of tech enthusiasts.

As a member, you'll have access to exclusive events, workshops, and resources, as well as the opportunity to collaborate with other motivated individuals. We encourage you to get involved and make the most of your membership.

You'll receive an official acceptance letter with important information.

We're looking forward to working with you!

Best,
Microsoft Innovations Club Technical Team
    '''.format(user.username)
    message = EmailMessage(subject,content,me,[email])
    message.send()
    