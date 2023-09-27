from django.urls import path, reverse_lazy

from django.contrib.auth.views import LoginView, LogoutView

from .views import CreateUserView, CustomerUpdateView, CustomerDetailsView, get_delivery_address

app_name = "customers"

urlpatterns = [
    path("login/", LoginView.as_view(template_name="login.html", next_page=reverse_lazy("records:list")), name="login"),
    path("logout/", LogoutView.as_view(next_page=reverse_lazy("customers:login")), name="logout"),
    path("registration/", CreateUserView.as_view(), name="registration"),
    path("my_account/<int:pk>/", CustomerDetailsView.as_view(), name="data"),
    path("delivery_address/<int:pk>", CustomerUpdateView.as_view(template_name="customer_form.html"), name="delivery_address"),
    path("address/<int:pk>", get_delivery_address, name="address"),
]