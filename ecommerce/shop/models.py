from pytils.translit import slugify
from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from shop.models_mixins import GeneralFieldsMixin
import uuid
import re

# Create your models here.


class ModelFiles(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    owner = models.UUIDField(default=uuid.uuid4, editable=True)
    cloud_link = models.CharField(max_length=300)
    title = models.CharField(max_length=100, default='Файл', blank=True)
    image_expansions = ['jpeg', 'png', 'jpg',
                        'gif', 'tiff', 'tif', 'wbmp', 'webp', 'svg']
    files_expansions = ['txt', 'pdf', 'xlsx', 'xls',
                        'zip', 'gzip', 'doc', 'docx', 'pptx']

    @staticmethod
    def get_all_files(owner, expansions):

        all_elements = ModelFiles.objects.filter(owner=owner)
        all_found_files = [element for element in all_elements]
        all_filtered_files = []

        for found_file in all_found_files:
            for expansion in expansions:
                if re.search(expansion+'$', found_file.cloud_link):
                    all_filtered_files.append(found_file)

        return all_filtered_files

    @staticmethod
    def get_all_images(owner):
        return ModelFiles.get_all_files(owner, ModelFiles.image_expansions)

    @staticmethod
    def get_all_files_except_images(owner):
        return ModelFiles.get_all_files(owner, ModelFiles.files_expansions)


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

    def get_pic_by_title_in(self, title):

        images = ModelFiles.get_all_images(self.link)
        for i in images:
            if len(re.findall(title, i.title)):
                return i.cloud_link


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


class Detail(GeneralFieldsMixin):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    title = models.CharField(max_length=50)
    detail_group = models.ForeignKey(
        'DetailGroup', on_delete=models.CASCADE, default=None, null=True)
    slug = models.SlugField(max_length=50, null=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):

        return self.title


class Product(models.Model):

    link = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=True)
    product_code = models.CharField(max_length=30)
    title = models.CharField(max_length=100)
    description = models.CharField(
        max_length=1000, blank=True, default="Описания нет")
    price = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, editable=True)
    sale_price = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, editable=True)
    unit_of_measurement = models.CharField(max_length=10, default=None)
    balance = models.DecimalField(
        max_digits=15, decimal_places=3, default=0, editable=True)
    detail = models.ManyToManyField(Detail, blank=True)
    category = models.ForeignKey(
        'Category', on_delete=models.SET_NULL, default=None, null=True)

    def __str__(self):

        return self.title

    def get_details(self):

        return self.detail.order_by('link')

    def get_details_in_row(self):

        queryset_details = self.get_details()
        details_row = ''
        for index, detail in enumerate(queryset_details):
            complite_symbol = ' / ' if index+1 != len(queryset_details) else ''
            details_row += '{detail_group} : {detail}{complite_symbol}'.format(
                detail_group=detail.detail_group.title, detail=detail.title, complite_symbol=complite_symbol)
        return details_row

    def get_all_images(self):

        return ModelFiles.get_all_images(self.link)

    def get_all_files(self):

        return ModelFiles.get_all_files_except_images(self.link)


class FeedBack(models.Model):

    feed_back_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=250, blank=False,
                            verbose_name="Ваше имя")
    company = models.CharField(
        max_length=100, blank=True, verbose_name="Компания")
    email = models.EmailField(
        verbose_name="Электронная почта", blank=False, max_length=100)
    phone_number = models.CharField(
        verbose_name="Номер телефона", blank=False, max_length=12)
    CLIENT_TYPE = (
        (1, 'Физическое лицо'),
        (2, 'Юридическое лицо'),
    )
    client_type = models.IntegerField(
        verbose_name='Лицо', choices=CLIENT_TYPE, blank=False)


class Cart(models.Model):

    id = models.AutoField(primary_key=True)
    product = models.UUIDField(default=uuid.uuid4, editable=True)
    quantity = models.DecimalField(
        max_digits=15, decimal_places=3, default=0, editable=True)
    product_length = models.DecimalField(
        max_digits=4, decimal_places=2, default=0, editable=True, null=True)
    product_quantity = models.IntegerField(editable=True, null=True, default=1)
    price = models.DecimalField(
        max_digits=15, decimal_places=2, default=0, editable=False, null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             null=True, blank=True, on_delete=models.CASCADE)
    cart_uuid = models.UUIDField(default=uuid.uuid4, editable=True)

    def get_product_object(self):

        return Product.objects.get(link=self.product)
