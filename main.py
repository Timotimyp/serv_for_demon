from flask import Flask
from flask_restful import Api, Resource, reqparse
from data import db_session
from data.categories import Category
from data.fophoto import Form_photo
from binascii import a2b_base64
from data.fovideo import Form_video
from data.form import Form
from data.users import User
import base64
from data.form_maker_user import User_maker
import os


app = Flask(__name__)
api = Api()

categories = ['mf', 'mm', 'ff', 'fm', 'massage', 'kc']


courses = {
    1: {"name": "Python", "videos": 15},
    2: {"name": "Java", "videos": 10}
}

parser = reqparse.RequestParser()
parser.add_argument("name", type=str)
parser.add_argument("videos", type=int)


class Main(Resource):
    def get(self, course_id):
        if course_id == 0:
            return courses
        else:
            return courses[course_id]

    def delete(self, course_id):
        del courses[course_id]
        return courses

    def post(self, course_id):
        courses[course_id] = parser.parse_args()
        return courses

    def put(self, course_id):
        courses[course_id] = parser.parse_args()
        return courses


parser_photo = reqparse.RequestParser()
parser_photo.add_argument("chat_id", type=int)
parser_photo.add_argument("photo", type=str)

class Photo(Resource):
    def post(self):
        req = parser_photo.parse_args()
        db_sess = db_session.create_session()

        fo = db_sess.query(User_maker).filter(User_maker.chat_id == req['chat_id']).first()

        if fo.now_red == 0:
            return 'Выбирите анкету'
        else:
            form_photo = Form_photo()
            form_photo.form_id = fo.now_red
            form_photo.photo = req['photo']
            db_sess.add(form_photo)
            db_sess.commit()
            return 'Норм'


parser_video = reqparse.RequestParser()
parser_video.add_argument("chat_id", type=int)
parser_video.add_argument("video", type=str)

class Video(Resource):
    def post(self):
        req = parser_video.parse_args()
        db_sess = db_session.create_session()

        fo = db_sess.query(User_maker).filter(User_maker.chat_id == req['chat_id']).first()

        if fo.now_red == 0:
            return 'Выбирите анкету'
        else:
            form_video = Form_video()
            form_video.form_id = fo.now_red
            form_video.video = req['video']
            db_sess.add(form_video)
            db_sess.commit()
            return 'Норм'


class Categories(Resource):
    def get(self, name, chat_id):
        if name == 'm' or name == 'f':
            if user.sex == 'male':
                name = 'm' + name
            else:
                name = 'f' + name
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
        cat = db_sess.query(Category).filter(Category.name == name).first().forms_id
        if len(cat) == 2:
            cat = []
        else:
            cat = cat[2:-2].split("', '")
            cat = list(map(lambda x: int(x), cat))
            print(cat)

        if user.now_search != name:
            user.now_search = name
            user.search_count = 0
        print(user.search_count)

        if len(cat) == 0:
            return 'Анкет в данной категории нет'
        elif user.search_count > len(cat) - 1:
            print(777)
            user.search_count = 1
            db_sess.commit()

            blank = db_sess.query(Form).filter(Form.id == cat[0]).first()


            photo = db_sess.query(Form_photo).filter(Form_photo.form_id == cat[0]).first().photo
            video = db_sess.query(Form_video).filter(Form_video.form_id == cat[0]).first().video


            return {
                        'id': blank.id,
                        'photo': photo,
                        'video': video,
                        'description': blank.description
                        }
        else:




            photo = db_sess.query(Form_photo).filter(Form_photo.form_id == cat[int(user.search_count)]).first().photo
            video = db_sess.query(Form_video).filter(Form_video.form_id == cat[int(user.search_count)]).first().video
            blank = db_sess.query(Form).filter(Form.id == cat[user.search_count]).first()
            user.search_count += 1
            db_sess.commit()

            return {
                        'id': blank.id,
                        'photo': photo,
                        'video': video,
                        'description': blank.description
                        }



parser_profile = reqparse.RequestParser()
parser_profile.add_argument("chat_id", type=int)
parser_profile.add_argument("sex", type=str)

class Profile(Resource):
    def post(self):
        req = parser_profile.parse_args()
        db_sess = db_session.create_session()
        user = db_sess.query(User).filter(User.chat_id == req['chat_id']).first()
        if user:
            user.sex = req['sex']
            db_sess.commit()
        else:
            user = User()
            user.chat_id = int(req['chat_id'])
            user.sex = req['sex']
            user.search_count = 0
            db_sess.add(user)
            db_sess.commit()

        return {'success': 'OK'}




parser_form = reqparse.RequestParser()
parser_form.add_argument("chat_id", type=int)
parser_form.add_argument("category", type=str)
parser_form.add_argument("telephone", type=str)
parser_form.add_argument("description", type=str)


class Forms(Resource):
    def post(self):
        req = parser_form.parse_args()

        form = Form()

        form.chat_id = req['chat_id']
        form.category = req['category']
        form.telephone = req['telephone']
        form.description = req['description']

        db_sess = db_session.create_session()
        db_sess.add(form)
        db_sess.commit()


        db_sess = db_session.create_session()

        form = db_sess.query(Form).filter(Form.chat_id == req['chat_id']).all()

        user = db_sess.query(User_maker).filter(User_maker.chat_id == req['chat_id']).first()

        if not user:
            user = User_maker()
            user.chat_id = req['chat_id']
            user.now_red = form[-1].id
            db_sess.add(user)
            db_sess.commit()
        else:
            user.now_red = form[-1].id
            db_sess.add(user)
            db_sess.commit()

        return 'Успех'





class Confirm(Resource):
    def put(self, form_id):
        db_sess = db_session.create_session()

        form_cat = db_sess.query(Form).filter(Form.id == form_id).first().category

        cat = db_sess.query(Category).filter(Category.name == form_cat).first()
        gh = cat.forms_id
        if len(gh) == 2:
            cat.forms_id = str([str(form_id)])
            db_sess.commit()
        else:
            cat_necat = gh[2:-2].split("', '")
            cat_necat.append(str(form_id))
            cat.forms_id = str(cat_necat)
            db_sess.commit() # TODO

        return 'УРА'




class Telephone(Resource):
    def get(self, form_id):
        db_sess = db_session.create_session()
        form = db_sess.query(Form).filter(Form.id == form_id).first()
        return form.telephone

class All_pice(Resource):
    def get(self, form_id):
        db_sess = db_session.create_session()
        ph = db_sess.query(Form_photo).filter(Form_photo.form_id == form_id).all()
        vi = db_sess.query(Form_video).filter(Form_video.form_id == form_id).all()
        photos = []
        videos = []
        for i in ph:
            photos.append(i.photo)
        for i in vi:
            videos.append(i.video)

        return {
            "photos": photos,
            "videos": videos
                }


class Redaction(Resource):
    def put(self, chat_id, form_id):
        db_sess = db_session.create_session()
        user = db_sess.query(User_maker).filter(User_maker.chat_id == chat_id).first()
        user.now_red = form_id
        db_sess.commit()





api.add_resource(Main, "/api/courses/<int:course_id>")
api.add_resource(Photo, '/api/add_photo')
api.add_resource(Video, '/api/add_video')
api.add_resource(Categories, '/api/form/<string:name>/<int:chat_id>')
api.add_resource(Profile, '/api/create_new_profile')
api.add_resource(Forms, '/api/create_form')
api.add_resource(Confirm, '/api/confirm_form/<int:form_id>')
api.add_resource(Telephone, '/api/telephone/<int:chat_id>')
api.add_resource(All_pice, '/api/get_media/<int:chat_id>')
api.add_resource(Redaction, '/api/change_form/<int:chat_id>/<int:form_id>')
api.init_app(app)

if __name__ == "__main__":
    db_session.global_init("db/b_bd.db")
    db_sess = db_session.create_session()
    if not db_sess.query(Category).all():
        for i in categories:
            category = Category()
            category.name = i
            category.forms_id = '[]'
            db_sess.add(category)
            db_sess.commit()
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
