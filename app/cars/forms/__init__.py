from flask_wtf import FlaskForm
from wtforms import SubmitField, TextAreaField, validators


class create_car_form(FlaskForm):
    name = TextAreaField('Car Name',
                         [validators.DataRequired(), ],
                         description="Name of the Car")
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
                                [validators.DataRequired(), ],
                                description="You need to add any description of the car")
    image_link = TextAreaField('Link to Car Image',
                             [validators.DataRequired(), ],
                             description="Add an image to your Car")
    submit = SubmitField()
