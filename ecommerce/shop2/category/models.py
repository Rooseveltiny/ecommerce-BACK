from shop2.mixins.models_mixins import AbstractGenericModel
from shop2.files.models import FilesStorage
from uuid import uuid4
from django.db import models


class Category(AbstractGenericModel, FilesStorage):

    class Meta:
        ordering = ('sorting',)

    link = models.UUIDField(default=uuid4, null=False,
                            primary_key=True, editable=True)
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=50, null=False, unique=True)
    parent = models.UUIDField(null=True)
    sorting = models.PositiveIntegerField(null=False, default=1)

    def get_pic_by_title(self, title):

        all_images = self.all_objects_files()['images']
        for image in all_images:
            if title in image['title']:
                return image['cloud_link']

    @staticmethod
    def _initializer_dict(model_object):

        output_dict = {
            'slug': model_object.slug,
            'title': model_object.title,
            'link': str(model_object.link),
            'icon': model_object.get_pic_by_title('small_icon'),
            'cat_pic': model_object.get_pic_by_title('cat_pic'),
            'kids': []
        }
        
        return output_dict

    @staticmethod
    def _get_all_parentless():
        return  Category.objects.filter(parent=None)

    @staticmethod
    def _find_all_kids(link):
        return [Category._initializer_dict(kid) for kid in Category.objects.filter(parent=link)]

    @staticmethod
    def _fill_dict_category_with_kids(categories):
        
        for cat in categories:
            cat['kids'] = Category._find_all_kids(cat['link'])
            if cat['kids']:
                Category._fill_dict_category_with_kids(cat['kids'])
        return categories

    @staticmethod
    def get_catalog_structure():

        # initializer all mother's categories
        all_mothers = Category._get_all_parentless()
        all_mothers = [Category._initializer_dict(mother) for mother in all_mothers]

        # fill all tree with kids
        return Category._fill_dict_category_with_kids(all_mothers)
