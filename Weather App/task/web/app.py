from flask import Flask, render_template, request, redirect, flash
from flask_migrate import Migrate
import json
import sys
import requests
import os
from models import City
from exts import db


def create_app():
    the_app = Flask(__name__)
    db.init_app(the_app)
    return the_app


app = create_app()
app.secret_key = '0'
app.app_context().push()
API_KEY = '0'
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' +\
                                        os.path.join(basedir, 'weather.db')


migrate = Migrate(app, db)
db.create_all()


# write your code here
@app.route("/")
def index():
    city_list = get_current_cities()
    return render_template('index.html', city_list=city_list)


@app.route("/add/", methods=['POST'])
def add_city():
    if request.method == 'POST':
        city_name = request.form["city_name"]

        if City.query.filter_by(name=city_name.title()).first() is not None:
            flash("The city has already been added to the list!")
        else:
            weather_dict = get_weather(city_name)

            if 'does not exist' in weather_dict:
                flash("The city doesn't exist!")
            else:
                new_city = City(name=city_name.title())
                db.session.add(new_city)
                db.session.commit()

        return redirect('/')


@app.route('/delete/<city_id>/', methods=['GET', 'POST'])
def delete_city(city_id):
    city = City.query.filter_by(id=city_id).first()
    db.session.delete(city)
    db.session.commit()
    return redirect('/')


def get_current_cities():
    cities = City.query.all()
    city_list = []

    for city in cities:
        city_dict = get_weather(city.name)
        city_dict['id'] = city.id
        city_list.append(city_dict)

    return city_list


def get_weather(city):
    page = requests.get(f'https://api.openweathermap.org/data/2.5/weather?q='
                        f'{city}&units=metric&appid={API_KEY}')
    weather_json = json.loads(page.text)

    if weather_json['cod'] == '404':
        return f'City "{city}" does not exist!'

    time_zone = weather_json['timezone']
    current_time = weather_json['dt'] + time_zone
    sun_rise_time = weather_json['sys']['sunrise'] + time_zone
    sun_set_time = weather_json['sys']['sunset'] + time_zone

    if current_time < sun_rise_time - 3600 or \
            current_time > sun_set_time + 3600:
        time = 'night'
    elif sun_rise_time + 3600 < current_time < sun_set_time - 3600:
        time = 'day'
    else:
        time = 'evening-morning'

    return {'name': weather_json['name'].upper(),
            'weather': weather_json['weather'][0]['main'],
            'temp': int(round(weather_json['main']['temp'], 0)),
            'time': time}


# don't change the following way to run flask:
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
