from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

app = Flask(__name__)

# Cấu hình kết nối MongoDB
client = MongoClient('mongodb://localhost:27017')
db = client['todo_app']
collection = db['tasks']

@app.route('/')
def index():
    tasks = collection.find()
    return render_template('index.html', tasks=tasks)

@app.route('/add', methods=['POST'])
def add_task():
    task_content = request.form.get('task')
    if task_content:
        new_task = {'content': task_content, 'done': False}
        collection.insert_one(new_task)
    return redirect(url_for('index'))

@app.route('/edit/<task_id>', methods=['GET', 'POST'])
def edit_task(task_id):
    task = collection.find_one({'_id': ObjectId(task_id)})
    if request.method == 'POST':
        task_content = request.form.get('task')
        collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'content': task_content}})
        return redirect(url_for('index'))
    return render_template('edit.html', task=task)

@app.route('/toggle/<task_id>', methods=['GET'])
def toggle_task(task_id):
    task = collection.find_one({'_id': ObjectId(task_id)})
    new_done_value = not task['done']
    collection.update_one({'_id': ObjectId(task_id)}, {'$set': {'done': new_done_value}})
    return redirect(url_for('index'))

@app.route('/delete/<task_id>', methods=['GET'])
def delete_task(task_id):
    collection.delete_one({'_id': ObjectId(task_id)})
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
