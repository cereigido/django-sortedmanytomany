# -*- encoding: utf-8 -*-

from django.db import router, transaction
from django.db.models import ManyToManyField, signals
from django.db.models.fields.related_descriptors import create_forward_many_to_many_manager, ManyToManyDescriptor
from django.utils.functional import cached_property
from sortedmanytomany.forms import SortedModelMultipleChoiceField


def create_sorted_forward_many_to_many_manager(superclass, rel, *args, **kwargs):
    RelatedManager = create_forward_many_to_many_manager(superclass, rel, *args, **kwargs)

    class ManyRelatedManager(RelatedManager):
        def __call__(self, **kwargs):
            manager = getattr(self.model, kwargs.pop('manager'))
            manager_class = create_sorted_forward_many_to_many_manager(manager.__class__, rel, reverse)
            return manager_class(instance=self.instance)
        do_not_call_in_templates = True

        def get_queryset(self):
            qs = super(ManyRelatedManager, self).get_queryset()
            return qs.extra(order_by=['%s.%s' % (rel.through._meta.db_table, 'id', )])

        get_query_set = get_queryset

        def set(self, objs, **kwargs):
            # Choosing to clear first will ensure the order is maintained.
            kwargs['clear'] = True
            super(ManyRelatedManager, self).set(objs, **kwargs)
        set.alters_data = True

        def _add_items(self, source_field_name, target_field_name, *objs):
            new_ids = [obj.id for obj in objs]
            db = router.db_for_write(self.through, instance=self.instance)

            with transaction.atomic(using=db, savepoint=False):
                if self.reverse or source_field_name == self.source_field_name:
                    signals.m2m_changed.send(sender=self.through, action='pre_add', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=new_ids, using=db)

                self.through._default_manager.using(db).bulk_create([
                    self.through(**{
                        '%s_id' % source_field_name: self.related_val[0],
                        '%s_id' % target_field_name: obj_id,
                    })
                    for obj_id in new_ids
                ])

                if self.reverse or source_field_name == self.source_field_name:
                    signals.m2m_changed.send(sender=self.through, action='post_add', instance=self.instance, reverse=self.reverse, model=self.model, pk_set=new_ids, using=db)

    return ManyRelatedManager


class SortedManyToManyDescriptor(ManyToManyDescriptor):
    def __init__(self, field):
        super(SortedManyToManyDescriptor, self).__init__(field.remote_field)

    @cached_property
    def related_manager_cls(self):
        model = self.rel.related_model if self.reverse else self.rel.model
        return create_sorted_forward_many_to_many_manager(model._default_manager.__class__, self.rel, reverse=self.reverse,)


class SortedManyToManyField(ManyToManyField):
    def contribute_to_class(self, cls, name, **kwargs):
        super(SortedManyToManyField, self).contribute_to_class(cls, name, **kwargs)
        # Add the descriptor for the m2m relation
        setattr(cls, self.name, SortedManyToManyDescriptor(self))

    def formfield(self, **kwargs):
        defaults = {}
        defaults['form_class'] = SortedModelMultipleChoiceField
        defaults.update(kwargs)
        return super(SortedManyToManyField, self).formfield(**defaults)
