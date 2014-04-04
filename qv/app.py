# coding: utf8

import json
import os
import qrcode
import StringIO

from flask import Flask, redirect, render_template, \
                  request, session, url_for

from qv.models import db, Item

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yguesswhatkeyitis'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/qv.db'

db.init_app(app)

# done
@app.route('/')
def index():
    basic = dict()
    basic['all-items'] = len(Item.query.all())
    basic['all-vaild'] = len(Item.query.filter(Item.status!=0).all())
    items = [ _transfer_item_info_to_dict(item)
             for item in Item.query.all()]
    verify_code = md5(os.urandom(50))
    return render_template('item-create.html', basic=basic, \
                           items=items, feature=verify_code)

# done
@app.route('/item/create', methods=['POST'])
def create_item():
    feature = request.form['feature']
    number = request.form['number']
    description = request.form['description']
    producer = request.form['producer']
    note = request.form['note']
    
    item = Item(feature=feature, number=number, note=note, \
                description=description, producer=producer)
    db.session.add(item)
    db.session.commit()
    return redirect(url_for('index'))

# done
@app.route('/code/<qrcode_feature>')
def get_code(qrcode_feature):
    return _build_qrcode(qrcode_feature)

# done
@app.route('/info/<qrcode_feature>')
def get_info(qrcode_feature):
    result = dict()
    item = Item.query.filter_by(feature=qrcode_feature).first()
    if item:
        if item.status==0:
            result['status'] = 'success'
            result['message'] = u'有效'
            item.status = 1
            db.session.add(item)
            db.session.commit()
        else:
            result['status'] = 'outdate'
            result['message'] = u'失效'
        result['info'] = _transfer_item_info_to_dict(item)
    else:
        result['status'] = 'error'
        result['message'] = u'不存在'
    return json.dumps(result, ensure_ascii=False, indent=2)

def md5(str):
    import hashlib
    m = hashlib.md5()
    m.update(str)
    return m.hexdigest()

def _transfer_item_info_to_dict(item):
    return dict(feature=item.feature, number=item.number, \
                description=item.description, producer=item.producer, \
                note = item.note, status=_item_status(item.status))

def _item_status(status):
    map = {
        '0': u'有效',
        '1': u'失效'
        }
    return map.get(str(status), u'错误状态')
    
def _build_qrcode(data):
    img = qrcode.make(data)
    buf = StringIO.StringIO()
    img.save(buf, 'png')
    buf = buf.getvalue()
    response = app.make_response(buf)
    response.headers['Content-Type'] = 'image/png'
    return response
    