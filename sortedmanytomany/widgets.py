# -*- encoding: utf-8 -*-

from copy import copy
from django import forms
from django.forms.utils import flatatt
from django.forms.widgets import Widget
from django.templatetags.static import static
from django.utils.datastructures import MultiValueDict
from django.utils.encoding import force_text
from django.utils.html import escapejs, format_html
from django.utils.safestring import mark_safe
from itertools import chain


class SortedFilteredSelectMultiple(Widget):
    allow_multiple_selected = True

    def __init__(self, verbose_name, attrs=None, choices=()):
        self.verbose_name = verbose_name
        self.is_stacked = False
        self.choices = list(choices)
        super(SortedFilteredSelectMultiple, self).__init__(attrs)

    def __deepcopy__(self, memo):
        obj = copy(self)
        obj.attrs = self.attrs.copy()
        obj.choices = copy(self.choices)
        memo[id(self)] = obj
        return obj

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'selectfilter'
        if self.is_stacked:
            attrs['class'] += 'stacked'

        if value is None:
            value = []
        final_attrs = self.build_attrs(attrs, name=name)
        output = [format_html('<select multiple="multiple"{}>', flatatt(final_attrs))]
        options = self.render_options(choices, value)
        if options:
            output.append(options)
        output.append('</select>')
        output.append('<script type="text/javascript">addEvent(window, "load", function(e) {')
        output.append('SortedSelectFilter.init("id_%s", "%s", %s); });</script>\n' % (name, escapejs(self.verbose_name), int(self.is_stacked)))
        return mark_safe(''.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            order_html = mark_safe(' data-order="%i"' % self.selected_ordered_choices.index(option_value))
        else:
            selected_html = ''
            order_html = ''
        return format_html('<option value="%s"%s%s>%s</option>' % (option_value, order_html, selected_html, option_label))

    def render_options(self, choices, selected_choices):
        self.selected_ordered_choices = [str(c) for c in selected_choices]
        selected_choices = set(force_text(v) for v in selected_choices)
        output = []
        for option_value, option_label in chain(self.choices, choices):
            if isinstance(option_label, (list, tuple)):
                output.append(format_html('<optgroup label="{}">', force_text(option_value)))
                for option in option_label:
                    output.append(self.render_option(selected_choices, *option))
                output.append('</optgroup>')
            else:
                output.append(self.render_option(selected_choices, option_value, option_label))
        return '\n'.join(output)

    def value_from_datadict(self, data, files, name):
        if isinstance(data, MultiValueDict):
            return data.getlist(name)
        return data.get(name)

    class Media:
        css = {'all': ('sortedmanytomany/css/widget.css',)}
        js = ('admin/js/core.js', 'sortedmanytomany/js/SortedSelectBox.js', 'sortedmanytomany/js/SortedSelectFilter.js')
