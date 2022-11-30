import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from liana.db import get_db

bp = Blueprint("app", __name__)


@bp.route("/")
def index():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT a.AppCode AS code, a.Algorithm AS algorithm, 0 AS lic"
        " FROM Application a"
        " ORDER BY a.AppCode ASC"
    )
    apps = cur.fetchall()
    return render_template("index.html", apps=apps)


@bp.route("/create", methods=("GET", "POST"))
def create():
    if request.method == 'POST':
        AppCode = request.form['AppCode']
        Algorithm = request.form['Algorithm']
        PrivateKey = request.form['PrivateKey']
        SignatureKey = request.form['SignatureKey']
        CreatedBy = request.form['CreatedBy']
        error = None

        if not AppCode:
            error = 'AppCode is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            cur= db.cursor(dictionary=True)
            cur.execute(
                'INSERT INTO Application (AppCode, SignatureKey, PrivateKey, Algorithm, CreatedBy)'
                ' VALUES (%s, %s, %s, %s, %s)',
                (AppCode, SignatureKey, PrivateKey, Algorithm, CreatedBy)
            )
            db.commit()
            return redirect(url_for('index'))

    return render_template('create.html')

def get_post():
    cur = get_db().cursor()
    cur.execute(
        "SELECT a.AppCode AS code, a.Algorithm AS algorithm, 0 AS lic"
        " FROM Application a"
        " ORDER BY a.AppCode ASC"
    )
    aps =cur.fetchone()

    if aps:
        return aps

@bp.route("/<appcode>")
def get_app(appcode):
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute(
        "SELECT a.AppCode AS code, a.Algorithm AS algorithm, 0 AS lic"
        " FROM Application a"
        " WHERE a.AppCode = %s",
        (appcode,)
    )
    app = cur.fetchone()
    if app:
        return app["code"]

    return "Not found", 404