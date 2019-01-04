from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/User/Desktop/ARAYÜZ PROGRAMLARI/TodoApp/todo.db' #oluşturduğumuz .db nin yerini söylüyoruz.
db = SQLAlchemy(app)

@app.route("/")
def index():
    todos = Todo.query.all() #Todo sınıfından oluşturduk. sözlük yapısı şeklinde dönecek.
    return render_template("index.html",todos=todos)

@app.route("/complete/<string:id>")
def completeTodo(id): #otomatik olarak gelen id olacak.
    todo = Todo.query.filter_by(id=id).first() #id si gelen id olsun.
    """if todo.complete == True:
        todo.complete = False
    else:
        todo.complete = True"""
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def deleteTodo(id):
    todo = Todo.query.filter_by(id=id).first() #id ye göre bilginin tamamını aldık.
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/add", methods = ["POST"])
def addTodo():
    title = request.form.get("title") #title değerine sahip name'i almış olduk.
    newTodo = Todo(title = title, complete = False)#tamamlanmadığı için false olarak başlattık.
    db.session.add(newTodo)
    db.session.commit()
    return redirect(url_for("index"))



class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    complete = db.Column(db.Boolean) #tamamlanmış özelliğidir. Her yeni Todo oluştuğu zaman bunlar tamamlanmamış iştir. Eğer işimizi tamamlamışsak True olacak tamamlamamışsak False olacak.
    
if __name__=="__main__":
    db.create_all() #her seferinde bir daha oluşmayacak.
    app.run(debug=True)

