import os
import secrets

from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed

from PIL import Image, UnidentifiedImageError
from secrets import token_hex

app = Flask(__name__)
current_user = 'Mike'
photos = UploadSet('photos', IMAGES)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = f'static/user_pics/{current_user}/'
configure_uploads(app, photos)


@app.route('/')
def index():
    form = MyUpdateImageForm()
    return render_template('index.html', form=form, title='Обновление изображения')


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = MyUpdateImageForm()
    try:
        if form.validate_on_submit():
            delete_user_image()
            filename = resize_pic(form.image.data, 450, 450)
            # filename = photos.save(form.image.data)
            # filename = url_for("static", filename=f'user_pics/{current_user}/{filename}')
            user_pic = f'<img src="{filename}" alt="user_pic" width=450>'
            flash('Фото было обновлено', 'success')
            return render_template('index.html', form=form, user_pic=user_pic)
    # except UploadNotAllowed:
    #     flash('UploadNotAllowed', 'warning')
    except UnidentifiedImageError:
        flash('UnidentifiedImageError - Файл не выбран!', 'error')

    flash('Выберите изображение для загрузки', 'info')
    return redirect(url_for('index'))


class MyUpdateImageForm(FlaskForm):
    image = FileField('image')
    submit = SubmitField('Обновить')


def delete_user_image():
    del_dir = os.listdir(f'static/user_pics/{current_user}')
    for i in del_dir:
        full_path = os.path.join(os.getcwd(), 'static/user_pics/', current_user, i)
        os.unlink(full_path)


def resize_pic(pic, a, b):
    random_name_pic = secrets.token_hex(10)
    _, file_ext = os.path.splitext(pic.filename)
    picture_fn = random_name_pic + file_ext
    full_path = os.path.join('static/', 'user_pics/', current_user)
    if not os.path.exists(full_path):
        os.mkdir(full_path)
    picture_path = os.path.join(full_path, picture_fn)
    output_size = (a, b)
    image = Image.open(pic)
    image.thumbnail(output_size)
    image.save(picture_path)
    return picture_path
