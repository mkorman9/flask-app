from flask import Blueprint

blueprint = Blueprint('healthcheck_api', __name__)


@blueprint.get('/')
def healthcheck():
    return {
        'status': 'healthy'
    }
