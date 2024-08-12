from flask import current_app as app
from flask import render_template, request, redirect
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
                return redirect('/influ/' + str(u.name))
            if u.type == 2:
                return redirect('/spons/' + str(u.name))
        else:
            return render_template("login.html", m="Incorrect username or password. Try again!")


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
                                   insta_flwrs=int(insta_flwrs),
                                   youtube_flwrs=int(yt_flwrs))
            db.session.add(new_influ)
            db.session.commit()
            return redirect('/')
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
            return redirect('/')
        else:
            return render_template('sponsor_reg.html', m="User already exists! Please try again.", e=mail, n=name,
                                   bn=bn, abt=abt)


@app.route('/admin/home')
def adminhome():
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)


@app.route('/admin/<string:name>/unflag')
def unflag(name):
    u = User.query.filter_by(name=name).first()
    u.status = 'Active'
    db.session.commit()
    return redirect('/admin/home')


@app.route('/admin/<string:name>/flag')
def flag(name):
    u = User.query.filter_by(name=name).first()
    u.status = 'Flagged'
    db.session.commit()
    return redirect('/admin/home')


@app.route('/admin/stats')
def adminstats():
    influencer = Influencer.query.all()
    sponsor = Sponsor.query.all()
    count_influ = len(influencer)
    count_spon = len(sponsor)
    active_influ = 0
    active_spon = 0
    flag_influ = 0
    flag_spon = 0
    users = User.query.all()
    for u in users:
        if u.type == 1:
            if u.status == 'Active':
                active_influ += 1
            else:
                flag_influ += 1
        elif u.type == 2:
            if u.status == "Active":
                active_spon += 1
            else:
                flag_spon += 1

    return render_template("admin_stats.html", count_influ=count_influ, count_spon=count_spon,
                           active_influ=active_influ, flag_influ=flag_influ, active_spon=active_spon,
                           flag_spon=flag_spon)


@app.route('/admin/campadreq')
def admin_camp():
    campaigns = Campaign.query.all()
    ad_requests = AdRequest.query.all()
    campaign_list = []
    adreq_list = []
    for campaign in campaigns:
        sponsor = User.query.filter_by(uid=campaign.sponsor_id).first().name
        campaign_list.append(
            [campaign.camp_id, sponsor, campaign.camp_name, campaign.desc, campaign.start_date, campaign.end_date,
             campaign.budget, campaign.visibility, campaign.goals, campaign.status])
    return render_template("admin_campaigns.html", campaigns=campaign_list)


@app.route('/admin/campadreq/status/<int:campaign_id>')
def admin_camp_status(campaign_id):
    campaign = Campaign.query.filter_by(camp_id=campaign_id).first()
    if campaign.status == 'Active':
        campaign.status = 'Flagged'
        db.session.commit()
        return redirect('/admin/campadreq')
    campaign.status = 'Active'
    db.session.commit()
    return redirect('/admin/campadreq')


@app.route('/admin/campadreq/<int:campaign_id>')
def admin_adreq(campaign_id):
    adreqs = AdRequest.query.filter_by(campaign_id=campaign_id).all()
    sponsor_id = Campaign.query.filter_by(camp_id=campaign_id).first().sponsor_id
    sponsor = User.query.filter_by(uid=sponsor_id).first().name
    adreq_list = []
    for adreq in adreqs:
        influencer = User.query.filter_by(uid=adreq.influencer_id).first().name
        adreq_list.append([adreq.adrequest_id, influencer, adreq.requirements, adreq.payment_amount, adreq.status,
                           adreq.present_status, adreq.response])
    return render_template("admin_adreq.html", campaign_id=campaign_id, adreqs=adreq_list, sponsor=sponsor)


@app.route('/admin/campadreq/<int:campaign_id>/status/<int:adrequest_id>')
def admin_adreq_status(campaign_id, adrequest_id):
    adreq = AdRequest.query.filter_by(adrequest_id=adrequest_id).first()
    if adreq.present_status == 'Active':
        adreq.present_status = 'Flagged'
        db.session.commit()
        return redirect('/admin/campadreq/' + str(campaign_id))
    adreq.present_status = 'Active'
    db.session.commit()
    return redirect('/admin/campadreq/' + str(campaign_id))


@app.route('/influ/<string:name>', methods=['GET', 'POST'])
def influencer(name):
    u = User.query.filter_by(name=name).first()  # get influencer's info
    i = Influencer.query.filter_by(influencer_id=u.uid).first()  # get more info on influencer
    ad_requests = []
    for adreq in i.adrequests:
        sponsors = Sponsor.query.all()  # query all sponsors
        for sponsor in sponsors:
            n = User.query.filter_by(uid=sponsor.sponsor_id).first().name  # get their names for every sponsor
            for campaign in sponsor.campaign:
                if adreq.campaign_id == campaign.camp_id:  # if campaign's adrequest's id is same as the id of sponsor's
                    sponsor_name = n
                    campaign_name = campaign.camp_name
            ad_requests.append(
                [adreq.adrequest_id, sponsor_name, campaign_name, adreq.requirements, adreq.payment_amount,
                 adreq.status])
    return render_template('influencer_dashboard.html', name=name, ad_requests=ad_requests)


@app.route('/influ/<int:adrequest_id>/status/<string:status>', methods=['GET', 'POST'])
def influencer_status(adrequest_id, status="Pending"):
    response = request.form['response']
    adrequest = AdRequest.query.filter_by(adrequest_id=adrequest_id).first()
    user = User.query.filter_by(uid=adrequest.influencer_id).first()
    adrequest.status = status
    adrequest.response = response
    db.session.commit()
    return redirect('/influ/' + user.name)


@app.route('/influ/<string:name>/search', methods=['GET', 'POST'])
def influencer_search(name):
    u = User.query.filter_by(name=name).first()
    i = Influencer.query.filter_by(influencer_id=u.uid).first()
    campaigns = Campaign.query.filter_by(visibility="public").all()
    if not campaigns:
        return render_template("influencer_search.html", name=name, m="No campaigns Found",
                               goback="go back")
    if request.method == 'POST':
        search = request.form['search']
        campaigns = Campaign.query.filter_by(visibility="public", camp_name=search).all()
        if not campaigns:
            return render_template("influencer_search.html", name=name, m="No campaigns Found", goback="go back")
        for campaign in campaigns:
            sponsor = User.query.filter_by(uid=campaign.sponsor_id).first().name
            campaign_list = []
            campaign_list.append([campaign.camp_name, sponsor, campaign.desc, campaign.goals])
        return render_template("influencer_search.html", campaigns=campaign_list, name=name, goback="go back")
    campaign_list = []
    for campaign in campaigns:
        sponsor = User.query.filter_by(uid=campaign.sponsor_id).first().name
        campaign_list.append([campaign.camp_name, sponsor, campaign.desc, campaign.goals])
    return render_template("influencer_search.html", campaigns=campaign_list, name=name)


@app.route('/influ/<string:name>/profile', methods=['GET', 'POST'])
def influencer_profile(name):
    u = User.query.filter_by(name=name).first()
    influ = Influencer.query.filter_by(influencer_id=u.uid).first()
    return render_template("influencer_profile.html", name=name, mail=u.mail, influ=influ)


@app.route('/spons/<string:name>', methods=['GET', 'POST'])
def sponsor(name):
    u = User.query.filter_by(name=name).first()
    campaigns = Campaign.query.filter_by(sponsor_id=u.uid).all()
    if request.method == "POST":
        camp_name = request.form['camp_name']
        description = request.form['description']
        start_date = request.form['start_date']
        end_date = request.form['end_date']
        budget = request.form['budget']
        visibility = request.form['visibility']
        goals = request.form['goals']
        campaign = Campaign.query.filter_by(camp_name=camp_name).first()
        if campaign:
            campaign.camp_name = camp_name
            campaign.desc = description
            campaign.start_date = start_date
            campaign.end_date = end_date
            campaign.budget = budget
            campaign.visibility = visibility
            campaign.goals = goals
            db.session.commit()
            return redirect('/spons/' + name)
        newcampaign = Campaign(camp_name=camp_name, desc=description, start_date=start_date, end_date=end_date,
                               budget=budget, visibility=visibility, goals=goals, status="Active", sponsor_id=u.uid)
        db.session.add(newcampaign)
        db.session.commit()
        return redirect('/spons/' + name)
    return render_template('sponsor_dashboard.html', campaigns=campaigns, user=u, name=name)


@app.route('/spons/<string:name>/adreq/<int:camp_id>', methods=['GET', 'POST'])
def sponsor_adreq(name, camp_id):
    u = User.query.filter_by(type=1).all()  # list of users with all influencers
    adlist = []
    camp_name = Campaign.query.filter_by(camp_id=camp_id).first().camp_name
    for influ in u:
        print('influ')
        influencer = Influencer.query.filter_by(influencer_id=influ.uid).first()  # each influencer related to u
        print(influencer.adrequests)
        for j in influencer.adrequests:
            print(j.campaign_id)  # j is every ad request sent to that influencer by all sponsors
            if j.campaign_id == camp_id:# if sponsor has same campaign id as the current campaign
                adlist.append([j.adrequest_id, influ.name, j.requirements, j.payment_amount, j.status, j.response])
    if request.method == "POST":
        influ = request.form['influencer']
        requirements = request.form['requirements']
        payment_amount = request.form['payment_amount']
        user = User.query.filter_by(name=influ).first()
        if not user:
            return render_template('Error.html', m="Invalid name for a user please type the right name",
                                   link="/spons/" + name + "/adreq/" + str(
                                       camp_id))  # Invalid name for a user please type the right name
        adrequest = AdRequest.query.filter_by(influencer_id=user.uid).first()
        if adrequest:
            adrequest.requirements = requirements
            adrequest.payment_amount = payment_amount
            db.session.commit()
            return redirect('/spons/' + name + '/adreq/' + str(camp_id))
        newadrequests = AdRequest(campaign_id=camp_id, influencer_id=user.uid, requirements=requirements,
                                  payment_amount=int(payment_amount), status='Pending', present_status='Active')
        db.session.add(newadrequests)
        db.session.commit()
        return redirect('/spons/' + name + '/adreq/' + str(camp_id))
    print(adlist)
    return render_template('sponsor_add_adreq.html', camp_name=camp_name, list=adlist, name=name, camp_id=camp_id)


@app.route("/spons/<string:name>/adreq/<int:camp_id>/del/<int:adreq_id>", methods=['GET', 'POST'])
def adreq_del(name, camp_id, adreq_id):
    adreq = AdRequest.query.get(adreq_id)
    db.session.delete(adreq)
    db.session.commit()
    return redirect('/spons/' + name + '/adreq/' + str(camp_id))


@app.route("/spons/<string:name>/del/<int:camp_id>", methods=['GET', 'POST'])
def campaign_del(name, camp_id):
    adreq = AdRequest.query.filter_by(campaign_id=camp_id).all()
    if adreq:
        for i in adreq:
            db.session.delete(i)
            db.session.commit()
    camp = Campaign.query.get(camp_id)
    db.session.delete(camp)
    db.session.commit()
    return redirect('/spons/' + name)


@app.route("/spons/<string:name>/search", methods=['GET', 'POST'])
def sponsor_search(name):
    influencers = []
    users = User.query.filter_by(type=1).all()
    for i in users:
        influencer = Influencer.query.filter_by(influencer_id=i.uid).first()
        influencers.append(
            [i.name, influencer.niche, influencer.insta_id, influencer.insta_flwrs, influencer.youtube_id,
             influencer.youtube_flwrs])

    if request.method == "POST":
        influencers = []
        search = request.form['search']
        users = User.query.filter_by(type=1, name=search).all()
        for i in users:
            influencer = Influencer.query.filter_by(influencer_id=i.uid).first()
            influencers.append(
                [i.name, influencer.niche, influencer.insta_id, influencer.insta_flwrs, influencer.youtube_id,
                 influencer.youtube_flwrs])
            return render_template("sponsor_search.html", name=name, influencers=influencers, back="Go back")
        return render_template("sponsor_search.html", name=name, influencers=influencers, back="Go back")
    if influencers:
        return render_template("sponsor_search.html", influencers=influencers, name=name)
    return render_template("sponsor_search.html", influencers=influencers, name=name,
                           m={"Seems like there are no influencers"})


@app.route("/spons/<string:name>/profile", methods=['GET', 'POST'])
def sponsor_profile(name):
    u = User.query.filter_by(name=name).first()
    spons = Sponsor.query.filter_by(sponsor_id=u.uid).first()
    if request.method == "POST":
        spons_name = request.form['name']
        mail = request.form['mail']
        brand_name = request.form['brand_name']
        industry = request.form['industry']
        info = request.form['info']
        total_budget = request.form['totalBudget']
        spons.brand_name = brand_name
        spons.industry_type = industry
        spons.info = info
        spons.total_budget = total_budget
        db.session.commit()
        u.name = spons_name
        u.mail = mail
        db.session.commit()
        return redirect('/spons/' + spons_name + '/profile')
    return render_template("sponsor_profile.html", name=name, mail=u.mail, spons=spons)
