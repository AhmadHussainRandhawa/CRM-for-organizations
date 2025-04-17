from django.shortcuts import reverse
from django.views import generic
from leads.models import Agent
from .forms import AgentModelForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import OrganizationAndLoginRequiredMixin


class AgentListView(OrganizationAndLoginRequiredMixin, generic.ListView):
    template_name = 'agents/agentList.html'
    context_object_name = 'agents'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)


class AgentCreateView(OrganizationAndLoginRequiredMixin, generic.CreateView):
    template_name = 'agents/agentCreate.html'
    form_class = AgentModelForm

    def get_success_url(self):
        return reverse('agents:agentList')

    def form_valid(self, form):
        agent = form.save(commit=False)
        agent.organization = self.request.user.userprofile
        agent.save()

        return super().form_valid(form)
    

class AgentDetailView(OrganizationAndLoginRequiredMixin, generic.DetailView):
    template_name = 'agents/agentDetail.html'
    context_object_name = 'agent'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
    

class AgentUpdateView(OrganizationAndLoginRequiredMixin, generic.UpdateView):
    template_name = 'agents/agentUpdate.html'
    form_class = AgentModelForm
    context_object_name = 'agent'

    def get_success_url(self):
        return reverse('agents:agentList')

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)


class AgentDeleteView(OrganizationAndLoginRequiredMixin, generic.DeleteView):
    template_name = 'agents/agentDelete.html'

    def get_queryset(self):
        return Agent.objects.filter(organization=self.request.user.userprofile)
    
    def get_success_url(self):
        return reverse('agents:agentList')
