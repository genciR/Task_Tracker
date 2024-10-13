from flask import request,jsonify
from flask_restful import Api, Resource
from models import db, User,Task,Skill,Assignment


api=Api()
    

########### Endpoints for  the User---
class UserDetail(Resource):
    def get(self,id):
        user=User.query.get_or_404(id)
        return jsonify(user.serialize())
##get by id

class UserList(Resource):
    def get(self):
        users=User.query.all()
        return jsonify([user.serialize() for user in users])
    
##to retrive all
  
    def post(self):
        data=request.get_json()
        new_user=User(name=data['name'],email=data['email'],role=data['role'])
        db.session.add(new_user)
        db.session.commit()
        return jsonify(new_user.serialize()),201
  ##post method  


class TaskList(Resource):
    def get(self):
        tasks=Task.query.all()
        return jsonify([task.serialize() for task in tasks])

    
    def post(self):
        data = request.get_json()
        new_task=Task(
            title=data['title'],
            description=data.get('description', ''), 
            status='To-Do', 
            priority=data['priority'],
            deadline=data.get('deadline')
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify(new_task.serialize()),201


class TaskDetail(Resource):
    def get(self,id):
        task=Task.query.get_or_404(id)
        return jsonify([task.serialize()])
    
    def put(self,id):
        task=Task.query.get_or_404(id)
        data=request.get_json()
        task.title=data.get('title',task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        task.deadline=data.get('deadline',task.deadline)
        db.session.commit()
        return jsonify(task.serialize())

    def delete(self, id):
        task=Task.query.get_or_404(id)
        db.session.delete(task) 
        db.session.commit()
        return '',204

        ###assigments

class AssignmentList(Resource):
    def get(self):
        assignments = Assignment.query.all()
        return jsonify([assignment.serialize() for assignment in assignments])

    def post(self):
        data = request.get_json()
        new_assignment = Assignment(
            task_id=data['task_id'],
            user_id=data['user_id'],
            skill_match=data.get('skill_match', False)
        )
        db.session.add(new_assignment)
        db.session.commit()
        return jsonify(new_assignment.serialize()), 201



class AssignmentDetails(Resource):
    def put(self, id):
        assignment = Assignment.query.get_or_404(id)
        data = request.get_json()
        assignment.skill_match = data.get('skill_match', assignment.skill_match)
        assignment.completed_at = data.get('completed_at', assignment.completed_at)
        db.session.commit()
        return jsonify(assignment.serialize())


class SkillList(Resource):
    def get(self):
        skills = Skill.query.all()
        return jsonify([skill.serialize() for skill in skills])

    def post(self):
        data = request.get_json()
        new_skill = Skill(skill_name=data['skill_name'])
        db.session.add(new_skill)
        db.session.commit()
        return jsonify(new_skill.serialize()), 201
 
        
###the routes

def init_routes(app):
    api.add_resource(UserList, '/users')
    api.add_resource(UserDetail, '/users/<int:id>')
    api.add_resource(TaskList, '/tasks')
    api.add_resource(TaskDetail, '/tasks/<int:id>')
    api.add_resource(AssignmentList, '/assignments')
    api.add_resource(AssignmentDetails, '/assignments/<int:id>')
    api.add_resource(SkillList, '/skills')
    api.init_app(app)


