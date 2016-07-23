django-sortedmanytomany
=======================

> In Django, if you need to order a many to many relation you will have to do it by using inlines width a foreign key and a sorting field. If there is no need to add another field in this relation, use inlines would make the admin interface complex where a simple many to many should do the trick.

Installation
------------

```sh
pip install django-sortedmanytomany
```

Defining your settings
----------------------

- There are 2 settings you must define in your Django settings:
  - PARSE_APPLICATION_ID
  - PARSE_REST_API_KEY
- You can also provide your master key to realize operations such as creating a new Parse.com class or list your app schemas:
  - PARSE_MASTER_API_KEY

Saving your model instance to Parse.com
---------------------------------------

- To sync your model you should make it a subclass of ParseModel (that subclasses Django model)
- As soon as you do that, your model will have 3 new read-only fields: objectId, createdAt and updatedAt.
- Any time you save your model instance, it will be synced.

```python
    from parsesync.models import ParseModel

    class MyModel(ParseModel):
        pass
```

Deleting your model instance to Parse.com
-----------------------------------------

- Deleting a model instance is not made by the model class itself and to extend it is not enough.
- Everytime a content is deleted, a signal is triggered and then the magic happens.
- To make sure the signal will be expected and noticed by our app you should import it to your INSTALLED_APPS on your settings.py:

```python
    INSTALLED_APPS = (
        ...
        'parsesync',
    )
```

Using Django admin customizations
---------------------------------

- To make objectId, createdAt and updatedAt visible on your Django model change form and content list you should make your ModelAdmin a subclass of ParseAdmin. ObjectId will also be added as a searchable field on your admin.
- ParseAdmin.parse_list_display method allows you to add your list display fields right before Parse fields.

```python
    from parsesync.admin import ParseAdmin

    class ProductAdmin(ParseAdmin):
        list_display = ParseAdmin.parse_list_display('__unicode__',)
```

Bringing data from Parse.com to your local database
---------------------------------------------------

- If you already have data on your Parse.com app or some of it was edited right from Parse.com Data Browser, you would want to bring it back to your Django admin by using the manage.py command parsetodjango.
- By default, the updated date for the last content is recorded and the next time the command is called, only new data is gathered. You can avoid this behavior by using the --all flag and everything will be started over.
- You may also want to grab data from an especific model by using the flag ---model followed by your model name. If your model is called FooBar, then foobar, Foobar, FOOBAR, foobaR are valid options, this parameter is case insensitive.

```
    usage: manage.py parsetodjango [--model MODEL] [--all]

    Sync data from parse to Django

    optional arguments:
        --model MODEL         Sync only provided model name
        --all                 Query content from the beggining of time
```

License
-------

MIT
