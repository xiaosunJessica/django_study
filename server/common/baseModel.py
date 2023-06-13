from django.db import models
from django.db.models.base import ModelBase


class ModelCustomName(ModelBase):
    def __new__(mcs, name, bases, attrs, **kwargs):
        table_name = f'baibao_{name}'
        if not attrs.get('Meta', None):
            attrs['Meta'] = type("Meta", (), dict(db_table=table_name))
        abstract = getattr(attrs["Meta"], 'abstract', False)
        if not hasattr(attrs["Meta"], 'db_table') and not abstract:
            setattr(attrs['Meta'], 'db_table', table_name)

        return super().__new__(mcs, name, bases, attrs, **kwargs)


class BaseModel(models.Model, metaclass=ModelCustomName):
    objects = models.Manager()
    id = models.AutoField(primary_key=True)
    create_time = models.DateTimeField(null=True, auto_now_add=True)
    update_time = models.DateTimeField(null=True, auto_now=True)

    @classmethod
    def get_fields(cls):
        fields = [field.name for field in cls._meta.get_fields()]
        return fields

    class Meta:
        abstract = True
