from django.db import models
from pytils.translit import slugify
import uuid

# Create your models here.


class Category(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50)
    parent = models.UUIDField(null=True)

    def __str__(self):

        return self.title

    def get_parent(self):

        return Category.objects.get(link=self.parent)

    def get_all_children(self):

        return Category.objects.all().filter(parent=self.link)

    @staticmethod
    def get_all_kids_by_parants_slug(slug):

        return Category.objects.get(slug=slug).get_all_children()

    @staticmethod
    def get_all_parentless():

        return Category.objects.filter(parent=None)

    def check_is_endpoint(self):

        return not len(self.get_all_children())


class DetailGroup(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField(max_length=50, null=True, unique=True)

    def __str__(self):

        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(DetailGroup, self).save(*args, **kwargs)


class Detail(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=50)
    detail_group = models.ForeignKey(
        'DetailGroup', on_delete=models.CASCADE, default=None, null=True)
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        ordering = ('title',)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super(Detail, self).save(*args, **kwargs)

    def __str__(self):

        return self.title


class Product(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    product_code = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000, blank=True)
    price = models.DecimalField(max_digits=15, decimal_places=2, default=0, editable=True)
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, editable=True)
    unit_of_measurement = models.CharField(max_length=10, default=None)
    balance = models.DecimalField(max_digits=15, decimal_places=3, default=0, editable=True)
    detail = models.ManyToManyField(Detail, blank=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):

        return self.title

    def get_details(self):

        return self.detail.order_by('link')