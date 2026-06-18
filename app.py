from flask import Flask, render_template, request, redirect, url_for
from model import db, Species, Tank
import plotly.graph_objects as go
from services.compatibility import (calculate_overlap, calculate_water_quality, compatibility_score)
from services.charts import create_range_chart

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///aquarium.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db.init_app(app)

with app.app_context():
    db.create_all()

def create_temperature_chart(species):
    fig = go.Figure()

    for fish in species:
        fig.add_trace(
            go.Bar(
                y=[fish.common_name],
                x=[fish.temp_max - fish.temp_min],
                base=fish.temp_min,
                orientation="h"
            )
        )
    return fig.to_html(full_html=False)


@app.route("/")
def home():
    return redirect(url_for("species_list"))


@app.route("/species")
def species_list():

    species = Species.query.order_by(Species.common_name).all()

    return render_template("species_list.html", species=species)


@app.route("/species/add", methods=["GET","POST"])
def add_species():

    if request.method == "POST":
        fish = Species(
            common_name = request.form["common_name"],
            scientific_name = request.form["scientific_name"],
            temp_min = float(request.form["temp_min"]),
            temp_max = float(request.form["temp_max"]),
            ph_min = float(request.form["ph_min"]),
            ph_max = float(request.form["ph_max"]),
            gh_min = float(request.form["gh_min"]),
            gh_max = float(request.form["gh_max"]),
            nitrate_min = float(request.form["nitrate_min"]),
            nitrate_max = float(request.form["nitrate_max"]),
            source = request.form["source"]
        )
        db.session.add(fish)
        db.session.commit()
        return redirect(url_for("species_list"))

    return render_template("species_form.html")


@app.route("/species/edit/<int:id>", methods=["GET", "POST"])
def edit_species(id):
    fish = Species.query.get_or_404(id)

    if request.method == "POST":

        fish.common_name = request.form["common_name"]
        fish.scientific_name = request.form["scientific_name"]
        fish.temp_min = float(request.form["temp_min"])
        fish.temp_max = float(request.form["temp_max"])
        fish.ph_min = float(request.form["ph_min"])
        fish.ph_max = float(request.form["ph_max"])
        fish.gh_min = float(request.form["gh_min"])
        fish.gh_max = float(request.form["gh_max"])
        fish.nitrate_min = float(request.form["nitrate_min"])
        fish.nitrate_max = float(request.form["nitrate_max"])
        fish.source = request.form["source"]

        db.session.commit()
        return redirect(url_for("species_list"))

    return render_template("species_form.html", fish=fish)


@app.route("/species/delete/<int:id>")
def delete_species(id):
    fish = Species.query.get_or_404(id)
    db.session.delete(fish)
    db.session.commit()

    return redirect(url_for("species_list"))


@app.route('/tanks')
def tank_list():
    tanks = Tank.query.order_by(Tank.name).all()

    return render_template("tank_list.html", tanks=tanks)


@app.route('/tanks/add', methods=["GET", "POST"])
def add_tank():
    if request.method == "POST":
        tank = Tank(
            name = request.form["name"],
            description = request.form["description"]
        )
        db.session.add(tank)
        db.session.commit()
        return redirect(url_for("tank_list"))

    return render_template("tank_form.html")


@app.route('/tanks/delete/<int:id>')
def delete_tank(id):
    tank = Tank.query.get_or_404(id)
    db.session.delete(tank)
    db.session.commit()

    return redirect(url_for('tank_list'))

@app.route('/tanks/<int:id>')
def tank_detail(id):
    tank = Tank.query.get_or_404(id)
    all_species = Species.query.order_by(Species.common_name).all()

    return render_template("tank_detail.html",
                           tank=tank,
                           all_species=all_species)


@app.route('/tanks/<int:tank_id>/add_species', methods=["POST"])
def add_species_to_tank(tank_id):
    tank = Tank.query.get_or_404(tank_id)
    species_id = int(request.form["species_id"])
    fish = Species.query.get_or_404(species_id)

    if fish not in tank.species:
        tank.species.append(fish)
        db.session.commit()

    return redirect(url_for("tank_detail", id=tank.id))


@app.route('/tanks/<int:id>/dashboard')
def tank_dashboard(id):
    tank = Tank.query.get_or_404(id)
    fish = tank.species

    temperature = calculate_overlap(fish, "temp")
    ph = calculate_overlap(fish, "ph")
    gh = calculate_overlap(fish, "gh")
    water_quality = calculate_water_quality(fish)
    score = compatibility_score({
        "temperature": temperature,
        "ph": ph,
        "gh": gh,
    })
    charts = {
        "temperature": create_range_chart(fish, "temp", temperature),
        "ph": create_range_chart(fish, "ph", ph),
        "gh": create_range_chart(fish, "gh", gh),
    }
    return render_template("dashboard.html",
                           tank=tank,
                           score=score,
                           temperature=temperature,
                           ph=ph,
                           gh=gh,
                           water_quality=water_quality,
                           charts=charts)


if __name__ == "__main__":
    app.run(debug=True)
