from flask import Blueprint, render_template, abort, flash, redirect, url_for, current_app
from flask_login import login_required
from jinja2 import TemplateNotFound

from app import db
from app.db import db
from app.auth import admin_required
from app.db.models import Cars
from app.cars.forms import create_car_form

cars = Blueprint('cars', __name__,
                 template_folder='templates')


@cars.route('/view_inventory')
@login_required
@admin_required
def browse_cars():
    data = Cars.query.all()
    titles = [('Product id', 'id')]
    add_url = url_for('cars.add_car')

    current_app.logger.info("Browse page loading")

    return render_template('view_inventory.html',
                           data=data,
                           Cars=Cars,
                           add_url=add_url,
                           record_type="products")


@cars.route('/list_inventory')
def list_cars():
    data = Cars.query.all()
    add_url = url_for('cars.add_car')

    current_app.logger.info("Browse page loading")

    return render_template('list_inventory.html',
                           data=data,
                           Cars=Cars,
                           add_url=add_url,
                           record_type="products")


@cars.route('/car/new', methods=['GET', 'POST'])
@login_required
def add_car():
    form = create_car_form()
    if form.validate_on_submit():
        car = Cars(car_maker=form.car_maker.data,
                   model=form.model.data,
                   year=form.year.data,
                   price=form.price.data,
                   description=form.description.data,
                   image_link=form.image_link.data)
        db.session.add(car)
        db.session.commit()
        flash('Congratulations, you just added a new car', 'success')
        return redirect(url_for('cars.browse_cars'))
    # else:
    #     flash('new product')
    #     return redirect(url_for('cars.browse_cars'))
    return render_template('add_car.html', form=form)
