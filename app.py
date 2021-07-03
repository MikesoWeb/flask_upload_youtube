import os

from flask import Flask, render_template, url_for, flash, redirect
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from flask_uploads import configure_uploads, IMAGES, UploadSet, UploadNotAllowed

app = Flask(__name__)
current_user = 'Mike'
photos = UploadSet('photos', IMAGES)
app.config['SECRET_KEY'] = os.urandom(24)
app.config['UPLOADED_PHOTOS_DEST'] = f'static/user_pics/{current_user}'
configure_uploads(app, photos)



@app.route('/')
def index():
    form = MyUpdateImageForm()
    return render_template('index.html', form=form)


@app.route('/', methods=['GET', 'POST'])
def upload():
    form = MyUpdateImageForm()
    try:
        if form.validate_on_submit():
            delete_user_image()
            filename = photos.save(form.image.data)
            fn = url_for('static', filename=f'user_pics/{current_user}/{filename}')
            user_pic = f'<img src="{fn}" alt="user_pic" width=450>'
            flash('Фото было обновлено')
            return render_template('index.html', form=form, user_pic=user_pic)
    except UploadNotAllowed:
        pass
    return redirect(url_for('index'))


class MyUpdateImageForm(FlaskForm):
    image = FileField('image')
    submit = SubmitField('Обновить')


def delete_user_image():
    del_dir = os.listdir(f'static/user_pics/{current_user}')
    for i in del_dir:
        full_path = os.path.join(os.getcwd(), 'static/user_pics', current_user, i)
        os.unlink(full_path)