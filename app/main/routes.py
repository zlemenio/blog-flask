from app.main import bp
from flask import render_template, request, session, redirect, url_for
from flask_login import login_required, current_user
from app.main.forms import AddTask, EditTask, DeleteTask
from app.models import TodoList, Person
from app import db


@bp.route('/')
def index():
    return render_template('index.html')


@bp.route('/profile')
@login_required
def profile():
    person = Person.query.filter_by(username=current_user.username).first()
    personTodo = person.todolist
    return render_template('profile.html', todolist=personTodo)


# Profile_edit PLUS delete hidden form
@bp.route('/profile_edit', methods=('GET', 'POST'))
@login_required
def profile_edit():
    # With Delete inside since tackle this alone would make no sense
    form = DeleteTask(request.form, meta={'csrf_context': session})
    if request.method == "POST" and form.validate():
        db.session.delete(TodoList.query.get(
            int(request.form['delete_task_id'])))
        db.session.commit()
        # take this line carefully
        return redirect(url_for('main.profile_edit'))
    person = Person.query.filter_by(username=current_user.username).first()
    personTodo = person.todolist
    return render_template('profile_edit.html', todolist=personTodo, form=form)

# Adding new task
@bp.route('/profile_add2DoList', methods=('GET', 'POST'))
@login_required
def profile_add2DoList():
    form = AddTask(request.form, meta={'csrf_context': session})
    if request.method == "POST" and form.validate():
        person = Person.query.filter_by(username=current_user.username).first()
        newTask = TodoList(
            category=request.form['category'],
            description=request.form['description'],
            status="Pending",
            person=person
        )
        db.session.add(newTask)
        db.session.commit()
        return redirect(url_for('main.profile_edit'))
    return render_template('profile_add2DoList.html', form=form)

# Task editing here
@bp.route('/profile_edit2DoList/<int:task_id>', methods=('GET', 'POST'))
@login_required
def profile_edit2DoList(task_id):
    form = EditTask(request.form, meta={'csrf_context': session})

    if request.method == "POST" and form.validate():
        task2Edit = TodoList.query.get(task_id)

        # Reassign again the value of task
        task2Edit.category = request.form['category']
        task2Edit.description = request.form['description']
        task2Edit.status = request.form['status']

        # Save them up to db
        db.session.add(task2Edit)
        db.session.commit()
        return redirect(url_for('main.profile_edit'))
    task2Render = TodoList.query.get(task_id)
    return render_template(
        'profile_edit2DoList.html',
        task=task2Render,
        defaultDescription='this.innerHTML="'+task2Render.description +'"',
        form=form)
