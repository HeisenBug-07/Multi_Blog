from myproject import app
from flask import render_template, request
from myproject.modles import Post
from sqlalchemy import desc


@app.route('/')
@app.route('/home', methods=['GET', 'POST'])
def home():
    page = request.args.get('page', 1, type=int)
    post = Post.query.order_by(desc(Post.date)).paginate(page=page, per_page=4)
    return render_template('home.html', post=post)


if __name__ == '__main__':
    app.run(debug=True)
