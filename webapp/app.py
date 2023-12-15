from webapp.base import create_base_app
from webapp import todo_items_api

app = create_base_app()


@app.route('/')
def hello_world():
    return {
        'message': 'hello world'
    }


app.register_blueprint(todo_items_api.api)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
