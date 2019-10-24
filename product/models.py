from django.core.paginator import Paginator
from django.db import models
from modelcluster.fields import ParentalKey
from wagtail.core.fields import StreamField
from base.models import BasePage, GeneralStreamBlock
from wagtail.snippets.models import register_snippet
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    MultiFieldPanel,
    FieldRowPanel,
)
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from modelcluster.models import ClusterableModel
from wagtail.core.models import Orderable
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from datetime import datetime


from users.models import Profile
from users.models import Address

from enum import Enum



class ProductStatus(Enum):  # A subclass of Enum
    UNPUBLISHED = "UNPUBLISHED"
    LIVE_APPROVAL = "LIVE_APPROVAL"
    LIVE_APPROVED = "LIVE_APPROVED"
    UNLISTED = "UNLISTED"
    SUSPENDED = "SUSPENDED"


class OrderStatusEnum(Enum):  # A subclass of Enum
    FOR_SHIPPING = "FOR_SHIPPING"
    SHIPPING = "SHIPPING"
    SELLER_CANCELED = "SELLER_CANCELED"
    DELIVERED = "DELIVERED"
    RECEIVED = "RECEIVED"
    COMPLETED = "COMPLETED"
    RETURN_REFUND = "RETURN_REFUND"


class OrderCourierEnum(Enum):  # A subclass of Enum
    LOGISTIKUS = "LOGISTIKUS"
    QUADX = "QUADX"
    MRSPEEDY = "MRSPEEDY"
    XDE = "XDE"
    ELTM = "ELTM"
    ABEST = "ABEST"
    ZOOM = "ZOOM"
    NINJAVAN = "NINJAVAN"


class Category(models.Model):
    unique_id = models.IntegerField(null=False, blank=False, primary_key=True)
    parent_id = models.IntegerField(null=True, blank=True)
    level = models.IntegerField(null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=500)
    image_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="images must have a white background",
    )


class Image(models.Model):
    product = models.ForeignKey(Profile, models.CASCADE, blank=True, null=True)
    url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="images must have a white background",
    )


@register_snippet
class Product(ClusterableModel):

    product_code = models.CharField(null=True, blank=True, max_length=500)
    profile = models.ForeignKey(Profile, models.DO_NOTHING, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    product_name = models.CharField(null=True, blank=True, max_length=500)
    product_description = models.TextField(null=True, blank=True)
    parent_sku_reference_no = models.CharField(null=True, blank=True, max_length=500)

    product_status = models.CharField(
        null=True, blank=True, max_length=500, default=ProductStatus.UNPUBLISHED.value
    )
    status_changed_on = models.DateTimeField(default=datetime.now)
    cover_image_url = models.TextField(null=True, blank=True)
    cover_image = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image1_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Photo must have a white background",
    )
    image1 = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image2_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Photo must have a white background",
    )
    image2 = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image3_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Photo must have a white background",
    )
    image3 = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image4_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Photo must have a white background",
    )
    image4 = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image5_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Photo must have a white background",
    )
    image5 = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    stock_sum = models.IntegerField(blank=True, null=True, default=None)
    product_weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, max_length=500
    )
    product_length = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, max_length=500
    )
    product_width = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, max_length=500
    )
    product_height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True, max_length=500
    )
    product_price = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, max_length=500
    )
    ship_out_in = models.IntegerField(null=True, blank=True)

    product_brand = models.CharField(null=True, blank=True, max_length=500)

    last_updated = models.DateTimeField(null=True, blank=True)
    date_created = models.DateTimeField(default=datetime.now)

    # product_condition = models.CharField(null=True, blank=True, choices=CONDITION_CHOICES, default=CONDITION_CHOICES[0], max_length=500)

    # product_brand = models.CharField(null=True, blank=True, max_length=500)
    # product_sale_price = models.IntegerField(blank=True, null=True, default=None)
    # product_sale_date_start = models.DateField(default=datetime.now, blank=True, null=True)
    # product_sale_date_end = models.DateField(default=datetime.now, blank=True, null=True)
    # product_sale_time_start = models.TimeField(default=datetime.now, blank=True, null=True)
    # product_sale_time_end = models.TimeField(default=datetime.now, blank=True, null=True)
    # live = models.BooleanField(default=False)
    # suspended = models.BooleanField(default=False)
    # unlisted = models.BooleanField(default=False)
    # unpublished = models.BooleanField(default=False)
    # last_updated = models.DateTimeField(null=True, blank=True)
    # date_created = models.DateTimeField(default=datetime.now)

    def save_model(self, request, obj, form, change):
        obj.user_id = request.user.id
        super().save_model(request, obj, form, change)

    def save(self, *args, **kwargs):
        super(Product, self).save(*args, **kwargs)
        self.last_updated = datetime.now()

        # Remove product code errors
        if self.product_code:
            Errors.objects.filter(product_id=self.id).filter(
                name="Product Code is required"
            ).delete()
            if len(str(self.product_code)) <= 100:
                Errors.objects.filter(product_id=self.id).filter(
                    name="Product Code exceeds maximum lenght of 100"
                ).delete()

        # Remove product category errors
        if self.category:
            Errors.objects.filter(product_id=self.id).filter(
                name="Product Category is required"
            ).delete()

        # Remove product name errors
        if self.product_name:
            Errors.objects.filter(product_id=self.id).filter(
                name="Product Name is required"
            ).delete()
            if len(self.product_name) >= 3:
                Errors.objects.filter(product_id=self.id).filter(
                    name="Product Name should have at least 3 characters"
                ).delete()

        # Remove Product description errors
        if self.product_description:
            Errors.objects.filter(product_id=self.id).filter(
                name="Product Description is required"
            ).delete()
            if len(self.product_description) >= 100:
                Errors.objects.filter(product_id=self.id).filter(
                    name="Product Description should have at least 100 characters"
                ).delete()

        # Remove product price errors
        if self.product_price:
            Errors.objects.filter(product_id=self.id).filter(
                name="Missing Product Price"
            ).delete()

        # Remove product stock errors
        if self.stock_sum:
            Errors.objects.filter(product_id=self.id).filter(
                name="Missing Product Stock"
            ).delete()

        # Remove product status errors
        if Errors.objects.filter(product_id=self.id).count() == 0:
            Product.objects.filter(id=self.id).update(
                product_status=ProductStatus.UNLISTED.value
            )
        return HttpResponseRedirect("/products/?category=all#all")

    def __unicode__(self):
        return self.product_name

    @staticmethod
    def get_view_all_product_context(user_id, category="all", page_number=1):
        context = {}

        query_by_category = {
            "all": Product.objects.filter(profile__user_id=user_id).exclude(
                product_status=ProductStatus.UNPUBLISHED.value
            ),
            "live": Product.objects.filter(
                profile__user_id=user_id,
                product_status=ProductStatus.LIVE_APPROVED.value,
            ),
            "soldout": Product.objects.filter(
                profile__user_id=user_id, stock_sum=0
            ).exclude(product_status=ProductStatus.UNPUBLISHED.value),
            "suspended": Product.objects.filter(
                profile__user_id=user_id, product_status=ProductStatus.SUSPENDED.value
            ),
            "unlisted": Product.objects.filter(
                profile__user_id=user_id, product_status=ProductStatus.UNLISTED.value
            ),
            "unpublished": Product.objects.filter(
                profile__user_id=user_id, product_status=ProductStatus.UNPUBLISHED.value
            ),
        }

        products = query_by_category.get(category, query_by_category["all"])

        paginator = Paginator(products, 12)
        paged_products = paginator.page(page_number)

        context["products"] = paged_products
        context["products_user_id"] = user_id
        context["categories"] = [
            {
                "code": "all",
                "humanized": "All",
                "count": query_by_category["all"].count(),
            },
            {
                "code": "live",
                "humanized": "Live",
                "count": query_by_category["live"].count(),
            },
            {
                "code": "soldout",
                "humanized": "Sold Out",
                "count": query_by_category["soldout"].count(),
            },
            {
                "code": "suspended",
                "humanized": "Suspended",
                "count": query_by_category["suspended"].count(),
            },
            {
                "code": "unlisted",
                "humanized": "Unlisted",
                "count": query_by_category["unlisted"].count(),
            },
            {
                "code": "unpublished",
                "humanized": "Unpublished",
                "count": query_by_category["unpublished"].count(),
            },
        ]
        context["active_category"] = category
        return context


class Variations(Orderable, models.Model):
    name = models.CharField(null=True, blank=True, max_length=500)
    sku = models.CharField(null=True, blank=True, max_length=500)
    price = models.CharField(null=True, blank=True, max_length=500)
    stock = models.IntegerField(null=True, blank=True)
    sale_price = models.IntegerField(blank=True, null=True, default=None)
    sale_date_start = models.DateField(default=datetime.now, blank=True, null=True)
    sale_date_end = models.DateField(default=datetime.now, blank=True, null=True)
    sale_time_start = models.TimeField(default=datetime.now, blank=True, null=True)
    sale_time_end = models.TimeField(default=datetime.now, blank=True, null=True)
    image_url = models.CharField(
        null=True,
        blank=True,
        max_length=2000,
        help_text="Optional: If your image is already hosted",
    )
    image_upload = models.ImageField(
        upload_to="original_images",
        null=True,
        blank=True,
        help_text="Optional: If you want to upload a new image. This will replace the image in the URL provided when bulk upload is performed.",
    )
    image_url_from_upload = models.CharField(null=True, blank=True, max_length=2000)
    image_url_from_sku = models.CharField(null=True, blank=True, max_length=2000)
    product = ParentalKey("Product", related_name="variations", null=True, blank=True)

    panels = [
        FieldPanel("name"),
        FieldPanel("sku"),
        FieldPanel("price"),
        FieldPanel("stock"),
        # FieldPanel('image_url'),
        ImageChooserPanel("image_upload"),
    ]

    def save(self, *args, **kwargs):
        super(Variations, self).save(*args, **kwargs)

        # Remove variation image error
        if self.image_upload:
            Errors.objects.filter(product_id=self.product_id).filter(
                name="Product image is required"
            ).delete()
        if Errors.objects.filter(product_id=self.product_id).count() == 0:
            Product.objects.filter(id=self.product_id).update(
                product_status=ProductStatus.UNLISTED.value
            )
        return redirect("/products/?category=all#all")


class Courier(models.Model):
    courier_name = models.CharField(null=True, blank=True, max_length=500)


class OrderCourier(models.Model):
    order_courier = ParentalKey(
        "Order", related_name="ordercourier", null=True, blank=True
    )
    courier = models.ForeignKey(Courier, on_delete=models.CASCADE)
    status = models.CharField(null=True, blank=True, max_length=500)
    status_changed_on = models.DateTimeField(default=datetime.now, blank=True, null=True)
    status_info = models.CharField(null=True, blank=True, max_length=500)


@register_snippet
class Order(ClusterableModel):
    order_reference_number = models.TextField(blank=True, primary_key=True)
    products = models.ManyToManyField(Product, through="OrderedProduct")
    total = models.CharField(null=True, blank=True, max_length=500)
    status = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        default=OrderStatusEnum.FOR_SHIPPING.value,
    )
    status_changed_on = models.DateTimeField(
        default=datetime.now, blank=True, null=True
    )
    countdown = models.CharField(null=True, blank=True, max_length=500)
    courier = models.ForeignKey(
        OrderCourier, null=True, blank=True, max_length=500, on_delete=models.CASCADE
    )
    shipping_channel = models.CharField(null=True, blank=True, max_length=500)
    creation_date = models.CharField(null=True, blank=True, max_length=500)
    paid_date = models.CharField(null=True, blank=True, max_length=500)
    shipping_address = models.TextField(null=True, blank=True)
    pickup_address = models.TextField(null=True, blank=True)
    user_id = models.CharField(null=True, blank=True, max_length=500)
    username = models.CharField(null=True, blank=True, max_length=500)
    additional_info = models.TextField(null=True, blank=True)
    order_date = models.DateField(default=datetime.now, blank=True, null=True)
    order_remark = models.TextField(null=True, blank=True)


class OrderStatus(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    status = models.CharField(
        null=True,
        blank=True,
        max_length=500,
        default=OrderStatusEnum.FOR_SHIPPING.value,
    )
    status_changed_on = models.DateTimeField(default=datetime.now, blank=True, null=True)
    additional_info = models.TextField(null=True, blank=True)


class OrderedProduct(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variations, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField(null=True, blank=True)
    product_price = models.DecimalField(
        max_digits=100, decimal_places=2, null=True, blank=True, max_length=500
    )
    product_name = models.CharField(null=True, blank=True, max_length=500)
    product_description = models.TextField(null=True, blank=True)
    cover_image_url = models.TextField(null=True, blank=True)
    variation_name = models.CharField(null=True, blank=True, max_length=500)
    variation_image_url = models.TextField(null=True, blank=True)


class Errors(ClusterableModel):
    name = models.CharField(null=True, blank=True, max_length=500)
    product = ParentalKey("Product", related_name="errors", null=True, blank=True)


class ProductPage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        return context


class ProductsPage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)

    def get_context(self, request):
        context = super().get_context(request)
        context["subPages"] = self.get_children().live()

        user_id = request.user.id
        category = request.GET.get("category", "all")
        page_number = request.GET.get("page", 1)

        context.update(
            Product.get_view_all_product_context(
                user_id=user_id, category=category, page_number=page_number
            )
        )

        return context


class ProductImportPage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)


class ProductsImportPage(BasePage):
    body = StreamField(GeneralStreamBlock, blank=True)


class Sale(models.Model):
    product = models.ForeignKey(Product, models.DO_NOTHING, blank=True, null=True)
    variation = models.ForeignKey(Variations, models.DO_NOTHING, blank=True, null=True)
    product_sale_price = models.DecimalField(
        max_digits=100, decimal_places=2, blank=True, null=True
    )
    product_sale_date_start = models.DateField(
        default=datetime.now, blank=True, null=True
    )
    product_sale_date_end = models.DateField(
        default=datetime.now, blank=True, null=True
    )
    product_sale_time_start = models.TimeField(
        default=datetime.now, blank=True, null=True
    )
    product_sale_time_end = models.TimeField(
        default=datetime.now, blank=True, null=True
    )

