from django.urls import path
from .views import AgentListView, AgentCreateView, AgentDetailView, AgentUpdateView, AgentDeleteView

app_name = 'agents'

urlpatterns = [
    path('', AgentListView.as_view(), name='agentList'),
    path('create/', AgentCreateView.as_view(), name='agentCreate'),
    path('<int:pk>/detail', AgentDetailView.as_view(), name='agentDetail'),
    path('<int:pk>/update', AgentUpdateView.as_view(), name='agentUpdate'),
    path('<int:pk>.delete', AgentDeleteView.as_view(), name='agentDelete'),
]
