from flask import current_app as app
from flask import render_template, request, redirect
from backend.models import *

"""LOGIN"""


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


"""REGISTRATION"""


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
                                   bn=bn, abt=abt, it=it)


"""ADMIN"""


@app.route('/admin/home')
def adminhome():
    users = User.query.all()
    return render_template("admin_dashboard.html", users=users)


@app.route('/admin/<int:uid>', methods=['GET', 'POST'])
def change(uid):
    if request.method == 'POST':
        name = request.form.get('name', '')
        mail = request.form.get('mail', '')
        username = request.form.get('username', '')
        if User.query.filter_by(username=username).first():
            return render_template('Error.html',
                                   h="Username already exisits",
                                   m="Please type in another username",
                                   link="/admin/home")
        user = User.query.filter_by(uid=uid).first()
        user.name = name
        user.mail = mail
        user.username = username
        db.session.commit()
        return redirect('/admin/home')


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


"""INFLUENCER"""


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


@app.route('/influ/<string:name>/<int:adrequest_id>/<string:status>', methods=['GET', 'POST'])
def influencer_status(name, adrequest_id, status):
    if request.method == 'POST':
        response = request.form.get('response', '')
        print(response)
        adrequest = AdRequest.query.filter_by(adrequest_id=adrequest_id).first()
        adrequest.status = status
        adrequest.response = response
        db.session.commit()
        return redirect('/influ/' + name)


@app.route('/influ/<string:name>/search', methods=['GET', 'POST'])
def influencer_search(name):
    categories = []
    for sponsor in Sponsor.query.all():
        if sponsor.industry_type not in categories:
            categories.append(sponsor.industry_type)

    if request.method == 'POST':
        search = request.form.get('search', '')
        category = request.form.get('category', '')
        budget = request.form.get('budget', '')
        if category:
            sponsors = Sponsor.query.filter_by(industry_type=category).all()
            if budget:
                if search:
                    # category budget search
                    campaign_list = []
                    for sponsor in sponsors:
                        sponsor_user = User.query.filter_by(uid=sponsor.sponsor_id).first()
                        for campaign in sponsor.campaign:
                            if int(budget.split('-')[0]) <= campaign.budget <= int(
                                    budget.split('-')[1]) and campaign.camp_name == search:
                                campaign_list.append([campaign.camp_name, sponsor_user.name, sponsor.brand_name,
                                                      sponsor.industry_type, campaign.desc, campaign.budget,
                                                      campaign.goals])
                    if not campaign_list:
                        return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                               goback="go back", categories=categories)
                    return render_template("influencer_search.html",
                                           campaigns=campaign_list,
                                           name=name,
                                           goback="go back",
                                           categories=categories)
                # category budget no search
                campaign_list = []
                for sponsor in sponsors:
                    sponsor_user = User.query.filter_by(uid=sponsor.sponsor_id).first()
                    for campaign in sponsor.campaign:
                        if int(budget.split('-')[0]) <= campaign.budget <= int(budget.split('-')[1]):
                            campaign_list.append([campaign.camp_name, sponsor_user.name, sponsor.brand_name,
                                                  sponsor.industry_type, campaign.desc, campaign.budget,
                                                  campaign.goals])
                if not campaign_list:
                    return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                           goback="go back", categories=categories)
                return render_template("influencer_search.html",
                                       campaigns=campaign_list,
                                       name=name,
                                       goback="go back",
                                       categories=categories)

            # category no budget no search
            campaign_list = []
            for sponsor in sponsors:
                sponsor_user = User.query.filter_by(uid=sponsor.sponsor_id).first()
                for campaign in sponsor.campaign:
                    campaign_list.append([campaign.camp_name, sponsor_user.name, sponsor.brand_name,
                                          sponsor.industry_type, campaign.desc, campaign.budget,
                                          campaign.goals])
            return render_template("influencer_search.html", campaigns=campaign_list, name=name, goback="go back",
                                   categories=categories)
        if budget:
            if search:
                # budget and search
                campaigns = Campaign.query.filter_by(camp_name=search).all()
                if not campaigns:
                    return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                           goback="go back", categories=categories)
                campaign_list = []
                for campaign in campaigns:
                    sponsor_user = User.query.filter_by(uid=campaign.sponsor_id).first()
                    sponsorer = User.query.filter_by(uid=sponsor_user.sponsor_id).first()
                    if int(budget.split('-')[0]) <= campaign.budget <= int(budget.split('-')[1]):
                        campaign_list.append([campaign.camp_name, sponsor_user.name, sponsorer.brand_name,
                                              sponsorer.industry_type, campaign.desc, campaign.budget,
                                              campaign.goals])
                return render_template("influencer_search.html",
                                       campaigns=campaign_list,
                                       name=name,
                                       goback="go back",
                                       categories=categories)
            # if budget no search
            campaigns = Campaign.query.all()
            if not campaigns:
                return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                       goback="go back", categories=categories)
            campaign_list = []
            for campaign in campaigns:
                sponsor_user = User.query.filter_by(uid=campaign.sponsor_id).first()
                sponsorer = Sponsor.query.filter_by(sponsor_id=sponsor_user.uid).first()
                if int(budget.split('-')[0]) <= campaign.budget <= int(budget.split('-')[1]):
                    campaign_list.append([campaign.camp_name, sponsor_user.name, sponsorer.brand_name,
                                          sponsorer.industry_type, campaign.desc, campaign.budget,
                                          campaign.goals])
            return render_template("influencer_search.html",
                                   campaigns=campaign_list,
                                   name=name,
                                   goback="go back",
                                   categories=categories)
        if search:
            campaigns = Campaign.query.filter_by(camp_name=search).all()
            if not campaigns:
                return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                       goback="go back", categories=categories)
            campaign_list = []
            for campaign in campaigns:
                sponsor_user = User.query.filter_by(uid=campaign.sponsor_id).first()
                sponsorer = Sponsor.query.filter_by(sponsor_id=sponsor_user.uid).first()
                campaign_list.append([campaign.camp_name, sponsor_user.name, sponsorer.brand_name,
                                      sponsorer.industry_type, campaign.desc, campaign.budget,
                                      campaign.goals])
            return render_template("influencer_search.html",
                                   campaigns=campaign_list,
                                   name=name,
                                   goback="go back",
                                   categories=categories)
        return redirect('/influ/' + name + '/search')
    if request.method == "GET":
        u = User.query.filter_by(name=name).first()
        campaigns = Campaign.query.filter_by(visibility="public").all()
        if not campaigns:
            return render_template("influencer_search.html", name=name, m="No campaigns Found",
                                   goback="go back")
        campaign_list = []
        for campaign in campaigns:
            sponsor_user = User.query.filter_by(uid=campaign.sponsor_id).first()
            sponsorer = Sponsor.query.filter_by(sponsor_id=sponsor_user.uid).first()
            campaign_list.append([campaign.camp_name, sponsor_user.name, sponsorer.brand_name, sponsorer.industry_type,
                                  campaign.desc, campaign.budget, campaign.goals])
        return render_template("influencer_search.html", campaigns=campaign_list, name=name, categories=categories)


@app.route('/influ/<string:name>/profile', methods=['GET', 'POST'])
def influencer_profile(name):
    u = User.query.filter_by(name=name).first()
    influ = Influencer.query.filter_by(influencer_id=u.uid).first()
    if request.method == "POST":
        influ_name = request.form.get('name', '')
        insta_id = request.form.get('insta_id', '')
        mail = request.form.get('mail', '')
        niche = request.form.get('niche', '')
        youtube_id = request.form.get('youtube_id', '')
        insta_flwrs = request.form.get('insta_flwrs', '')
        youtube_flwrs = request.form.get('youtube_flwrs', '')
        influ.insta_id = insta_id
        influ.niche = niche
        influ.youtube_id = youtube_id
        influ.insta_flwrs = insta_flwrs
        influ.youtube_flwrs = youtube_flwrs
        db.session.commit()
        u.name = influ_name
        u.mail = mail
        db.session.commit()
        return redirect('/influ/' + str(influ_name) + '/profile')
    return render_template("influencer_profile.html", name=name, mail=u.mail, influ=influ)


"""SPONSOR"""


@app.route('/spons/<string:name>', methods=['GET', 'POST'])
def sponsor(name):
    u = User.query.filter_by(name=name).first()
    sponsor = Sponsor.query.filter_by(sponsor_id=u.uid).first()
    campaigns = Campaign.query.filter_by(sponsor_id=u.uid).all()
    if request.method == "POST":
        camp_name = request.form.get('camp_name', '')
        description = request.form.get('description', "")
        start_date = request.form.get('start_date', '')
        end_date = request.form.get('end_date', '')
        budget = request.form.get('budget', '')
        visibility = request.form.get('visibility', '')
        goals = request.form.get('goals', '')
        if camp_name == '' or description == '' or start_date == '' or end_date == '' or budget == '' or visibility == '' or goals == '':
            return render_template('Error.html',
                                   h="Please type in all required fields",
                                   link="/spons/" + name)
        if sponsor.total_budget == 0:
            return render_template('Error.html',
                                   h="Total budget is 0:",
                                   m="Please go to the profile section and enter your total budget",
                                   link="/spons/" + name + "/profile")
        if int(sponsor.total_budget) < int(budget):
            return render_template('Error.html',
                                   h="Your budget is higher than your total budget:",
                                   m="Please decrease your budget, or go to Profile to increase your total budget",
                                   link="/spons/" + name + "/profile")
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
    campaign = Campaign.query.filter_by(camp_id=camp_id).first()
    for influ in u:
        influencer = Influencer.query.filter_by(influencer_id=influ.uid).first()  # each influencer related to u
        for j in influencer.adrequests:  # j is every ad request sent to that influencer by all sponsors
            if j.campaign_id == camp_id:  # if sponsor has same campaign id as the current campaign
                adlist.append([j.adrequest_id, influ.name, j.requirements, j.payment_amount, j.status, j.response])
    if request.method == "POST":
        influ = request.form.get('influencer', '')
        requirements = request.form.get('requirements', '')
        payment_amount = request.form.get('payment_amount', '')
        user = User.query.filter_by(name=influ).first()
        if influ == '' or requirements == '' or payment_amount == '':
            return render_template("Error.html",
                                   h="Please type in all required fields",
                                   link="/spons/" + name + "/adreq/" + str(camp_id))
        if not user:
            return render_template("Error.html",
                                   h="Invalid name for a user please type the right name",
                                   link="/spons/" + name + "/adreq/" + str(camp_id))
        if int(payment_amount) > int(campaign.budget):
            return render_template("Error.html",
                                   h="Payment amount exceeds budget for campaign",
                                   m="Please decreese payment amount or update your budget",
                                   link="/spons/" + name + "/adreq/" + str(camp_id))
        adrequest = AdRequest.query.filter_by(influencer_id=user.uid, campaign_id=camp_id).first()
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
    return render_template('sponsor_add_adreq.html', camp_name=campaign.camp_name, list=adlist, name=name,
                           camp_id=camp_id)


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
    niches = []
    users = User.query.filter_by(type=1).all()
    for i in users:
        influencer = Influencer.query.filter_by(influencer_id=i.uid).first()
        influencers.append(
            [i.name, influencer.niche, influencer.insta_id, influencer.insta_flwrs, influencer.youtube_id,
             influencer.youtube_flwrs])
    for influ in Influencer.query.all():
        if influ.niche not in niches:
            niches.append(influ.niche)

    if request.method == "POST":
        influencers = []
        search = request.form.get('search', '')
        niche = request.form.get('niche', '')
        insta = request.form.get('insta', '')
        yt = request.form.get('yt', '')
        if search:
            u = User.query.filter_by(name=search).first()
            influ = Influencer.query.filter_by(influencer_id=u.uid).first()
            if niche:
                if insta:
                    if yt:
                        # search niche insta and yt
                        if (influ.niche == niche and int(insta.split('-')[0]) <= influ.insta_flwrs <= int(
                                insta.split('-')[1]) and
                                int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1])):
                            influencers.append(
                                [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                 influ.youtube_flwrs])
                            return render_template("sponsor_search.html", name=name, influencers=influencers,
                                                   back="Go back", niches=niches)
                    # search niche and insta
                    if influ.niche == niche and int(insta.split('-')[0]) <= influ.insta_flwrs <= int(
                            insta.split('-')[1]):
                        influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                            influ.youtube_flwrs])
                        return render_template("sponsor_search.html", name=name, influencers=influencers,
                                               back="Go back",
                                               niches=niches)
                print("IN")
                # search and niche
                if influ.niche == niche:
                    print(niche, influ.niche)
                    influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                        influ.youtube_flwrs])
                    return render_template("sponsor_search.html", name=name, influencers=influencers, back="Go back",
                                           niches=niches)

            if insta:
                if yt:
                    # search insta and yt
                    if (int(insta.split('-')[0]) <= influ.insta_flwrs <= int(insta.split('-')[1]) and
                            int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1])):
                        influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                            influ.youtube_flwrs])
                        return render_template("sponsor_search.html", name=name, influencers=influencers,
                                               back="Go back", niches=niches)
                # search and insta
                if int(insta.split('-')[0]) <= influ.insta_flwrs <= int(insta.split('-')[1]):
                    influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                        influ.youtube_flwrs])
                    return render_template("sponsor_search.html", name=name, influencers=influencers,
                                           back="Go back", niches=niches)

            if yt:
                # search and yt
                if int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1]):
                    influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                        influ.youtube_flwrs])
                    return render_template("sponsor_search.html", name=name, influencers=influencers,
                                           back="Go back", niches=niches)
            # only search
            influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                influ.youtube_flwrs])
            return render_template("sponsor_search.html", name=name, influencers=influencers, back="Go back",
                                   niches=niches)

        if niche:
            influs = Influencer.query.filter_by(niche=niche).all()
            if insta:
                if yt:
                    # niche insta and yt
                    for influ in influs:
                        u = User.query.filter_by(uid=influ.influencer_id).first()
                        if (int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1]) and
                                int(insta.split('-')[0]) <= influ.insta_flwrs <= int(insta.split('-')[1])):
                            influencers.append(
                                [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                 influ.youtube_flwrs])
                    return render_template("sponsor_search.html", name=name, influencers=influencers,
                                           back="Go back", niches=niches)
                # niche and insta
                for influ in influs:
                    u = User.query.filter_by(uid=influ.influencer_id).first()
                    if int(insta.split('-')[0]) <= influ.insta_flwrs <= int(insta.split('-')[1]):
                        influencers.append([u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                                            influ.youtube_flwrs])
                return render_template("sponsor_search.html", name=name, influencers=influencers,
                                       back="Go back", niches=niches)
            if yt:
                # niche and yt
                for influ in influs:
                    u = User.query.filter_by(uid=influ.influencer_id).first()
                    if int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1]):
                        influencers.append(
                            [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                             influ.youtube_flwrs])
                return render_template("sponsor_search.html", name=name, influencers=influencers,
                                       back="Go back", niches=niches)
            # niche
            for influ in influs:
                u = User.query.filter_by(uid=influ.influencer_id).first()
                influencers.append(
                    [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                     influ.youtube_flwrs])
            return render_template("sponsor_search.html", name=name, influencers=influencers,
                                   back="Go back", niches=niches)

        if insta:
            influs = Influencer.query.all()
            for influ in influs:
                u = User.query.filter_by(uid=influ.influencer_id).first()
                if int(insta.split('-')[0]) <= influ.insta_flwrs <= int(insta.split('-')[1]):
                    influencers.append(
                        [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                         influ.youtube_flwrs])
            return render_template("sponsor_search.html", name=name, influencers=influencers,
                                   back="Go back", niches=niches)
        if yt:
            influs = Influencer.query.all()
            for influ in influs:
                u = User.query.filter_by(uid=influ.influencer_id).first()
                if int(yt.split('-')[0]) <= influ.youtube_flwrs <= int(yt.split('-')[1]):
                    influencers.append(
                        [u.name, influ.niche, influ.insta_id, influ.insta_flwrs, influ.youtube_id,
                         influ.youtube_flwrs])
            return render_template("sponsor_search.html", name=name, influencers=influencers,
                                   back="Go back", niches=niches)

    return render_template("sponsor_search.html", influencers=influencers, name=name, niches=niches)


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
