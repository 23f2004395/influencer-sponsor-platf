from flask import current_app as app
from flask import render_template, request, redirect, url_for
from backend.models import *


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template("login.html")
    elif request.method == 'POST':
        uname = request.form['uname']
        pwd = request.form['pwd']
        u = User.query.filter_by(username=uname).first()
        if u and pwd == u.pwd:
            if u.type == 0:
                return redirect('/admin/home')
            if u.type == 1:
                return redirect('/influencer' + str(u.name))
            if u.type == 2:
                return redirect('/sponsor' + str(u.name))
        else:
            return render_template("login.html", m="Incorrect username or password")


@app.route('/influencer_reg', methods=['GET', 'POST'])
def influ_reg():
    if request.method == 'GET':
        return render_template("influencer_reg.html")
    if request.method == 'POST':
        uname = request.form['username']
        mail = request.form['mail']
        name = request.form['name']
        niche = request.form['niche']
        instagram = request.form['insta']
        insta_flwrs = request.form['insta-flwrs']
        youtube = request.form['yt']
        yt_flwrs = request.form['yt-flwrs']
        password = request.form['pwd']
        u = User.query.filter_by(username=uname).first()
        if not u:
            new_user = User(username=uname, mail=mail, name=name, pwd=password, status='Active', type=1)
            db.session.add(new_user)
            db.session.commit()
            u = User.query.filter_by(username=uname).first()
            new_influ = Influencer(influencer_id=u.uid, niche=niche, insta_id=instagram, youtube_id=youtube,
                                   insta_flwrs=insta_flwrs,
                                   youtube_flwrs=yt_flwrs)
            db.session.add(new_influ)
            db.session.commit()
            return redirect('/influencer/' + u.name)
        else:
            return render_template('influencer_reg.html', m="User already exists! Please try again.", e=mail, n=name,
                                   ni=niche,
                                   i=instagram, y=youtube, i_f=insta_flwrs, y_f=yt_flwrs)


@app.route('/sponsor_reg', methods=['GET', 'POST'])
def sponsor_reg():
    if request.method == 'GET':
        return render_template('sponsor_reg.html')
    if request.method == 'POST':
        uname = request.form['username']
        mail = request.form['mail']
        name = request.form['name']
        bn = request.form['bn']
        it = request.form['it']
        abt = request.form['abt']
        password = request.form['pwd']
        u = User.query.filter_by(username=uname).first()
        if not u:
            new_user = User(username=uname, mail=mail, name=name, pwd=password, status='Active', type=2)
            db.session.add(new_user)
            db.session.commit()
            u = User.query.filter_by(username=uname).first()
            new_spons = Sponsor(sponsor_id=u.uid, brand_name=bn, industry_type=it, info=abt)
            db.session.add(new_spons)
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return render_template('influencer_reg.html', m="User already exists! Please try again.", e=mail, n=name,
                                   bn=bn, abt=abt)


@app.route('/influencer/<string:name>')
def influencer(name):
    u = User.query.filter_by(name=name).first()
    i = Influencer.query.filter_by(influencer_id=u.uid).first()
    return render_template('influencer_dashboard.html',influencer=i, user=u)


@app.route('/sponsor/<string:name>')
def sponsor(name):
    u = User.query.filter_by(name=name).first()
    s = Sponsor.query.filter_by(sponsor_id=u.uid).first()
    return render_template('sponsor_dashboard.html', sponsor=s, user=u)


@app.route('/admin/home')
def adminhome():
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)


@app.route('/admin/stats')
def adminstats():
    return render_template("admin_stats.html")
