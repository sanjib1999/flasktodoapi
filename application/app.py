from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from datetime import datetime
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS

app=Flask(__name__)
#allow cors origins resource
CORS(app)

#set config
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///database.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"]=False 

#swagger config
SWAGGER_URL= '/swagger'
API_URL='/static/swagger.json'
SWAGGER_BLUEPRINT=get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name':'Todo list api'
    }
)

app.register_blueprint(SWAGGER_BLUEPRINT, url_prefix=SWAGGER_URL)


#create db object
db=SQLAlchemy(app)

#create marshmallow object
ma=Marshmallow(app)

#create database
class Todolist(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    Checked=db.Column(db.Boolean, nullable=False, default=False)
    Name=db.Column(db.String(100),nullable=False)
    Type=db.Column(db.String(100),nullable=False)
    Age=db.Column(db.Integer, nullable=False)
    Description=db.Column(db.String(200),nullable=False)
    Date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self):
        return self.id

#create todolist schema

class TodolistSchema(ma.Schema):
    class Meta:
        fields=('id','Checked','Name','Type','Age','Description','Date')

#create instance of schema
todolist_schema=TodolistSchema(many=False)
todolists_schema=TodolistSchema(many=True)

#todos routes 
@app.route('/todolist',methods=['POST'])
def add_todo():
    try:
        Name=request.json['Name']
        Description=request.json['Description']
        Type=request.json['Type']
        Age=request.json['Age']

        new_todo=Todolist(Name=Name,Description=Description,Type=Type,Age=Age)
        db.session.add(new_todo)
        db.session.commit()

        return todolist_schema.jsonify(new_todo)
    except Exception as e:
        return jsonify({'error':'invalid request'})

#get todos
@app.route("/todolist",methods=["GET"])
def get_todos():
    todos=Todolist.query.all()
    result_list=todolists_schema.dump(todos)
    return jsonify(result_list)



@app.route("/todolist/<int:id>" ,methods=['GET'])
def get_todo(id):
    todo=Todolist.query.get_or_404(int(id))
    return todolist_schema.jsonify(todo)



#update todo
@app.route("/todolist/<int:id>", methods=["PUT"])
def update_todo(id):
    todo=Todolist.query.get_or_404(int(id))
   
    Name=request.json['Name']
    Description=request.json['Description']
    Type=request.json['Type']
    Age=request.json['Age']
    Checked=request.json['Checked']

    todo.Name=Name
    todo.Description=Description
    todo.Type=Type
    todo.Age=Age
    todo.Checked=Checked

    db.session.commit()
    return todolist_schema.jsonify(todo)

#delete todo
@app.route("/todolist/<int:id>" ,methods=["DELETE"])
def delete_todo(id):
    todo=Todolist.query.get_or_404(int(id))
    db.session.delete(todo)
    db.session.commit()
    return jsonify({'success':'deleted successfully'})

if __name__=="__main__":
    app.run(debug=True)