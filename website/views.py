from flask import Blueprint, render_template, request, flash, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST': 
        data = request.json
        note = data.get('message')  

        if len(note) < 1:
            return jsonify({'status': 'error', 'message': 'Message is too short!'}), 400
        else:
            new_note = Note(data=note, user_id=current_user.id)  
            db.session.add(new_note)  
            db.session.commit()
            return jsonify({'status': 'success', 'message': 'Message added!'}), 200

    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=['POST'])
@login_required
def delete_note():  
    note = json.loads(request.data) 
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()

    return jsonify({})
