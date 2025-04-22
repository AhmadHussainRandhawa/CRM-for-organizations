from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Lead
from .forms import leadModelForm, CustomUserCreationForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizationAndLoginRequiredMixin

import logging
from django.contrib.auth import get_user_model, logout
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.forms import SetPasswordForm
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import force_str
from django.shortcuts import redirect
from django.urls import reverse_lazy

logger = logging.getLogger(__name__)
User = get_user_model()

class DebugPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = SetPasswordForm
    success_url = reverse_lazy('password_reset_complete')

    def dispatch(self, *args, **kwargs):
        logger.info("👉 dispatch() called with kwargs: %s", kwargs)
        self.validlink = False
        self.user = None

        uidb64 = kwargs.get('uidb64')
        token = kwargs.get('token')
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            self.user = User.objects.get(pk=uid)
            logger.info("✅ User found: %s", self.user)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            logger.warning("⚠️ UID decoding failed or user not found.")

        if self.user is not None and default_token_generator.check_token(self.user, token):
            self.validlink = True
        else:
            logger.warning("⚠️ Invalid token for user.")

        return super().dispatch(*args, **kwargs)

    def form_valid(self, form):
        logger.info("💡 form_valid reached. new_password1=%r", form.cleaned_data.get('new_password1'))

        form.save()  # Save new password
        logger.info("  ▶️ password hash after save: %r", self.user.password)

        # Instead of calling super().form_valid(form), we manually do everything
        logout(self.request)
        logger.info("🔒 logged out old session after password reset")

        return redirect(self.success_url)

    def form_invalid(self, form):
        logger.warning("⚠️ form_invalid: %s", form.errors)
        return super().form_invalid(form)
    

# Class Based Views
class HomePageView(generic.TemplateView):
    template_name = 'homePage.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/leadList.html'
    context_object_name = 'leads'

    def get_queryset(self):
        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(organization=self.request.user.userprofile)
        else:
            queryset = Lead.objects.filter(organization=self.request.user.agent.organization)
            # Filter for the agent that is logged in.
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset
            

class LeadDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'leads/leadDetail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(OrganizationAndLoginRequiredMixin, generic.CreateView):
    template_name = 'leads/leadCreate.html'
    form_class = leadModelForm
    
    def get_success_url(self):
        return reverse('leads:leadList')
    
    def form_valid(self, form):
        # TO send mail
        send_mail(
            subject="A lead has been Created",
            message = "Now Go and check new leads",
            from_email = 'HAmac@gmail.com',
            recipient_list=['tesdsfc.rom'],
        )

        return super().form_valid(form)
    
    

class LeadEditView(OrganizationAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'leads/leadEdit.html'
    form_class = leadModelForm

    def get_success_url(self):
        return reverse('leads:leadList')
    
    def get_queryset(self):
        return Lead.objects.filter(organization=self.request.user.userprofile)


class LeadDeleteView(OrganizationAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'leads/leadDelete.html'

    def get_success_url(self):
        return reverse('leads:leadList')
    

    def get_queryset(self):
        return Lead.objects.filter(organization=self.request.user.userprofile)
    

class SignupView(generic.CreateView):
    template_name = 'registration/signup.html'
    form_class = CustomUserCreationForm

    def get_success_url(self):
        return reverse('login')



# Function based views:
"""def homePage(request):
    return render(request, 'homePage.html')

def leadList(request):
    leads = Lead.objects.all()
    context = {'leads': leads}

    return render(request, 'leads/leadList.html', context)

def leadDetail(request, pk):
    lead = Lead.objects.get(id=pk)
    context = {'lead': lead}

    return render(request, 'leads/leadDetail.html', context)

def leadCreate(request):
    if request.method=='POST':
        form = leadModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('leads:leadList')
        
    else: 
        form = leadModelForm()
    
    context = {'form':form}
    return render(request, 'leads/leadCreate.html', context)
    
def leadEdit(request, pk):
    lead = Lead.objects.get(id=pk)
    if request.method=='POST':
        form = leadModelForm(request.POST, instance=lead)   # It add new data in the previous lead
        if form.is_valid():
            form.save()
            return redirect('leads:leadList')
    else: 
        form = leadModelForm(instance=lead)     # It shows the previous data of a lead
    
    context = {'form':form, 'lead':lead}
    return render(request, 'leads/leadEdit.html', context)
    

def leadDelete(pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('leads:leadList')
"""


"""def leadEdit(request, pk):
    lead = Lead.objects.get(id=pk)
    if request.method=='POST':
        form = leadModelForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = form.cleaned_data['agent']

            lead.first_name = first
            lead.last_name = last
            lead.age = age
            lead.agent = agent

            lead.save()
            return redirect('leads:leadList')

    else: 
        form = leadModelForm(request.POST)
    
    context = {'lead':lead, 'form': form}
    
    return render(request, 'leads/leadEdit.html', context)


def leadCreate(request):
    if request.method=="POST":
        form = leadForm(request.POST)
        if form.is_valid():
            first = form.cleaned_data['first_name']
            last = form.cleaned_data['last_name']
            age = form.cleaned_data['age']
            agent = Agent.objects.get(id=2)
            Lead.objects.create(first_name=first, last_name=last, age=age, agent=agent)
            return redirect('leads:leadList')
                
    else:
        form = leadForm()

    context = {'form': form}

    return render(request, 'leads/leadCreate.html', context)
"""