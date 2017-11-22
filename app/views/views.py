# -*- coding: utf-8 -*-

import time
from datetime import datetime

from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app
from . import main
from .. import db
from ..models import Snippet, Category


@main.route('/shutdown')
def server_shutdown():
    # if not current_app.testing:
    #     abort(404)
    shutdown = request.environ.get('werkzeug.server.shutdown')
    if not shutdown:
        abort(500)
    shutdown()
    return 'Shutting down...'


@main.route('/', methods=['GET', 'POST'])
def index():
    categories = Category.query.all()
    cats = {c.name: c.id for c in categories}
    return render_template('article.html', cname='article', cid=cats['article'], cats=cats)


@main.route('/qa')
def qa():
    categories = Category.query.all()
    cats = {c.name: c.id for c in categories}
    return render_template('qa.html', cname='qa', cid=cats['qa'], cats=cats)


@main.route('/save/<int:cid>', methods=['GET', 'POST'])
def save(cid):
    summary = request.form.get('summary', '')
    keywords = request.form.get('keywords', '')
    body = request.form.get('content_txt', '')
    body_html = request.form.get('content_html', '')
    try:
        snippet = Snippet(summary=summary, keywords=keywords, body=body, body_html=body_html, category=cid)
        db.session.add(snippet)
        flash(u'保存成功 :)')
    except:
        flash(u'保存失败 π__π')
    c = Category.query.get_or_404(cid)

    if c.name == 'qa':
        return redirect(url_for('main.qa'))
    elif c.name == 'article':
        return redirect(url_for('main.article'))


@main.route('/snippet_by_cat/<int:cid>', methods=['GET', 'POST'])
def snippet_by_cat(cid):
    page = request.args.get('page', 1, type=int)
    pagination = Snippet.query.filter_by(category=cid).order_by(Snippet.timestamp.desc()).\
        paginate(
        page, per_page=current_app.config['FLASKY_SNIPPETS_PER_PAGE'],
        error_out=False)
    categories = Category.query.all()
    snippets = pagination.items
    cats = {c.name: c.id for c in categories}
    r = ''
    for i in snippets:
        r += i.summary
        r += i.body
        r += i.body_html
        r += str(i.timestamp).rsplit('.')[0]
        r += '<br/>'
    return render_template('snippets.html', snippets=snippets, cid=cid,
                           cats=cats, pagination=pagination)


@main.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    s = Snippet.query.get_or_404(id)
    #
    r = ''
    r += s.summary
    r += s.keywords
    r += s.body
    r += s.body_html
    r += str(s.timestamp).rsplit('.')[0]
    r += '<br/>'
    # print r
    #
    cid = s.category
    categories = Category.query.all()
    cats = {c.name: c.id for c in categories}

    return render_template('edit.html', snippet=s, cats=cats, cid=cid)


@main.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    s = Snippet.query.get_or_404(id)
    summary = request.form.get('summary', '')
    keywords = request.form.get('keywords', '')
    body = request.form.get('content_txt', '')
    body_html = request.form.get('content_html', '')
    s.summary = summary
    s.keywords = keywords
    s.body = body
    s.body_html = body_html
    s.update_timestamp = datetime.utcnow()
    try:
        db.session.commit()
        flash(u'更新成功 :)')
    except:
        flash(u'更新失败 π__π')

    return redirect(url_for('main.edit', id=id))


@main.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    s = Snippet.query.get_or_404(id)
    cid = s.category
    try:
        db.session.delete(s)
        db.session.commit()
        flash(u'删除成功 :)')
    except:
        flash(u'删除失败 π__π')
    return redirect(url_for('main.snippet_by_cat', cid=cid))


