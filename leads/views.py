from django.core.mail import send_mail
from django.shortcuts import render, redirect, reverse
from .models import Lead
from .forms import leadModelForm, CustomUserCreationForm
from django.views import generic


# Class Based Views
class HomePageView(generic.TemplateView):
    template_name = 'homePage.html'


class LeadListView(generic.ListView):
    template_name = 'leads/leadList.html'
    queryset = Lead.objects.all()
    context_object_name = 'leads'


class LeadDetailView(generic.DetailView):
    template_name = 'leads/leadDetail.html'
    queryset = Lead.objects.all()
    context_object_name = 'lead'


class LeadCreateView(generic.CreateView):
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
    
    

class LeadEditView(generic.UpdateView):
    template_name = 'leads/leadEdit.html'
    queryset = Lead.objects.all()
    form_class = leadModelForm

    def get_success_url(self):
        return reverse('leads:leadList')
    

class LeadDeleteView(generic.DeleteView):
    template_name = 'leads/leadDelete.html'
    queryset = Lead.objects.all()

    def get_success_url(self):
        return reverse('leads:leadList')
    

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