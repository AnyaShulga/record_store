from django.urls import path

from .views import (HomePageView,
                    RecordListView,
                    RecordDeleteView,
                    RecordDetailView,
                    get_order_list,
                    order,
                    RecordAddView,
                    SearchView,
                    placing_an_order,
                    list_of_orders, delete_from_cart, OrderDetailsView
                    )

app_name = "records"

urlpatterns = [
    path("", HomePageView.as_view(), name="home"),
    path("catalogue/", RecordListView.as_view(), name="list"),
    path("<int:pk>/", RecordDetailView.as_view(), name="details"),
    path("<int:pk>/confirm_delete", RecordDeleteView.as_view(), name="delete"),
    path("cart/", get_order_list, name="cart"),
    path("cart/confirm_delete/<int:pk>", delete_from_cart, name="delete_from_cart"),
    path("add_to_cart/<int:pk>/", order, name="add_to_cart"),
    path("details/<int:pk>/", RecordDetailView.as_view(), name="details"),
    path("add/", RecordAddView.as_view(), name="add"),
    path("search/", SearchView.as_view(), name="search_results"),
    path("got_order", placing_an_order, name="got_order"),
    path("orders/", list_of_orders, name="orders"),
    path("orders/<int:pk>", OrderDetailsView.as_view(), name="order_details")
]