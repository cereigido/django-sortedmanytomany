# -*- encoding: utf-8 -*-

from django.forms import ModelMultipleChoiceField
from django.utils.encoding import force_text
from sortedmanytomany.widgets import SortedFilteredSelectMultiple


class SortedModelMultipleChoiceField(ModelMultipleChoiceField):
    def __init__(self, queryset, required=True, widget=None, label=None, initial=None, help_text='', *args, **kwargs):
        super(ModelMultipleChoiceField, self).__init__(queryset, None, required, widget, label, initial, help_text, *args, **kwargs)
        self.widget = SortedFilteredSelectMultiple(verbose_name=queryset.model._meta.verbose_name_plural)

    def has_changed(self, initial, data):
        if initial is None:
            initial = []
        if data is None:
            data = []
        if len(initial) != len(data):
            return True
        initial_list = [force_text(value) for value in self.prepare_value(initial)]
        data_list = [force_text(value) for value in data]
        return data_list != initial_list

    def _check_values(self, value):
        qs = super(SortedModelMultipleChoiceField, self)._check_values(value)
        ordering = 'CASE %s END' % ' '.join(['WHEN id=%s THEN %s' % (pk, i) for i, pk in enumerate(value)])
        return qs.extra(select={'ordering': ordering}, order_by=('ordering',))
