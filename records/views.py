from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q, Sum
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, TemplateView, CreateView
from .models import Record, Order
from .forms import RecordForm
from .tasks import notify_order_created


def order(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == "POST":
        if "items in cart" in request.session:
            request.session["items in cart"].append(pk)
            request.session.modified = True
        else:
            request.session["items in cart"] = [pk]
        next = request.POST.get('next')
        return HttpResponseRedirect(next)
    request.session.clear_expired()
    context = {"record": record}
    return render(request, "add_to_cart.html", context)


class HomePageView(TemplateView):
    template_name = "home.html"


class RecordListView(ListView):
    template_name = "list.html"
    queryset = (
        Record
        .objects
        .order_by("artist")
        .all()
    )


class RecordDetailView(DetailView):
    template_name = "details.html"
    queryset = (
        Record
        .objects
        .select_related("record_label")
        .prefetch_related("genre")
    )


class RecordAddView(CreateView):
    model = Record
    template_name = "add_record.html"
    form_class = RecordForm
    success_url = reverse_lazy("records:list")


class RecordDeleteView(DeleteView):
    template_name = "confirm_delete.html"
    model = Record
    success_url = reverse_lazy("records:list")


class SearchView(ListView):
    model = Record
    template_name = "search_results.html"

    def get_queryset(self):
        query = self.request.GET.get("q")
        object_list = Record.objects.filter(
            Q(artist__icontains=query) | Q(album__icontains=query) | Q(year__icontains=query)
        )
        return object_list


def get_order_list(request):
    try:
        cart = request.session["items in cart"]
        if len(cart) == 0:
            context = {
                "message": "No records added yet"
            }
        else:
            queryset = Record.objects.filter(pk__in=cart).all()
            total_price = (Record.objects.filter(pk__in=cart).aggregate(Sum('price')))["price__sum"]
            context = {
                "orders": queryset,
                "price": total_price
            }
    except KeyError:
        context = {
            "message": "No records added yet"
        }
    return render(request, template_name="cart.html", context=context)


def delete_from_cart(request, pk):
    record = Record.objects.get(pk=pk)
    if request.method == "POST":
        request.session["items in cart"].remove(pk)
        request.session.modified = True
        return HttpResponseRedirect(reverse_lazy("records:cart"))
    context = {"record": record}
    return render(request, template_name="delete_from_cart.html", context=context)


@login_required(login_url="/customers/login/")
def placing_an_order(request):
    user_id = request.user.id
    cart = request.session["items in cart"]
    records = Record.objects.filter(pk__in=cart)
    date = datetime.now()
    order = Order(user_id=user_id, date=date)
    order.save()
    for item in cart:
        order.record.add(item)
    del request.session["items in cart"]
    task = notify_order_created.delay()
    return render(request, "got_order.html")


@login_required(login_url="/customers/login/")
def list_of_orders(request):
    user_id = request.user.id
    queryset = (
        Order
        .objects
        .filter(user_id=user_id)
        .all()
    )
    context = {
        "orders": queryset
    }
    return render(request, "order.html", context)


class OrderDetailsView(LoginRequiredMixin, DetailView):
    login_url = "/customers/login/"
    template_name = "order_details.html"
    model = Order


def get_task(request, task_id: str):
    task_result = notify_order_created.AsyncResult(task_id)

    return JsonResponse({
        "task_id": task_id,
        "status": task_result.status,
    })
