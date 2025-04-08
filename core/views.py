from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import Project, Skill, SocialLink,Service
from .forms import ContactForm

# views.py
from django.shortcuts import render
from .models import HomePageContent

def home1(request):
    content = HomePageContent.objects.filter(version='home1', is_active=True).first()
    context = {
        'content': content
    }
    return render(request, 'home1.html', context)

def home2(request):
    content = HomePageContent.objects.filter(version='home2', is_active=True).first()
    context = {
        'content': content
    }
    return render(request, 'home2.html', context)

# views.py
from django.shortcuts import render
from .models import AboutContent, SocialLink

def about(request):
    about_content = AboutContent.objects.filter(is_active=True).first()
    social_links = SocialLink.objects.filter(is_active=True)
    
    # Prepare filtered data for the template
    experiences = about_content.experiences.filter(is_active=True) if about_content else []
    educations = about_content.educations.filter(is_active=True) if about_content else []
    testimonials = about_content.testimonials.filter(is_active=True) if about_content else []

    context = {
        'about_content': about_content,
        'social_links': social_links,
        'experiences': experiences,
        'educations': educations,
        'testimonials': testimonials,
    }
    return render(request, 'about.html', context)



def projects(request):
    projects = Project.objects.all()
    context = {
        'projects': projects
    }
    return render(request, 'projects.html', context)

def skills(request):
    skills = Skill.objects.all()
    context = {
        'skills': skills
    }
    return render(request, 'skills.html', context)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            # Send email
            send_mail(
                subject=f"New Contact Form Submission: {form.cleaned_data['subject']}",
                message=f"From: {form.cleaned_data['name']}\nEmail: {form.cleaned_data['email']}\n\nMessage:\n{form.cleaned_data['message']}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
            )
            messages.success(request, 'Your message has been sent successfully!')
            return redirect('contact')
    else:
        form = ContactForm()
    
    context = {
        'form': form
    }
    return render(request, 'contact.html', context)


def services(request):
    services = Service.objects.all()
    return render(request, 'services.html', {'services': services})