from flask import Flask, render_template, request, redirect, url_for
import db
from models import Tarea

app = Flask(__name__)

@app.route("/")
def home():
    todas_las_tareas = db.session.query(Tarea).all()
    for i in todas_las_tareas:
        print(i)
    return render_template("index.html", lista_de_tareas=todas_las_tareas)

@app.route("/crear-tarea", methods=["POST"])
def crear():
    tarea = Tarea(contenido=request.form["contenido_tarea"] , hecha=False)
    db.session.add(tarea)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/tarea-hecha/<id>")
def hecha(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    #tarea = db.session.query(Tarea).filter_by(id = int(id)).first()
    tarea.hecha = not(tarea.hecha)
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/eliminar-tarea/<id>")
def eliminar(id):
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).delete()
    #tarea = db.session.query(Tarea).filter_by(id = int(id)).delete()
    db.session.commit()
    return redirect(url_for("home"))

@app.route("/editar-tarea/<id>", methods=["POST", "GET"])
def editar(id):
    if request.method == "POST":
        tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
        tarea.contenido = request.form["tarea.contenido"]

        db.session.commit()
        return redirect(url_for("home"))
    tarea = db.session.query(Tarea).filter(Tarea.id == int(id)).first()
    return render_template("update.html", tarea=tarea)

    #return redirect(url_for("home"))
if __name__ == "__main__":
    db.Base.metadata.create_all(bind=db.engine)
    app.run(debug=True)


