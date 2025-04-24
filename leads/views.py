from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Lead
from .forms import leadModelForm, CustomUserCreationForm, AssignAgentForm
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin
from agents.mixins import OrganizationAndLoginRequiredMixin
    

# Class Based Views
class HomePageView(generic.TemplateView):
    template_name = 'homePage.html'


class LeadListView(LoginRequiredMixin, generic.ListView):
    template_name = 'leads/leadList.html'
    context_object_name = 'leads'

    def get_queryset(self):
        if self.request.user.is_organizer:
            queryset = Lead.objects.filter(organization=self.request.user.userprofile, agent__isnull=False)
        else:
            queryset = Lead.objects.filter(organization=self.request.user.agent.organization)
            # Filter for the agent that is logged in.
            queryset = queryset.filter(agent__user=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        if user.is_organizer:
            queryset = Lead.objects.filter(organization=user.userprofile, agent__isnull=True)
            context.update({'unassigned_leads': queryset})
        
        return context
    

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


class AssignAgentView(OrganizationAndLoginRequiredMixin, generic.FormView):
    template_name = 'leads/assignAgent.html'
    form_class = AssignAgentForm

    def get_success_url(self):
        return reverse('lead:leadList')
        
    def get_form_kwargs(self, **kwargs):
        kwargs = super().get_form_kwargs(**kwargs)
        kwargs.update({'request':self.request})
        return kwargs

    def form_valid(self, form):
        agent = form.cleaned_data['agent']
        lead = Lead.objects.get(id=self.kwargs['pk'])
        lead.agent = agent
        lead.save()

        return super().form_valid(form)
        

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