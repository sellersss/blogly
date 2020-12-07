from flask import Flask, render_template, redirect, request, flash
from models import db, connect_db, User, Post, Tag, PostTag
from sqlalchemy import desc

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql://sellerscrisp:Admin123@srv-captain--postgres-db/db?blogly"
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
        tags = Tag.query.all()

        return render_template('post_new.html', user=user, tags=tags)

    @app.route('/users/<int:user_id>/posts/new', methods=["POST"])
    def post_new(user_id):
        """Submit post request on form submit to add blog to db"""

        user = User.query.get(user_id)

        # get post details from form
        title = request.form["title"]
        body = request.form["body"]

        # get tags the user checked
        tags = Tag.query.all()
        tag_ids = []
        for tag in tags:
            if request.form.get(tag.name, None):
                tag_ids.append(tag.id)

        # create post and add to db
        post = Post(title=title, body=body, user_id=user_id)
        db.session.add(post)
        db.session.commit()

        # add tags to post
        for tag_id in tag_ids:
            post_tag = PostTag(post_id=post.id, tag_id=tag_id)
            db.session.add(post_tag)
        db.session.commit()

        return redirect(f"/users/{user_id}")

    @app.route('/posts/<int:post_id>')
    def posts_all(post_id):
        """Display post by a single user from user_id"""

        post = Post.query.get_or_404(post_id)
        user = User.query.get_or_404(post.user_id)
        tags = post.tags

        return render_template('post.html', post=post, user=user, tags=tags)

    @app.route('/posts/<int:post_id>/edit')
    def post_edit_form(post_id):
        """Form to edit posts"""

        post = Post.query.get_or_404(post_id)
        tags = Tag.query.all()
        post_tag_ids = [tag.id for tag in post.tags]

        return render_template('post_edit.html', post=post, tags=tags, post_tag_ids=post_tag_ids)

    @app.route('/posts/<int:post_id>/edit', methods=["POST"])
    def post_edit(post_id):
        """Handle editing per post ID"""

        post = Post.query.get_or_404(post_id)
        post.title = request.form['title']
        post.body = request.form['body']

        db.session.add(post)
        db.session.commit()

        tags = Tag.query.all()
        post_tags = post.tags
        for tag in tags:
            # check if tag was there initially, if not add to post
            if request.form.get(tag.name, None):
                tag_added = True
                for post_tag in post_tags:
                    # don't add tag if post already has specified tag
                    if tag.id == post_tag.id:
                        tag_added = False
                if tag_added:
                    post_tag = PostTag(post_id=post.id, tag_id=tag.id)
                    db.session.add(post_tag)
            # if tag was unchecked, remove from post
            else:
                tag_removed = False
                for post_tag in post_tags:
                    # ensure tag was removed if post previously had the tag
                    if tag.id == post_tag.id:
                        tag_removed = True
                if tag_removed:
                    post_tag = PostTag.query.filter_by(
                        post_id=post.id, tag_id=tag.id).one()
                    db.session.delete(post_tag)
        db.session.commit()

        flash('Post updated successfully!')
        return redirect(f'/posts/{post_id}')

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

    @app.route('/tags')
    def tags_list():
        """Display all tags"""

        tags = Tag.query.all()

        return render_template('tags.html', tags=tags)

    @app.route('/tags/<int:tag_id>')
    def tag_details(tag_id):
        """Shows the details of a specified tag by id"""

        tag = Tag.query.get_or_404(tag_id)
        tags = Tag.query.all()
        posts = tag.posts

        return render_template('tag.html', tag=tag, tags=tags, posts=posts)

    @app.route('/tags/new')
    def tag_new_form():
        """Displays new tag form"""

        return render_template('tag_new.html')

    @app.route('/tags/new', methods=["POST"])
    def tag_new():
        """Adds new tag to database from form"""

        name = request.form['tag']
        new_tag = Tag(name=name)

        db.session.add(new_tag)
        db.session.commit()

        flash(f'{name} has been added successfully!')
        return redirect('/tags/new')

    @app.route('/tags/<int:tag_id>/edit')
    def tag_edit_form(tag_id):
        """Displays form to edit a tag"""

        tag = Tag.query.get_or_404(tag_id)

        return render_template('tag_edit.html', tag=tag)

    @app.route('/tags/<int:tag_id>/edit', methods=["POST"])
    def tag_edit(tag_id):
        """Editing functionaliy for /tag/id/edit"""

        name = request.form['tag']

        tag = Tag.query.get_or_404(tag_id)
        tag.name = name
        db.session.add(tag)
        db.session.commit()

        flash(f'{name} has been updated successfully!')

        return redirect(f'/tags/{ tag_id }/edit')

    @app.route('/tags/<int:tag_id>/delete', methods=["POST"])
    def tag_delete(tag_id):
        """Deletes a tag"""

        tag = Tag.query.get_or_404(tag_id)

        db.session.delete(tag)
        db.session.commit()

        return redirect('/tags')

    @app.errorhandler(404)
    def page_not_found(e):
        """Handle page not found"""

        return render_template('404.html'), 404


if __name__ == "__main__":
    db.run()
