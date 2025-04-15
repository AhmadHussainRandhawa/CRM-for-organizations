from django.shortcuts import reverse
from django.views import generic
from leads.models import Agent


class AgentListView(generic.ListView):
    template_name = 'agents/agentList.html'

    def get_queryset(self):
        return Agent.objects.all()
