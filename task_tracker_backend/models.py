from extensions import db ,pwd_context
from sqlalchemy.ext.hybrid import hybrid_property
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    _password=db.Column("password",db.String[255],nullable=False)
    @hybrid_property
    def password(self):
        return self._password
    @password.setter
    def password(self,value):
        self._password=pwd_context.hash(value)
    
    
    
   
    tasks = db.relationship('Assignment', backref='user', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'role': self.role,
            'tasks': [assignment.task_id for assignment in self.tasks]  
        }

class Task(db.Model):
    __tablename__ = 'tasks'  
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(20), nullable=False, default="To-Do")
    priority = db.Column(db.String(10), nullable=False)
    deadline = db.Column(db.DateTime, nullable=True)
    
    assignments = db.relationship('Assignment', backref='task', lazy=True)

    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'status': self.status,
            'priority': self.priority,
            'deadline': self.deadline.strftime("%Y-%m-%d %H:%M:%S") if self.deadline else None,
            'users': [assignment.user_id for assignment in self.assignments]  
        }

class Skill(db.Model):
    __tablename__ = 'skills'  
    id = db.Column(db.Integer, primary_key=True)
    skill_name = db.Column(db.String(50), nullable=False)

    def serialize(self):
        return {
            'id': self.id,
            'skill_name': self.skill_name
        }

class Assignment(db.Model):
    __tablename__ = 'assignments'  
    id = db.Column(db.Integer, primary_key=True)
    task_id = db.Column(db.Integer, db.ForeignKey('tasks.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    skill_match = db.Column(db.Boolean, default=False)
    assigned_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    completed_at = db.Column(db.DateTime, nullable=True)

    def serialize(self):
        return {
            'id': self.id,
            'task_id': self.task_id,
            'user_id': self.user_id,
            'skill_match': self.skill_match,
            'assigned_at': self.assigned_at.strftime("%Y-%m-%d %H:%M:%S") if self.assigned_at else None,
            'completed_at': self.completed_at.strftime("%Y-%m-%d %H:%M:%S") if self.completed_at else None
        }
