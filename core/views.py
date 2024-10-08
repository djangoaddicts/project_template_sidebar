from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from handyhelpers.views import HandyHelperIndexView


class RegisterUser(CreateView):
    """add a new user"""

    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "registration/register_user.html"


class Index(HandyHelperIndexView):
    """render the project index page"""

    title = """Welcome to <span class="text-primary">{{ project_name }}</span><span class="text-secondary"></span>!"""
    subtitle = "Select an option below to get started"
    item_list = [
        {
            "url": "/dashboard",
            "icon": """<i class="fa-solid fa-gauge-high"></i>""",
            "title": "Dashboard",
            "description": "View {{ project_name }} dashboard",
        },
        {
            "url": "/rest",
            "icon": """<i class="fa-solid fa-arrow-right-arrow-left"></i>""",
            "title": "APIs",
            "description": "List available RESTful APIs",
        },
    ]
    protected_item_list = [
        {
            "url": "/admin",
            "icon": """<i class="fa-brands fa-python"></i>""",
            "title": "Django Console",
            "description": "Access the django administrator console",
        },
    ]
    protected_group_name = "admin"


class ProjectDashboard(View):
    """project-level dashboard"""

    template_name = "core/custom/dashboard.html"

    def get(self, request):
        """ """
        context = {}
        return render(request, self.template_name, context=context)
