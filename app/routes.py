from flask import Blueprint, render_template
from flask.views import MethodView

bp = Blueprint('main', __name__)

class IndexView(MethodView):
    def get(self):
        return render_template('index.html')

bp.add_url_rule('/', view_func=IndexView.as_view('index'))