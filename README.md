django-sortedmanytomany
=======================

> In Django, if you need to order a many to many relation you will have to do it by using inlines width a foreign key and a sorting field. If there is no need to add another field in this relation, use inlines would make the admin interface complex where a simple many to many should do the trick.

Installation
------------

```sh
pip install django-sortedmanytomany
```

Adding to installed apps
------------------------

- To use the many to many sorted field, you have to add it to your INSTALLED_APPS on your project's settings.py so the needed static files can be loaded:

```python
    INSTALLED_APPS = (
        ...
        'sortedmanytomany',
    )
```

Using SortedManyToManyField
---------------------------

- To use SortedManyToMany field, just create a field as if you were adding the default ManyToMany

```python
    from django.db import models
    from sortedmanytomany.models import SortedManyToManyField

    class Album(models.Model):
        ...
        tracks = SortedManyToManyField('Track')

    class Track(models.Model):
        ...
```

License
-------

MIT
