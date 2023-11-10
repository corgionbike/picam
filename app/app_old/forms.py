from flask_wtf import FlaskForm
from wtforms import BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import Select, TextInput


class SettingsForm(FlaskForm):
    rotation = IntegerField('Поворот', default=180, validators=[NumberRange(min=0, max=270)])
    saturation = IntegerField('Насыщенность', default=20, validators=[NumberRange(min=-100, max=100)])
    sharpness = IntegerField('Четкость', default=10, validators=[NumberRange(min=-100, max=100)])
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
    iso = IntegerField('ISO (0-auto)', default=100, validators=[NumberRange(min=0, max=800)])
    monohrom = BooleanField('Монохром', default=False)
    auto_night = BooleanField('Авто-ночь', default=True)
    annotate_text = BooleanField('Штамп времени', default=False)
    annotate_text_size = IntegerField('Размер шрифта', default=48, validators=[NumberRange(min=0, max=64)])
