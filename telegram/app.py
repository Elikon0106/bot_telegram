from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///courses.db'
db = SQLAlchemy(app)

# Определяем модель Course
class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    video_link = db.Column(db.String(200), nullable=False)
    assignment_link = db.Column(db.String(200), nullable=False)

# Создаем базу данных
with app.app_context():
    db.create_all()

@app.route('/courses')
def courses_list():
    courses = Course.query.all()  # Получаем все курсы из базы данных
    return render_template('courses.html', courses=courses)

@app.route('/add_course', methods=['GET', 'POST'])
def add_course():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        video_link = request.form['video_link']
        assignment_link = request.form['assignment_link']

        new_course = Course(name=name, description=description, video_link=video_link, assignment_link=assignment_link)
        db.session.add(new_course)
        db.session.commit()
        return redirect(url_for('courses_list'))  # Перенаправляем на список курсов
    return render_template('add_course.html')

if __name__ == '__main__':
    app.run(debug=True)
