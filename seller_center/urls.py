from django.conf import settings
from django.conf.urls import include, url
from django.contrib import admin

from wagtail.admin import urls as wagtailadmin_urls
from wagtail.core import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from search import views as search_views
from sign_up import views as sign_up_views
from product import views as product_views

urlpatterns = [
    url(r'^django-admin/', admin.site.urls),

    url(r'^admin/', include(wagtailadmin_urls)),
    url(r'^documents/', include(wagtaildocs_urls)),

    url(r'^search/$', search_views.search, name='search'),
    
    url(r'^sign/(?P<username>.*)(?P<clientId>.*)(?P<clientSecret>.*)(?P<visibility>.*)', sign_up_views.sign_up, name='sign_up'),
    url(r'^sign/verify_email', sign_up_views.verify_email, name='verify_email'),
    
    url(r'^products/import/download_template', product_views.download_template, name='download_template'),
    url(r'^products/add-new-products', product_views.products_import, name='products_import'),
    url(r'^products/add-single-product', product_views.product_import, name='product_import'),
    url(r'^products/delete/(?P<product_id>.*)/$', product_views.product_delete, name='product_delete'),
    url(r'^products/unlist/(?P<product_id>.*)/$', product_views.product_unlist, name='product_unlist'),
    url(r'^products/suspend/(?P<product_id>.*)/$', product_views.product_suspend, name='product_suspend'),
    url(r'^products/live/(?P<product_id>.*)/$', product_views.product_live, name='product_live'),

    # For anything not caught by a more specific rule above, hand over to
    # Wagtail's page serving mechanism. This should be the last pattern in
    # the list:
    url(r'', include(wagtail_urls)),

    # Alternatively, if you want Wagtail pages to be served from a subpath
    # of your site, rather than the site root:
    #    url(r'^pages/', include(wagtail_urls)),
]


if settings.DEBUG:
    from django.conf.urls.static import static
    from django.contrib.staticfiles.urls import staticfiles_urlpatterns

    # Serve static and media files from development server
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
