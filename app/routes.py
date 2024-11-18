from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from app.config import db
from app.models import Question, Choice, Answer

route_bp = Blueprint("survey_routes", __name__)

# 설문조사 생성
@route_bp.route('/questions/<int:step>', methods = ['GET', 'POST'])
def survey(step):
    # 질문 가져오기
    question = Question.query.filter_by(step = step, is_active = True).first()
    if not question:
        return render_template('404.html'), 404
    
    # GET : 질문 표시
    if request.method == 'GET':
        choices = Choice.query.filter_by(question_id = question.id, is_active = True).all()
        user_id = request.args.get('user_id', 1)
        return render_template('question.html', question = question, choices = choices, user_id = user_id)
    
    # POST : 답변 저장
    if request.method == 'POST':
        user_id = request.form.get('user_id')
        choice_id = request.form.get('choice_id')

        if not user_id or not choice_id:
            return jsonify({"msg" : "User ID or choice Id is missiing"}), 400
        
        # 답변 저장
        new_answer = Answer(user_id = user_id, choice_id = choice_id)
        db.session.add(new_answer)
        db.session.commit()

        # 다음 질문으로 이동
        next_question = Question.query.filter_by(step = step + 1, is_active = True).first()
        if next_question:
            return redirect(url_for('route_bp.survey', step = next_question.step, user_id = user_id))
        
        # 마지막 질문이면 설문 완료 페이지로 이동
        return redirect(url_for('route_bp.survey_complete', user_id = user_id))
    
@route_bp.route('/survey/complete')
def survey_complete():
    user_id = request.args.get('user_id')
    return render_template('results.html', user_id = user_id)