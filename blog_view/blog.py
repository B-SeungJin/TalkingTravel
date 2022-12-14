from flask import Flask, Blueprint, request, render_template, make_response, jsonify, redirect, url_for, session
from flask_login import login_user, current_user, logout_user
from blog_control.user_mgmt import User
from blog_control.session_mgmt import BlogSession
import datetime

blog_abtest = Blueprint('blog', __name__)


@blog_abtest.route('/set_email', methods=['GET', 'POST'])
def set_email():
    if request.method == 'GET':
        # print('set_email', request.headers)
        print('set_email', request.args.get('user_email'))
        return redirect(url_for('blog.blog_talkingTravel'))
    else:
        # print('set_email', request.headers)
        # content type 이 application/json 인 경우
        # print('set_email', request.get_json())
        print('set_email', request.form['user_email'])
        user = User.create(request.form['user_email'], 'A')
        # https://docs.python.org/3/library/datetime.html#timedelta-objects
        login_user(user, remember=True, duration=datetime.timedelta(days=365))

        return redirect(url_for('blog.blog_talkingTravel'))

    # return redirect('/blog/blog_talkingTravel')
    # return make_response(jsonify(success=True), 200)


@blog_abtest.route('/logout')
def logout():
    User.delete(current_user.id)
    logout_user()
    return redirect(url_for('blog.blog_talkingTravel'))


@blog_abtest.route('/blog_talkingTravel')
def blog_talkingTravel():
    BlogSession.get_blog_page()
    if current_user.is_authenticated:
        return render_template('blog_A.html', user_email=current_user.user_email)
    else:
        webpage_name = BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'], 'anonymous', webpage_name)
        return render_template(webpage_name)
