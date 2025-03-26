from django.shortcuts import render, redirect
from .models import Lead, Agent
from .forms import leadForm, leadModelForm


def homePage(request):
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
    
    return render(request, 'leads/leadCreate.html', {'form':form})


def leadEdit(request, pk):
    lead = Lead.objects.get(id=pk)
    if request.method == 'POST':
        form = leadModelForm(request.POST, instance=lead)
        if form.is_valid():
            form.save()
            return redirect('leads:leadList')

    else:
        form = leadModelForm(instance=lead)

    context = {'form':form, 'lead':lead}
    return render(request, 'leads/leadEdit.html', context)


def leadDelete(request, pk):
    lead = Lead.objects.get(id=pk)
    lead.delete()
    return redirect('leads:leadList')


# def leadEdit(request, pk):
#     lead = Lead.objects.get(id=pk)
#     if request.method=='POST':
#         form = leadModelForm(request.POST)
#         if form.is_valid():
#             first = form.cleaned_data['first_name']
#             last = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = form.cleaned_data['agent']

#             lead.first_name = first
#             lead.last_name = last
#             lead.age = age
#             lead.agent = agent

#             lead.save()
#             return redirect('leads:leadList')

#     else: 
#         form = leadModelForm(request.POST)
    
#     context = {'lead':lead, 'form': form}
    
#     return render(request, 'leads/leadEdit.html', context)


# def leadCreate(request):
#     if request.method=="POST":
#         form = leadForm(request.POST)
#         if form.is_valid():
#             first = form.cleaned_data['first_name']
#             last = form.cleaned_data['last_name']
#             age = form.cleaned_data['age']
#             agent = Agent.objects.get(id=2)
#             Lead.objects.create(first_name=first, last_name=last, age=age, agent=agent)
#             return redirect('leads:leadList')
                
#     else:
#         form = leadForm()

#     context = {'form': form}

#     return render(request, 'leads/leadCreate.html', context)
