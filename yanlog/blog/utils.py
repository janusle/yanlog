from django import forms
from django.utils.safestring import mark_safe


class MarkdownTextAreaWidget(forms.widgets.Textarea):
    def render(self, name, value, attrs=None):
        """
         Hide the original textarea and add a container for EpicEditor
         to render. The content of EpicEditor will be synced from the textarea.
        """
        attrs['style'] = 'display:none'  # hide the textarea
        ta_html = (super(MarkdownTextAreaWidget, self)
                   .render(name, value, attrs))
        # add a container for EpicEditor
        return mark_safe("<div id='content_editor'></div>%s" % ta_html)
