import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://{}:{}@{}/{}'.format(    
    os.environ.get('DB_USER', 'your_user'),
    os.environ.get('DB_PASS', 'your_password'),
    os.environ.get('DB_HOST', 'db'),
    os.environ.get('DB_NAME', 'your_db')
)
db = SQLAlchemy(app)
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)

    def __repr__(self):
        return '<User %r>' % self.name

@app.before_first_request
def create_tables():
    db.create_all()
# end database

@app.route('/')
def hello_world():
    ret = []
    res = User.query.all()
    for user in res:
        ret.append(
            {
                'name': user.name,
                'email': user.email
            }
        )
    return jsonify(ret)   

if __name__ == '__main__':
    app.run(debug=True)