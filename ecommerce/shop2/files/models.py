from shop2.mixins.models_mixins import AbstractGenericModel
from rest_framework import serializers
from django.db import models
from uuid import uuid4
import re


class ModelFiles(AbstractGenericModel):

    link = models.UUIDField(
        primary_key=True, default=uuid4, editable=True)
    owner = models.UUIDField(default=uuid4, editable=True)
    cloud_link = models.CharField(max_length=500)
    title = models.CharField(max_length=100, default='Файл', blank=True)

class FilesStorage:

    class ObjectsFilesSerializer(serializers.ModelSerializer):
        class Meta:
            fields = ('cloud_link', 'title')
            model = ModelFiles

    look_up_owner_field = 'link'  # default look up field

    image_expansions = ['jpeg', 'png', 'jpg',
                        'gif', 'tiff', 'tif', 'wbmp', 'webp', 'svg']
    files_expansions = ['txt', 'pdf', 'xlsx', 'xls',
                        'zip', 'gzip', 'doc', 'docx', 'pptx']

    @staticmethod
    def _get_all_files(owner, expansions):

        all_elements = ModelFiles.objects.filter(owner=owner)
        all_found_files = [element for element in all_elements]
        all_filtered_files = []

        for found_file in all_found_files:
            for expansion in expansions:
                if re.search(expansion+'$', found_file.cloud_link):
                    all_filtered_files.append(found_file)

        return all_filtered_files

    def _get_files_by_expansion(self, expansions):
        return self._get_all_files(self.__dict__[self.look_up_owner_field], expansions)

    def all_objects_files(self) -> list:

        images = self._get_files_by_expansion(self.image_expansions)
        files = self._get_files_by_expansion(self.files_expansions)
        serialized_images = self.ObjectsFilesSerializer(images, many=True).data
        serialized_files = self.ObjectsFilesSerializer(files, many=True).data

        result_dict = {
            'images': serialized_images,
            'files': serialized_files,
        }

        return result_dict
