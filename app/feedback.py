from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

from app import db
from app.forms import FeedbackForm
from app.models import Feedback

feedback = Blueprint("feedback", __name__)


@feedback.route("/feedback", methods=["GET", "POST"])
@login_required
def send_feedback():
    form = FeedbackForm()

    if form.validate_on_submit():
        fb = Feedback(
            message=form.message.data,
            user_id=current_user.id
        )
        db.session.add(fb)
        db.session.commit()
        return redirect(url_for("main.dashboard"))

    return render_template("feedback.html", form=form)
