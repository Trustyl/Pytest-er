from flask import Flask, jsonify, request, abort

def create_app():
    app = Flask(__name__)
    todos = []
    next_id = 1

    @app.get('/todos')
    def list_todos():
        return jsonify(todos)

    @app.post('/todos')
    def add_todo():
        nonlocal next_id
        data = request.get_json()
        if not data or 'title' not in data:
            abort(400)
        todo = {'id': next_id, 'title': data['title']}
        todos.append(todo)
        next_id += 1
        return jsonify(todo), 201

    @app.put('/todos/<int:todo_id>')
    def update_todo(todo_id):
        data = request.get_json()
        if not data or 'title' not in data:
            abort(400)
        for todo in todos:
            if todo['id'] == todo_id:
                todo['title'] = data['title']
                return jsonify(todo)
        abort(404)

    @app.delete('/todos/<int:todo_id>')
    def delete_todo(todo_id):
        for idx, todo in enumerate(todos):
            if todo['id'] == todo_id:
                todos.pop(idx)
                return '', 204
        abort(404)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
