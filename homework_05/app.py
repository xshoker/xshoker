from flask import Flask

from views.products import products_app

app = Flask(__name__)
app.register_blueprint(products_app, url_prefix="/about")


@app.route("/")
def root():
    return '<h1>Hello, World!</h1>'


@app.route("/items/")
@app.route("/items/<int:item_id>")
def get_item_by_id(item_id=None):
    return {'item_id': item_id}


if __name__=='__main__':
    app.run(debug=True)