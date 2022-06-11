import flask
from data import db_session
from .users import User
from flask import request as req
from flask import jsonify
from .form import Form
from .categories import Category
from binascii import a2b_base64
from .fophoto import Form_photo

blueprint = flask.Blueprint(
    'f111_api',
    __name__,
    template_folder='templates'
)
#
#
#
#
#
# @blueprint.route('/api/chat_id_for_registration')
# def get_chat_id():
#     db_sess = db_session.create_session()
#     return {
#         'chat_id': [prof.chat_id for prof in db_sess.query(Profile).all()],
#     }
#
#
# @blueprint.route('/api/logins_for_registration')
# def post_login():
#     db_sess = db_session.create_session()
#     return {
#         'logins': [prof.login for prof in db_sess.query(Profile).all()],
#     }
#
# @blueprint.route('/api/create_new_profile', methods=['POST'])
# def create_profile():
#     if not req.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in req.json for key in
#                  ['chat_id', 'login', 'password']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     prof = Profile()
#     prof.chat_id = req.json['chat_id']
#     prof.login = req.json['login']
#     prof.set_password(req.json['password'])
#     db_sess.add(prof)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
#
# @blueprint.route('/api/create_history_post', methods=['POST'])
# def write_history():
#     if not req.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in req.json for key in
#                  ['chat_id', 'request', 'subject']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#     hist = History()
#     hist.chat_id = req.json['chat_id']
#     hist.request = req.json['request']
#     hist.subject = req.json['subject']
#     db_sess.add(hist)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
#
#
# @blueprint.route('/api/get_history/<int:chat_id>', methods=['GET'])
# def get_history(chat_id):
#     db_sess = db_session.create_session()
#     history = [hist.request for hist in db_sess.query(History).filter(History.chat_id == int(chat_id)).all()]
#     if not history:
#         return jsonify({'error': 'Not found'})
#     return jsonify(
#         {
#             'error': 'No error',
#             'history': history
#         }
#     )
#
#
# @blueprint.route('/api/get_genres/<int:chat_id>', methods=['GET'])
# def get_genre(chat_id):
#     db_sess = db_session.create_session()
#     prof = db_sess.query(Profile).filter(Profile.chat_id == int(chat_id)).first()
#     genres = prof.genres
#     return jsonify(
#         {
#             'error': 'No error',
#             'genres': genres
#         }
#     )
#
#
#
# @blueprint.route('/api/new_genres/<int:chat_id>', methods=['POST'])
# def new_genres(chat_id):
#     if not req.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in req.json for key in
#                  ['gen']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#
#     prof = db_sess.query(Profile).filter(Profile.chat_id == chat_id).first()
#     print(prof)
#     prof.genres = req.json['gen']
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
# @blueprint.route('/api/add_bookmark/<int:chat_id>', methods=['POST'])
# def new_bookmark(chat_id):
#     if not req.json:
#         return jsonify({'error': 'Empty request'})
#     elif not all(key in req.json for key in
#                  ['request']):
#         return jsonify({'error': 'Bad request'})
#     db_sess = db_session.create_session()
#
#     bm = Bookmarks()
#     bm.chat_id = int(chat_id)
#     bm.request = req.json['request']
#     db_sess.add(bm)
#     db_sess.commit()
#     return jsonify({'success': 'OK'})
#
# @blueprint.route('/api/get_last_film/<int:chat_id>', methods=['GET'])
# def get_last_film(chat_id):
#     db_sess = db_session.create_session()
#     prof = db_sess.query(History).filter(History.chat_id == int(chat_id), History.subject == 'film').all()
#     if prof:
#         return jsonify(
#         {
#             'film': prof[-1].request
#         }
#     )
#     else:
#         return jsonify(
#         {
#             'film': None
#         }
#     )


#sdefghjklekjdodjiou9dpihodaeoifdipasenfojlasejk;lcfshdfpiawskfduoasudask;fdnsdfhksev







@blueprint.route('/api/get_mf/<int:chat_id>', methods=['GET'])
def male_female(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
    cat_count = db_sess.query(Category).filter(Category.name == 'mf').first().count
    if user.now_search == 'mf':
        if cat_count == 0:
            return 'Анкет в данной категории нет'
        elif user.search_count == cat_count:
            user.search_count = 0
            db_sess.commit()

            blank = db_sess.query(Form).filter(Form.category == 'mf', Form.category_id == 0).first()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )
        else:
            blank = db_sess.query(Form).filter(Form.category == 'mf', Form.category_id == user.search_count).first()
            user.search_count += 1
            db_sess.commit()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )


@blueprint.route('/api/get_mm/<int:chat_id>', methods=['GET'])
def male_male(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
    cat_count = db_sess.query(Category).filter(Category.name == 'mm').first().count
    if user.now_search == 'mm':
        if cat_count == 0:
            return 'Анкет в данной категории нет'
        elif user.search_count == cat_count:
            user.search_count = 0
            db_sess.commit()

            blank = db_sess.query(Form).filter(Form.category == 'mm', Form.category_id == 0).first()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )
        else:
            blank = db_sess.query(Form).filter(Form.category == 'mm', Form.category_id == user.search_count).first()
            user.search_count += 1
            db_sess.commit()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )




@blueprint.route('/api/get_ff/<int:chat_id>', methods=['GET'])
def female_female(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
    cat_count = db_sess.query(Category).filter(Category.name == 'ff').first().count
    if user.now_search == 'ff':
        if cat_count == 0:
            return 'Анкет в данной категории нет'
        elif user.search_count == cat_count:
            user.search_count = 0
            db_sess.commit()

            blank = db_sess.query(Form).filter(Form.category == 'ff', Form.category_id == 0).first()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )
        else:
            blank = db_sess.query(Form).filter(Form.category == 'ff', Form.category_id == user.search_count).first()
            user.search_count += 1
            db_sess.commit()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )



@blueprint.route('/api/get_fm/<int:chat_id>', methods=['GET'])
def female_male(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
    cat_count = db_sess.query(Category).filter(Category.name == 'fm').first().count
    if user.now_search == 'fm':
        if cat_count == 0:
            return 'Анкет в данной категории нет'
        elif user.search_count == cat_count:
            user.search_count = 0
            db_sess.commit()

            blank = db_sess.query(Form).filter(Form.category == 'fm', Form.category_id == 0).first()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )
        else:
            blank = db_sess.query(Form).filter(Form.category == 'fm', Form.category_id == user.search_count).first()
            user.search_count += 1
            db_sess.commit()
            return jsonify(
                {
                    'photo': blank.photo['0'],
                    'video': blank.video['0'],
                    'description': blank.description
                }
            )


@blueprint.route('/api/check_sex/<int:chat_id>', methods=['GET'])
def check_sex(chat_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == int(chat_id)).first()
    return {'sex': user.sex}



@blueprint.route('/api/create_new_form', methods=['POST'])
def create_new_blank():
    if not req.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req.json for key in
                 ['chat_id', 'category', 'description', 'photo', 'video']):
        return jsonify({'error': 'Bad request'})
    print(req.json)
    db_sess = db_session.create_session()

    form = Form()
    form.chat_id = req.json['chat_id']

    cat = db_sess.query(Category).filter(Category.name == req.json['category']).first()
    form.category_id = cat.count
    cat.count += 1

    form.category = req.json['category']
    form.description = req.json['description']


    db_sess.add(form)
    db_sess.commit()

    return jsonify({'success': 'OK'})



@blueprint.route('/api/create_new_profile', methods=['POST'])
def create_new_profile():
    if not req.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req.json for key in
                 ['chat_id', 'sex']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.chat_id == req.json['chat_id']).first()
    if user:
        user.sex = req.json['sex']
        db_sess.commit()
    else:
        user = User()
        user.chat_id = int(req.json['chat_id'])
        user.sex = req.json['sex']
        user.search_count = 0
        db_sess.add(user)
        db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/add_photo', methods=['POST'])
def add_photo():
    print(888)
    if not req.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in req.json for key in
                 ['chat_id', 'photo']):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()

    fo = db_sess.query(Form_photo).filter(Form_photo.chat_id == int(req.json['chat_id'])).first()
    if fo:
        encoded = bytes(req.json['photo'], encoding="raw_unicode_escape")
        encoded = encoded[2:-1]
        print(len(encoded))
        print(type(encoded))

        binary_data = a2b_base64(encoded)

        fd = open(f'pho\\{req.json["chat_id"]}_{fo.count}', 'wb')
        fd.write(binary_data)

        fd.close()
        fo.count += 1
        db_sess.commit()
    else:
        fr = Form_photo()
        fr.chat_id = int(req.json['chat_id'])
        fr.count = 1
        db_sess.add(fr)
        db_sess.commit()
        encoded = bytes(req.json['photo'], encoding="raw_unicode_escape")
        encoded = encoded[2:-1]
        print(len(encoded))
        print(type(encoded))

        binary_data = a2b_base64(encoded)

        fd = open(f'pho\\{req.json["chat_id"]}_0', 'wb')
        fd.write(binary_data)

        fd.close()