from flask import current_app as app
from flask import render_template, request, redirect, url_for


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")


@app.route('/influencer_reg', methods=['GET','POST'])
def influ_reg():
    if request.method == 'GET':
        return render_template("influencer_reg.html")


@app.route('/sponsor_reg', methods=['GET','POST'])
def sponsor_reg():
    if request.method == 'GET':
        return render_template('sponsor_reg.html')
