import os
from PIL import UnidentifiedImageError
from flask import Flask, render_template, url_for, flash, redirect
from flask_uploads import configure_uploads, UploadSet, IMAGES

from config import Configuration, CURRENT_USER
from forms import MyUpdateImageForm
from utils import resize_pic

app = Flask(__name__)
config_app = Configuration()
app.config.from_object(config_app)
photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)


@app.route('/')
def index():
    form = MyUpdateImageForm()
    return render_template('index.html', title='Главная страница', current_user=CURRENT_USER, form=form)


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    try:
        form = MyUpdateImageForm()
        if form.validate_on_submit():
            delete_user_image()
            filename = resize_pic(form.image.data, 450, 450)
            user_pic = os.path.relpath(filename)
            flash('Фото было обновлено', 'success')
            return render_template('upload.html', form=form, user_pic=user_pic, current_user=CURRENT_USER,
                                   title='Обновление изображения')
    except UnidentifiedImageError:
        flash('UnidentifiedImageError - Файл не выбран!', 'error')

    flash('Выберите изображение для загрузки', 'info')
    return redirect(url_for('index'))


def delete_user_image():
    try:
        del_dir = os.listdir(config_app.UPLOADED_PHOTOS_DEST)
        for i in del_dir:
            full_path = os.path.join(config_app.UPLOADED_PHOTOS_DEST, i)
            os.unlink(full_path)
    except FileNotFoundError:
        print('Папки с текущим пользователем не существовало и она была создана!')
