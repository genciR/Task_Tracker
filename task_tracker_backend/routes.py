from flask import request,jsonify
from flask_restful import Api, Resource
from models import db, User,Task,Skill,Assignment 
from schemas import UserSchema
from flask_jwt_extended import create_access_token,get_jwt_identity,jwt_required
from extensions import pwd_context


    

schema=UserSchema()
users_schema=UserSchema(many=True)
########### Endpoints for  the User---
class UserDetail(Resource):
    def get(self,id):
        from schemas import UserSchema 
        user=User.query.get_or_404(id)
        return users_schema.jsonify(user)
    


##get by id
    def put(self, id):
        data = request.get_json()
        user = User.query.get(id)
    
        if not user:
            print("User not found")
            return jsonify({"error": "User not found"}), 404

        user_data = schema.load(data) 
        user.name = data.get('name', user.name)
        user.email = data.get('email', user.email)
        user.role = data.get('role', user.role)
    
        try:
            db.session.commit()
            print("User updated successfully")
            return schema.jsonify(user), 200
        except Exception as e:
             db.session.rollback()
             print(f"Error during update: {str(e)}")
             return jsonify({"error": str(e)}), 400
        
user_schema = UserSchema()
users_schema = UserSchema(many=True)
        
class UserList(Resource):
    def get(self):
        users=User.query.all()
        return users_schema.jsonify(users)
    
##to retrive all
  
    @get_jwt_identity
    def post(self):
        current_user = get_jwt_identity()
        
        if current_user['role'] != 'admin':
            return jsonify({"error": "You do not have permission to perform this action."}), 403
        
        data = request.get_json()
        try: 
            user_data=schema.load(data)
            existing_user = User.query.filter_by(email=data['email']).first()
            if existing_user:
                return jsonify({"error": "User with this email already exists"}), 409
        ##here i have to haash password
            password=data['password']
            hashed_password=pwd_context.hash(data['password'])
       
            new_user = User(
                name=data['name'],
                  email=data['email'],
                    role=data['role'],
                    password=hashed_password
                    )
            
            db.session.add(new_user)
            db.session.commit()
            return user_schema.jsonify(new_user.serialize()), 201
        except Exception as e:
                db.session.rollback() 
                return jsonify({"error": str(e)}), 400

class UserLogin(Resource):
    def post(self):
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        # Check if the user exists
        user = User.query.filter_by(email=email).first()
        if not user or not pwd_context.verify(password, user.password):
            return jsonify({"error": "Invalid credentials"}), 401

        # Generate JWT token
        access_token = create_access_token(identity={"id": user.id, "role": user.role})
        return jsonify(access_token=access_token), 200   
    


class TaskList(Resource):

    def get(self):
        tasks=Task.query.all()
        return jsonify([task.serialize() for task in tasks])
    
    @jwt_required()
    def post(self):

        current_user=get_jwt_identity()

        if current_user['role']not in['admin','teamlead']:
            return jsonify({"error":"You do not have permission to perform this action."}),403
        
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
    @jwt_required()
    def put(self,id):
        current_user=get_jwt_identity()
        task=Task.query.get_or_404(id)

        if current_user['role'] == 'team_member' and task.user_id != current_user['id']:
            return jsonify({"error": "You can only update your own tasks."}), 403
        
        data=request.get_json()
        task.title=data.get('title',task.title)
        task.description = data.get('description', task.description)
        task.status = data.get('status', task.status)
        task.priority = data.get('priority', task.priority)
        task.deadline=data.get('deadline',task.deadline)
        db.session.commit()
        return jsonify(task.serialize()),200

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

def init_routes(api):
    api.add_resource(UserList, '/api/users')
    api.add_resource(UserDetail, '/api/users/<int:id>')
    api.add_resource(UserLogin, '/api/login') 
    api.add_resource(TaskList, '/api/tasks')
    api.add_resource(TaskDetail, '/api/tasks/<int:id>')
    api.add_resource(AssignmentList, '/api/assignments')
    api.add_resource(AssignmentDetails, '/api/assignments/<int:id>')
    api.add_resource(SkillList, '/api/skills')
  

