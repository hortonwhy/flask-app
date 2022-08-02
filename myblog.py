""" My blog, a Flask App """
from flask import Flask, session, flash
from flask import render_template, request, redirect, url_for
from flask_bootstrap import Bootstrap4
from lite import get_all_posts, validate_login, create_user, is_admin
from lite import get_all_users, create_post, get_author_id, get_post
from lite import delete_post, edit_post
from myforms import LoginForm, RegisterForm, PostForm


app = Flask(__name__)
app.secret_key = b"\x1aAoT\\\xcf\xa4\xb2\xf7\r\x16)\xb7h)d#\x81\xba@O\xc2\x12\xda"
bootstrap = Bootstrap4(app)


@app.route("/")
@app.route("/index")
def index():
    """ Main page of the site, as well as admin panel if admin """
    posts = get_all_posts()
    if "email" in session:
        email = session["email"]
        author_id = -1
        if "author_id" in session:
            author_id = session["author_id"]
        if is_admin(email):
            users = get_all_users()
            return render_template("admin.html", users=users, email=email, posts=posts)
        return render_template(
            "index.html", posts=posts, email=email, author_id=author_id
        )  # logged in
    return render_template("index.html", posts=posts)  # not logged in


@app.route("/about")
def about():
    """ Return a simple static about page html file """
    if "email" in session:
        email = session["email"]
        return render_template("about.html", email=email)
    return render_template("about.html",)


@app.route("/login", methods=("POST", "GET"))
def login():
    """ Login route, handles validation and session """
    if "email" in session:
        email = session["email"]
        flash("You are already logged in!")
        return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        email = request.form["email"]
        password = request.form["password"]
        if validate_login(email, password):  # use sqlite 3 to validate cred.
            session["email"] = email
            session["author_id"] = get_author_id(email=email)
            flash(f"Successfully logged in as {email}")
            return redirect(url_for("index"))
        flash("Invalid user and/or password")

    return render_template("login.html", form=form)


@app.route("/logout")
def logout():
    """ Logout route, handles poping session data """
    try:
        if session:
            session.clear()
            flash("Successfully logged out")
            return redirect(url_for("index"))
        flash("You are not logged in!")
        return redirect(url_for("index"))
    except session.NullSession:
        flash("An error occurred when trying to logout")
        return False


@app.route("/register", methods=("POST", "GET"))
def register():
    """ Register route for inserting a user, if valid to the database """
    if "email" in session:
        flash("You are already logged in, logout to make a new account")
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        fname = request.form["fname"]
        lname = request.form["lname"]
        email = request.form["email"]
        password = request.form["password"]

        if create_user(fname, lname, email, password):
            session["email"] = email
            flash(f"Successfully created user: {email}")
            return redirect(url_for("index"))
        flash("email is already in use")

    return render_template("register.html", form=form)


@app.route("/post", methods=("POST", "GET"))
def make_post():
    """ Post Route for regular users and superusers """
    if "email" in session:
        email = session["email"]
        form = PostForm()
        if form.validate_on_submit():
            author_id = get_author_id(email)
            title = request.form["title"]
            body = request.form["body"]
            if create_post(author_id, title, body):
                if "author_id" not in session:  # for first time posters
                    session["author_id"] = get_author_id(email=email)
                flash(f"Successfully Posted {title}")
                return redirect(url_for("index"))
        return render_template("post.html", form=form, email=email)
    flash("You must login to post")
    return redirect(url_for("login"))


@app.route("/delete/<int:post_id>")
def delete_post_route(post_id):
    """ Route which takes post_id from url and deletes associated post """
    if "author_id" in session:
        author_id = session["author_id"]
        post = get_post(post_id)
        if post["author"] == author_id:
            print("authorized editor")
            if delete_post(post["id"]):
                flash(f"Successfully deleted post {post['title']}")
                return redirect(url_for("index"))
        flash("You are not authorized to edit this page")
        return redirect(url_for("index"))

    flash("You must login to delete or edit posts")
    return redirect(url_for("index"))


@app.route("/edit/<int:post_id>", methods=("POST", "GET"))
def edit_post_route(post_id):
    """ Route which takes post_id from url and edits associated post from DB"""
    if "author_id" in session:
        author_id = session["author_id"]
        post = get_post(post_id)
        if post["author"] == author_id:
            # authenticated user
            form = PostForm()
            form.title.data = post["title"]
            form.body.data = post["body"]
            if form.validate_on_submit():
                title = request.form["title"]
                body = request.form["body"]
                if edit_post(post_id, title, body):
                    flash(f"Successfully Edited Post {title}")
                    return redirect(url_for("index"))
            return render_template("edit-post.html", form=form, post=post)

        flash("You are not authorized to edit this page")
        return redirect(url_for("index"))

    flash("You must login to delete or edit posts")
    return redirect(url_for("index"))
