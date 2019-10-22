from django.shortcuts import render
from django.core.paginator import Paginator
from django.contrib.auth.models import User
# Create your views here.

USERS_PER_PAGE = 5

def view_all_sellers(request):
    context = {}

    all_users = User.objects.filter(groups__name='Seller').only("username", "email").order_by('id')
    paginator = Paginator(all_users, USERS_PER_PAGE)

    page_num = request.GET.get('page', 1)
    context['users'] = paginator.get_page(page_num)

    return render(request, 'seller_admin/view_all_sellers.html', context)
