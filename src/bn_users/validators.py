from django.core.exceptions import ValidationError


def inn_validator(value):
    def inn_csum(value):
        k = (3, 7, 2, 4, 10, 3, 5, 9, 4, 6, 8)
        pairs = zip(k[11-len(value):], [int(x) for x in value])
        return str(sum([k * v for k, v in pairs]) % 11 % 10)

    inn_length = len(value)
    if inn_length not in (10, 12):
        raise ValidationError('Должно быть введено 10 или 12 цифр')
    elif inn_length == 10:
        if value[-1] != inn_csum(value[:-1]):
            raise ValidationError('Введен некорректный ИНН')
    elif inn_length == 12:
        if value[-2:] != inn_csum(value[:-2]) + inn_csum(value[:-1]):
            raise ValidationError('Введен некорректный ИНН')


def inn_exists(value):
    from .models import User

    if not User.objects.filter(inn=value).exists():
        raise ValidationError('Users with INN {} not found'.format(value))
