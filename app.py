from flask import Flask, render_template, request, redirect, url_for
import datetime

app = Flask(__name__)

blog_posts = [
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post.", "date": "2023-01-01"},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post.", "date": "2023-01-02"}
]


# Hilfsfunktion zum Finden eines Posts nach ID
def fetch_post_by_id(post_id):
    for post in blog_posts:
        if post["id"] == post_id:
            return post
    return None


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)


@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        new_id = max([post["id"] for post in blog_posts], default=0) + 1
        current_date = datetime.date.today().strftime('%Y-%m-%d')

        new_post = {
            "id": new_id,
            'title': title,
            'author': author,
            'content': content,
            'date': current_date,
        }

        blog_posts.append(new_post)
        return redirect(url_for('index'))

    return render_template('add.html')


@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global blog_posts
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    return redirect(url_for('index'))


@app.route('/update/<int:post_id>', methods=['GET', 'POST'])
def update(post_id):
    # Hole den Blog-Post mit der gegebenen ID
    post = fetch_post_by_id(post_id)
    if post is None:
        # Post nicht gefunden
        return "Post not found", 404

    if request.method == 'POST':
        # Aktualisiere die Post-Daten mit den Formulardaten
        post['title'] = request.form.get('title')
        post['author'] = request.form.get('author')
        post['content'] = request.form.get('content')

        # Leite zur Startseite weiter
        return redirect(url_for('index'))

    # Bei GET-Anfrage: zeige das Bearbeitungsformular an
    return render_template('update.html', post=post)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)