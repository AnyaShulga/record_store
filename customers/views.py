from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from .models import Customer, User
from .forms import UserRegisterForm


class CreateUserView(CreateView):
    model = User
    template_name = "registration.html"
    form_class = UserRegisterForm

    def get_success_url(self, **kwargs):
        return reverse_lazy("customers:data", kwargs={'pk': self.object.pk})


class CustomerUpdateView(LoginRequiredMixin, UpdateView):
    login_url = "/customers/login/"
    model = Customer
    fields = ['address']

    def get_success_url(self):
        return self.request.POST.get("next")


class CustomerDetailsView(LoginRequiredMixin, DetailView):
    login_url = "/customers/login/"
    model = Customer
    template_name = "data.html"


@login_required(login_url="/customers/login")
def get_delivery_address(request, pk):
    user_id = request.user.id
    customer = Customer.objects.get(user_id=user_id)
    if Customer.objects.filter(user_id=user_id).filter(address__exact='').exists():
        return HttpResponseRedirect(reverse("customers:delivery_address", args=(
            Customer.objects.get(user_id=user_id).pk,)) + f'?next={request.path}')
    else:
        context = {"customer": customer}
        return render(request, template_name="delivery_address.html", context=context)

