from app import db

class assesments(db.Model):
    #for the database initialization
    #all records with relevant datatypes
    __tablename__= 'assesments'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(500), index=True)   
    modulecode = db.Column(db.String(500), index=True, unique=True)
    deadline = db.Column(db.Date())
    description = db.Column(db.String(4000), index=True)
    status = db.Column(db.String(500), index=True)

    def __init__(self, title, modulecode, deadline, description, status):
        self.title = title
        self.modulecode = modulecode
        self.deadline = deadline
        self.description = description
        self.status = status
