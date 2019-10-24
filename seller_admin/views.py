from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
from users.models import Documents
from product.models import Product

# Create your views here.

USERS_PER_PAGE = 5


def view_all_sellers(request):
    all_users = (
        User.objects.filter(groups__name="Seller")
        .only("username", "email")
        .order_by("id")
    )
    paginator = Paginator(all_users, USERS_PER_PAGE)

    page_num = request.GET.get("page", 1)

    return render(
        request,
        "seller_admin/view_all_sellers.html",
        {"users": paginator.get_page(page_num)},
    )


def view_seller_documents(request, user_id):
    username = User.objects.only("username").get(id=user_id)
    docs = Documents.objects.filter(profile__user_id=user_id)
    return render(
        request,
        "seller_admin/view_seller_documents.html",
        {"documents": docs, "username": username},
    )


def view_seller_products(request, user_id):
    context = {}
    context["username"] = User.objects.only("username").get(id=user_id)
    context.update(
        Product.get_view_all_product_context(
            user_id=user_id,
            status=request.GET.get("status", "all"),
            page_number=request.GET.get("page", 1),
        )
    )
    return render(request, "seller_admin/view_seller_products.html", context)

