from flask import Flask, render_template, request, redirect, url_for
import datetime
app = Flask(__name__)

blog_posts =[
    {"id": 1, "author": "John Doe", "title": "First Post", "content": "This is my first post."},
    {"id": 2, "author": "Jane Doe", "title": "Second Post", "content": "This is another post."}
    # More blog posts can go here...
]


@app.route('/')
def index():
    return render_template('index.html', posts=blog_posts)



@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        # Hole die Daten aus dem Formular, die über die POST-Anfrage gesendet wurden
        title = request.form.get('title')
        author = request.form.get('author')
        content = request.form.get('content')

        # Generiere ID automatisch (anstatt vom Nutzer eingeben zu lassen)
        new_id = max([post["id"] for post in blog_posts], default=0) + 1

        # Generiere das aktuelle Datum
        # Formatieren als String YYYY-MM-DD
        current_date = datetime.date.today().strftime('%Y-%m-%d')

        # Erstelle ein neues Blog-Post-Dictionary
        new_post = {
            "id": new_id,
            'title': title,
            'author': author,
            'content': content,
            'date': current_date,
        }

        # Füge den neuen Blog-Post zur Liste hinzu
        blog_posts.append(new_post)

        # Leite den Benutzer nach dem Hinzufügen des Posts zur Startseite (index) um
        return redirect(url_for('index'))

    # Wenn die Anfrage eine GET-Anfrage ist, zeige das Formular an
    return render_template('add.html')

# Neue DELETE-Route
@app.route('/delete/<int:post_id>', methods=['POST'])
def delete(post_id):
    global blog_posts
    # Filtere den Beitrag mit der gegebenen ID heraus
    blog_posts = [post for post in blog_posts if post["id"] != post_id]
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
