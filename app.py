from flask import Flask, render_template, flash, redirect, url_for, session, logging, request
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secrettttzzz'

db = SQLAlchemy(app)

DEFAULT_PFP = 'https://twirpz.files.wordpress.com/2015/06/twitter-avi-gender-balanced-figure.png'


#----------------------------#
#-------| DATABASES |--------#
#----------------------------#
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)

    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(db.String, nullable=False, default=DEFAULT_PFP)

    def __repr__(self):
        u = self
        return f"<User {u.id} {u.first_name} {u.last_name} {u.image_url}>"

    def full_name(self):
        return self.first_name + ' ' + self.last_name


#----------------------------#
#---------| ROUTES |---------#
#----------------------------#
class Routes():
    @app.route('/')
    def index():
        """Redirect to users list"""

        return redirect('/users')

    @app.route('/users')
    def users_list():
        """Users list"""

        users = User.query.all()
        return render_template('users.html', users=users)

    @app.route('/users/new')
    def user_new_form():
        return render_template('user_new.html')

    @app.route('/users/new', methods=["POST"])
    def user_new():
        """Create a new user with a POST request"""
        first = request.form['first']
        last = request.form['last']
        img = request.form['img'] if request.form['img'] else None

        user = User(first_name=first, last_name=last, image_url=img)

        db.session.add(user)
        db.session.commit()

        return redirect('/users')

    @app.route('/users/<int:user_id>')
    def user_details(user_id):
        """Display details on a specific user"""

        user = User.query.get_or_404(user_id)
        return render_template('user.html', user=user)

    @app.route('/users/<int:user_id>/edit')
    def user_edit(user_id):
        """Edit a user's details"""

        user = User.query.get_or_404(user_id)
        return render_template('user_edit.html', user=user)

    @app.route('/users/<int:user_id>/edit', methods=["POST"])
    def user_edit_post(user_id):
        """Send POST request on submit of user edit"""

        user = User.query.get_or_404(user_id)
        user.first_name = request.form['first_name']
        user.last_name = request.form['last_name']
        user.image_url = request.form['image_url'] if request.form['image_url'] else None

        db.session.add(user)
        db.session.commit()

        flash('User details updated successfully!')
        return redirect(f'/users/{user.id}/edit')

    @app.route('/users/<int:user_id>/delete', methods=["POST"])
    def user_delete(user_id):
        """Delete a user"""

        user = User.query.get_or_404(user_id)
        return redirect('/users')

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle page not found"""

        return render_template('404.html'), 404


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)
