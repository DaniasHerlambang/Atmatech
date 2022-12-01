from flask import Flask,request, jsonify, make_response, abort
from datetime import datetime, timedelta
import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from flask_sqlalchemy import SQLAlchemy
import uuid
import jwt
import os
from models import *

#---------------------------------------------------------------------- paginasi
def get_paginated_list(results, url, start, limit):
    start = int(start)
    limit = int(limit)
    count = len(results)
    if count < start or limit < 0:
        abort(404)
    # make response
    obj = {}
    obj['start'] = start
    obj['limit'] = limit
    obj['count'] = count
    # make URLs
    # make previous url
    if start == 1:
        obj['previous'] = ''
    else:
        start_copy = max(1, start - limit)
        limit_copy = start - 1
        obj['previous'] = url + '?start=%d &limit=%d' % (start_copy, limit_copy)
    # make next url
    if start + limit > count:
        obj['next'] = ''
    else:
        start_copy = start + limit
        obj['next'] = url + '?start=%d&limit=%d' % (start_copy, limit)
    # finally extract result according to bounds
    obj['results'] = results[(start - 1):(start - 1 + limit)]
    return obj

#----------------------------------------------------------------------login
@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})
    user = UserProfile.query.filter_by(username=auth.username).first()
    if not user:
        return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'publik_id' : user.publik_id, 'exp' : datetime.utcnow() + timedelta(minutes=30)}, app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})

    return make_response('Could not verify', 401, {'WWW-Authenticate' : 'Basic realm="Login required!"'})

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']

        if not token:
            return jsonify({'message' : 'Token tidak ditemukan !'}), 401

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            user_saat_ini = UserProfile.query.filter_by(publik_id=data['publik_id']).first()
        except:
            return jsonify({'message' : 'Token tidak valid !'}), 401

        return f(user_saat_ini, *args, **kwargs)

    return decorated

#---------------------------------------------------------------------- home
@app.route("/", methods=["GET"])
def home():
    data = {
        "message" : "Simpel API dibangun dengan framework Python Flask dan autentikasi JWT ",
        "aplikasi disarankan" : "postman",
        "GIT"  : "x",
        "docker"    : "x"
    }
    return jsonify(data)
    return '<h1>Hello World!</h1>'

#---------------------------------------------------------------------- book crud
@app.route('/books', methods=['POST'])
@token_required
def create_book(user_saat_ini):
    if not user_saat_ini.active:
        return jsonify({'message' : 'Tidak Dapat Menjalankan Fungsi !'})
    req_data = request.form
    title = req_data['title']
    bks = [b.serialize() for b in Book.query.all() ]
    for b in bks:
        if b['title'] == title:
            return jsonify({
                # 'error': '',
                'res': f'Error ! Book with title {title} is already in library!',
                'status': '404'
            })

    bk = Book( title = req_data['title'],
               description = req_data['description'] ,
               content = req_data['content'],
               created_by_id = UserProfile.query.get(user_saat_ini.id) ,
               )
    db.session.add(bk)
    db.session.commit()

    # new_bks = [b.serialize() for b in Book.query.filter_by(title=req_data['title'])]
    return jsonify({
        'res': bk.serialize(),
        'status': '200',
        'msg': 'Success Creating a new Book'
    })

@app.route('/books', methods=['GET'])
@token_required
def getBooks(user_saat_ini):
    bks = [b.serialize() for b in Book.query.filter_by(deleted=None) ] #menampilkan book yang belum di hapus
    # bks = [b.serialize() for b in Book.query.all() ]
    return jsonify(get_paginated_list(
        bks,
        '/books',
        start=request.args.get('start', 1),
        limit=request.args.get('limit', 10)
    ))

@app.route('/books/<book_id>', methods=['GET'])
@token_required
def detail_book(user_saat_ini, book_id):
    print(Book.query.get(book_id).serialize())
    book = [b.serialize() for b in Book.query.filter_by(id=book_id) ]
    if not book:
        return jsonify({'message' : 'Buku tidak ditemukan !'})

    return jsonify({
        'res': Book.query.get(book_id).serialize(),
        'status': '200',
        'msg': 'Success a Book available'
    })


@app.route('/books/<book_id>', methods=['PUT'])
@token_required
def update_books(user_saat_ini, book_id):
    book = Book.query.filter_by(id=book_id).first()

    if not book:
        return jsonify({'message': 'Buku tidak ditemukan !'})

    data = request.form
    for key in data:
        setattr(book,key,data[key])

    db.session.commit()
    return jsonify({
        'res': book.serialize(),
        'status': '200',
        'message': 'Customer berhasil terupdate !'
    })

@app.route('/books/<book_id>', methods=['DELETE'])
@token_required
def delete_book(user_saat_ini, book_id):
    buku = Book.query.filter_by(id=book_id).first()
    if not buku:
        return jsonify({'message' : 'Buku tidak ditemukan !'})

    book = Book.query.get(book_id)
    book.deleted = datetime.now()
    db.session.commit()

    # db.session.delete(buku)
    # db.session.commit()

    return jsonify({
        'res': book.serialize(),
        'status': '200',
        'message': 'Success Book a Deleted'
    })

if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0", port=5000, use_reloader=True)