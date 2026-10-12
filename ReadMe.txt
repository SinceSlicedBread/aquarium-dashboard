# Aquarium Dashboard

A web application built with Python and Flask to help aquarium enthusiasts manage fish species and assess compatibility within community tanks. The dashboard compares species' preferred water conditions to identify overlapping ranges and calculate an overall compatibility score.

## Features

- **Species Management:** Add, edit, and remove fish species and their preferred water parameters.
- **Tank Management:** Create and manage aquariums, including adding or removing species.
- **Compatibility Analysis:** Compare temperature, pH, and general hardness (GH) requirements across species.
- **Visualisations:** Display water parameter ranges using interactive charts.
- **Compatibility Scoring:** Calculate an overall compatibility score based on overlapping environmental requirements.
- **Water Quality Assessment:** Summarise water condition compatibility for the selected tank.

## Technologies

- Python
- Flask
- Flask-SQLAlchemy
- SQLAlchemy
- SQLite
- Plotly
- HTML and CSS

## Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/SinceSlicedBread/aquarium-dashboard.git
   ```

2. Navigate to the project directory:

   ```bash
   cd aquarium-dashboard
   ```

3. Install the dependencies:

   ```bash
   pip install flask flask-sqlalchemy plotly
   ```

4. Run the application:

   ```bash
   python app.py
   ```

5. Open the local address displayed in your terminal in a web browser.

## Project Structure

- `app.py` — Flask application, routes, and dashboard logic.
- `model.py` — Database models for species and tanks.
- `services/` — Compatibility calculations and chart generation.
- `templates/` — HTML templates for the application interface.
- `instance/` — Application database storage.
- `species.csv` — Fish species data.

## Purpose

This project demonstrates web application development, relational database management, CRUD operations, data visualisation, and the implementation of domain-specific compatibility algorithms using Python.