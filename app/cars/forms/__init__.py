from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators


class create_car_form(FlaskForm):
    car_maker = TextAreaField('Car Maker',
                              [validators.DataRequired(), ],
                              description="Provide maker of the car")
    model = TextAreaField('Car Model',
                          [validators.DataRequired(), ],
                          description="You need add the model of the car")
    year = TextAreaField('Car Year',
                         [validators.DataRequired(), ],
                         description="Year of this Car")
    price = TextAreaField('Price',
                          [validators.DataRequired(), ],
                          description="You need add the price of this car")
    description = TextAreaField('Description',
                                description="You need to add any description of the car")
    image_link = TextAreaField('Link to Car Image',
                               [validators.DataRequired(), ],
                               description="Add an image to your Car")
    vin = TextAreaField('Vehicle Identification Number',
                        [validators.DataRequired(), ],
                        description="PLease Add the Car's Vin Number")
    submit = SubmitField()


class edit_car_form(FlaskForm):
    price = TextAreaField('Price',
                          [validators.DataRequired(), ],
                          description="You need to update the car price")
    description = TextAreaField('Description',
                                description="Add any description of the car")
    submit = SubmitField()
