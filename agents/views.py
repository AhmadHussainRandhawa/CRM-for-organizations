from django.shortcuts import reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from django.contrib.auth.mixins import LoginRequiredMixin

class AgentListView(LoginRequiredMixin, generic.ListView):
    template_name = 'agents/agentList.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.all()


class AgentCreateView(LoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agentCreate.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agentList')

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()

        return super().form_valid(form)
    

class AgentDetailView(LoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agentDetail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.all()
    

class AgentUpdateView(LoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agentUpdate.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agentList')

    def get_queryset(self):
        return Agent.objects.all()


class AgentDeleteView(LoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agentDelete.html'

    def get_queryset(self):
        return Agent.objects.all()
    
    def get_success_url(self):
        return reverse('agents:agentList')
