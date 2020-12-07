from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post
from sqlalchemy import desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///blogly"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "crispppppyyyyyyyy"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

connect_db(app)
db.create_all()


# db.create_all()


#----------------------------#
#---------| ROUTES |---------#
#----------------------------#
class Routes():
    @app.route('/')
    def index():
        """Redirect to users list"""

        return redirect('/posts')

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

        db.session.delete(user)
        db.session.commit()

        return redirect('/users')

    @app.route('/users/<int:user_id>/posts/new')
    def post_new_form(user_id):
        """Display form to handle new posts on a per user basis"""

        user = User.query.get_or_404(user_id)

        return render_template('post_new.html', user=user)

    @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
    def post_new(user_id):
        """Submit post request on form submit to add blog to db"""

        # user = User.query.get_or_404(user_id)

        title = request.form['title']
        body = request.form['body']
        post = Post(title=title, body=body, user_id=user_id)

        db.session.add(post)
        db.session.commit()

        return redirect(f"/users/{user_id}")

    @app.route('/posts/<int:post_id>')
    def posts_all(post_id):
        """Display post by a single user from user_id"""

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)

        return render_template('post.html', post=post, user=user)

    @app.route('/posts/<int:post_id>/edit')
    def post_edit_form(post_id):
        """Form to edit posts"""

        post = Post.query.get_or_404(post_id)

        return render_template('post_edit.html', post=post)

    @app.route('/posts/<int:post_id>/edit', methods=["POST"])
    def post_edit(post_id):
        """Handle editing per post ID"""

        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.body = request.form['body']

        db.session.add(post)
        db.session.commit()

        flash('Post updated successfully!')
        return render_template('post_edit.html', post=post)

    @app.route('/posts/<int:post_id>/delete', methods=["POST"])
    def post_delete(post_id):
        """Deletes a specified post"""

        post = Post.query.get_or_404(post_id)

        db.session.delete(post)
        db.session.commit()

        return redirect('/users')

    @app.route('/posts')
    def posts_list():
        """Display all posts"""

        posts = Post.query.order_by(desc(Post.created_at)).limit(5).all()

        return render_template('posts.html', posts=posts)

    # @app.errorhandler(404)
    # def page_not_found(e):
    #     """Handle page not found"""

    #     return render_template('404.html'), 404


if __name__ == "__main__":
    db.run()
