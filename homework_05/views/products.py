from flask import Blueprint, render_template, request, redirect, url_for
from werkzeug.exceptions import NotFound, BadRequest

products_app = Blueprint("products_app", __name__)


PRODUCTS = {
    1: 'Laptop',
    2: 'Smartphone',
    3: 'Tablet',
}

ABOUT = {
    1: 'Надёжность',
    2: 'Скорость',
    3: 'Качество'
}


@products_app.route("/", endpoint='list')
def list_products():
    return render_template('products/list.html',
                           products=PRODUCTS.items(), )


@products_app.route("/about/", endpoint='about')
def about_products():
    return render_template('products/about.html', about=ABOUT.items(), )


@products_app.route("/<int:product_id>", endpoint='details')
def get_product_by_id(product_id: int):
    product_name = PRODUCTS.get(product_id)
    if product_name is None:
        raise NotFound(f'Product with id #{product_id} not found.')
    return render_template('products/details.html',
                           product_name=product_name,
                           product_id=product_id)


@products_app.route('/add/', methods=['GET', 'POST'], endpoint='add')
def add_product():
    if request.method=='GET':
        return render_template('products/add.html')

    product_name = request.form.get("product-name")
    if not product_name:
        raise BadRequest("field product-name is required!")
    product_id = len(PRODUCTS) + 1
    PRODUCTS[product_id] = product_name
    return redirect(url_for("products_app.details", product_id=product_id))
