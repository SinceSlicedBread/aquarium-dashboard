from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import ForeignKey

db = SQLAlchemy()

class TankSpecies(db.Model):
    __tablename__ = "tank_species"
    tank_id = db.Column(db.Integer, db.ForeignKey("tank.id"), primary_key=True)
    species_id = db.Column(db.Integer, db.ForeignKey("species.id"), primary_key=True)

class Tank(db.Model):
    __tablename__ = "tank"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    species = db.relationship("Species", secondary="tank_species", backref="tanks")

class Species(db.Model):
    __tablename__ = "species"
    id = db.Column(db.Integer, primary_key=True)
    common_name = db.Column(db.String(100), nullable=False)
    scientific_name = db.Column(db.String(100))
    temp_min = db.Column(db.Float)
    temp_max = db.Column(db.Float)
    ph_min = db.Column(db.Float)
    ph_max = db.Column(db.Float)
    gh_min = db.Column(db.Float)
    gh_max = db.Column(db.Float)
    nitrate_min = db.Column(db.Float)
    nitrate_max = db.Column(db.Float)
    source = db.Column(db.String(100))