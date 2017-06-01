from django import forms

from ..validators import inn_validator


class INNField(forms.CharField):
    default_validators = [inn_validator]

    def clean(self, value):
        value = self.to_python(value).strip()
        return super(INNField, self).clean(value)
