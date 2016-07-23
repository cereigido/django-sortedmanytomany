# -*- encoding: utf-8 -*-

from django.contrib.admin.widgets import FilteredSelectMultiple
from django.utils.encoding import force_text
from django.utils.html import escapejs
from django.utils.safestring import mark_safe


class SortedFilteredSelectMultiple(FilteredSelectMultiple):
    def __init__(self, verbose_name, attrs=None, choices=()):
        self.verbose_name = verbose_name
        super(FilteredSelectMultiple, self).__init__(attrs, choices)

    def render(self, name, value, attrs=None, choices=()):
        if attrs is None:
            attrs = {}
        attrs['class'] = 'selectfilter'
        output = [super(FilteredSelectMultiple, self).render(name, value, attrs, choices)]
        output.append('<script type="text/javascript">addEvent(window, "load", function(e) { SortedSelectFilter.init("id_%s", "%s", 0); });</script>\n' % (name, escapejs(self.verbose_name)))
        return mark_safe(''.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        option_value = force_text(option_value)
        if option_value in selected_choices:
            selected_html = mark_safe(' selected="selected"')
            order_html = mark_safe(' data-order="%i"' % self.selected_ordered_choices.index(int(option_value)))
        else:
            selected_html = ''
            order_html = ''
        return '<option value="%s"%s%s>%s</option>' % (option_value, order_html, selected_html, option_label)

    def render_options(self, choices, selected_choices):
        self.selected_ordered_choices = selected_choices
        return super(SortedFilteredSelectMultiple, self).render_options(choices, selected_choices)

    class Media:
        css = {'all': ('sortedmanytomany/css/widget.css',)}
        js = ('admin/js/core.js', 'sortedmanytomany/js/SortedSelectBox.js', 'sortedmanytomany/js/SortedSelectFilter.js')
