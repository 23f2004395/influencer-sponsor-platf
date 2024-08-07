from backend.database import *


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, unique=True, nullable=False)
    mail = db.Column(db.String, unique=True, nullable=False)
    name = db.Column(db.String, nullable=False)
    pwd = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    type = db.Column(db.Integer, nullable=False)


class Influencer(db.Model):
    __tablename__ = 'influencer'
    influencer_id = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    niche = db.Column(db.String, nullable=False)
    insta_id = db.Column(db.String, unique=True)
    insta_flwrs = db.Column(db.Integer, default=0)
    youtube_id = db.Column(db.String, unique=True)
    youtube_flwrs = db.Column(db.Integer, default=0)
    adrequests = db.relationship('AdRequest', backref='influencer')


class Sponsor(db.Model):
    __tablename__ = 'sponsor'
    sponsor_id = db.Column(db.Integer, db.ForeignKey('user.uid'), primary_key=True)
    brand_name = db.Column(db.String, nullable=False)
    industry_type = db.Column(db.String, nullable=False)
    info = db.Column(db.String, nullable=False)
    total_budget = db.Column(db.Integer, default=0)
    campaign = db.relationship('Campaign', backref='sponsor')


class Campaign(db.Model):
    _tablename_ = 'campaign'
    campaign_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    description = db.Column(db.String, nullable=False)
    start_date = db.Column(db.String, nullable=False)
    end_date = db.Column(db.String, nullable=False)
    budget = db.Column(db.Double, nullable=False)
    visibility = db.Column(db.String, nullable=False)
    goals = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    validity = db.Column(db.String, nullable=False)
    sponsor_id = db.Column(db.Integer, db.ForeignKey('sponsor.sponsor_id'))
    adrequest = db.relationship('AdRequest', backref='campaign')


class AdRequest(db.Model):
    _tablename_ = 'adrequest'
    adrequest_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    campaign_id = db.Column(db.Integer,
                            db.ForeignKey('campaign.campaign_id'),
                            nullable=False)
    influencer_id = db.Column(db.Integer,
                              db.ForeignKey('influencer.influencer_id'))
    message = db.Column(db.String(200), nullable=False)
    requirements = db.Column(db.String(200), nullable=False)
    payment_amount = db.Column(db.Double, nullable=False)
    status = db.Column(db.String(100), nullable=False)  #Pending/Acepted/Rejected
    present_status = db.Column(db.String(100), nullable=False)  # Flagged or Unflagged
    response = db.Column(db.String(500))  # Influencer response
