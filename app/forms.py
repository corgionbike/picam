from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import Select, TextInput


class SettingsForm(FlaskForm):
    saturation = IntegerField('Насыщенность', default=40, validators=[NumberRange(min=-100, max=100)])
    sharpness = IntegerField('Четкость', default=20, validators=[NumberRange(min=-100, max=100)])
    awb_mode = SelectField('Баланс белого', coerce=str, default='auto', choices=[
        ("off", "off"),
        ("auto", "auto"),
        ("sunlight", "sunlight"),
        ("cloudy", "cloudy"),
        ("shade", "shade"),
        ("tungsten", "tungsten"),
        ("fluorescent", "fluorescent"),
        ("incandescent", "incandescent"),
        ("flash", "flash"),
        ("horizon", "horizon"),
    ])
    resolution = SelectField('Разрешение', coerce=str, default='2560x1440', choices=[
        ('1280x720', '1280x720 (HD)'),
        ('1920x1080', '1920x1080 (FHD)'),
        ('2560x1440', '2560x1440 (QHD)'),
        ('3280x2464', '3280x2464 (MAX)'),
    ])
    rotation = SelectField('Поворот', coerce=int, default=0, choices=[
        (0, '0'),
        (90, '90'),
        (180, '180'),
        (270, '270'),
    ])
    iso = SelectField('ISO', coerce=int, default=0, choices=[
        (0, '0-auto'),
        (100, '100'),
        (200, '200'),
        (300, '300'),
        (400, '400'),
        (500, '500'),
        (600, '600'),
        (700, '700'),
        (800, '800'),
    ])
    monohrom = BooleanField('Монохром', default=False)
    auto_night = BooleanField('Авто-ночь', default=True)
    annotate_text = BooleanField('Штамп времени', default=False)
    annotate_text_size = IntegerField('Размер шрифта штампа', default=48, validators=[NumberRange(min=0, max=64)])
