from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from riskch.db import get_db
from riskch.compute import getTrades, calCAR

bp = Blueprint('mpool', __name__)

@bp.route('/')
def index():
    db = get_db()
    issues = db.execute(
        'SELECT *'
        ' FROM marketpool m'
        ' ORDER BY m.id ASC'
    ).fetchall()
    return render_template('mpool/index.html', issues=issues)

@bp.route('/create', methods=('GET', 'POST'))
def create():
    if request.method == 'POST':
        issue = request.form['issue']
        fromdate = request.form['from_date']
        todate = request.form['to_date']
        car25 = 0
        error = None

        if not issue:
            error = 'Issue is required.'
        
        if error is None:
            db = get_db()
            try:
                db.execute(
                    'INSERT INTO marketpool (issue, fromdate, todate, car25)'
                    ' VALUES (?, ?, ?, ?)',
                    (issue, fromdate, todate, car25)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Issue {issue} is already in the pool."
            else:
                return redirect(url_for("mpool.index"))
        flash(error)

    return render_template('mpool/create.html')

def get_issue(id,):
    oneissue = get_db().execute(
        'SELECT *'
        ' FROM marketpool m'
        ' WHERE m.id = ?',
        (id,)
    ).fetchone()

    if oneissue is None:
        abort(404, f"Issue id {id} doesn't exist.")

    return oneissue

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
def update(id):
    oneissue = get_issue(id)

    if request.method == 'POST':
        issue = request.form['issue']
        fromdate = request.form['from_date']
        todate = request.form['to_date']
        error = None

        if not issue:
            error = 'Issue is required.'

        if error is None:
            db = get_db()
            try:
                db.execute(
                    'UPDATE marketpool SET issue = ?, fromdate = ?, todate = ?'
                    ' WHERE id = ?',
                    (issue, fromdate, todate, id)
                )
                db.commit()
            except db.IntegrityError:
                error = f"Issue {issue} is already in the pool."
            else:
                return redirect(url_for("mpool.index"))
        flash(error)

    return render_template('mpool/update.html', oneissue=oneissue)

@bp.route('/<int:id>/delete', methods=('POST',))
def delete(id):
    get_issue(id)
    db = get_db()
    db.execute('DELETE FROM marketpool WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('mpool.index'))

@bp.route('/<int:id>/load', methods=('GET',))
def load(id):

    return redirect(url_for('mpool.index'))

@bp.route('/<int:id>/sim', methods=('GET',))
def sim(id):
    oneissue = get_issue(id)
    datasource = "remote"
    remoterefresh = True   
    fromdate = oneissue['fromdate']
    todate = oneissue['todate']
    error = None

    if fromdate is None or todate is None:
        error = "Time period is required."

    try:
        pnl = getTrades(oneissue, datasource, remoterefresh)
    except Exception as e:
        error = str(e)
    else:
        result = calCAR(pnl,oneissue)
        
    if error is not None:
        flash(error)
    else:
        db = get_db()
        db.execute(
            'UPDATE marketpool SET car25 = ?'
            ' WHERE id = ?',
            (result['car25'], id)
        )
        db.commit()
    return redirect(url_for('mpool.index'))