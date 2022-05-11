from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import SubmitField, TextAreaField, validators


class create_product_form(FlaskForm):
    name = TextAreaField('Product Name',
                         [validators.DataRequired(), ],
                         description="You need add a product name")
    description = TextAreaField('Description',
                                [validators.DataRequired(), ],
                                description="You need to add a description")
    price = TextAreaField('Price',
                          [validators.DataRequired(), ],
                          description="You need to add a price")
    comments = TextAreaField('Comments',
                             [validators.DataRequired(), ],
                             description="You need to add a comment")
    filename = TextAreaField('Link to Image',
                             [validators.DataRequired(), ],
                             description="Add an image to your product")
    email = TextAreaField('Enter your email',
                             [validators.DataRequired(), ],
                             description="Add your email")

    submit = SubmitField()
