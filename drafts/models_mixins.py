from django.db import models

class GeneralFieldsMixin(models.Model):

    class Meta:
        abstract=True

    active_object = models.BooleanField(default=True)
    marked_to_delete = models.BooleanField(default=False)

    def activate(self):
        self.active_object = True

    def deactivate(self):
        self.active_object = False

    def mark_to_delete(self):
        self.marked_to_delete = True

    def remove_delete_mark(self):
        self.marked_to_delete = False