from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required, current_user
from app.models import Todo
from app import db
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@login_required
def dashboard():
    todos = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.due_date).all()
    return render_template('dashboard.html', todos=todos)

@main.route('/add', methods=['POST'])
@login_required
def add():
    title = request.form.get('title')
    due_date = request.form.get('due_date')

    todo = Todo(
        title=title,
        user_id=current_user.id,
        due_date=datetime.strptime(due_date, '%Y-%m-%dT%H:%M')
    )

    db.session.add(todo)
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/complete/<int:id>')
@login_required
def complete(id):
    todo = Todo.query.get_or_404(id)
    todo.status = 'Completed'
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/pending/<int:id>')
@login_required
def pending(id):
    todo = Todo.query.get_or_404(id)
    todo.status = 'Pending'
    db.session.commit()
    return redirect(url_for('main.dashboard'))

@main.route('/delete/<int:id>')
@login_required
def delete(id):
    todo = Todo.query.get_or_404(id)
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for('main.dashboard'))
