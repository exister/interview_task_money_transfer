from django.db.models import fields

from ..validators import inn_validator
from ..forms.fields import INNField as INNFormField


class INNField(fields.CharField):
    default_validators = [inn_validator]

    def __init__(self, *args, **kwargs):
        kwargs['max_length'] = kwargs.get('max_length', 12)
        super(INNField, self).__init__(*args, **kwargs)

    def db_type(self, connection):
        return 'varchar(%s)' % self.max_length

    def get_internal_type(self):
        return "INNField"

    def formfield(self, **kwargs):
        defaults = {'form_class': INNFormField}
        defaults.update(kwargs)
        return super(INNField, self).formfield(**defaults)
