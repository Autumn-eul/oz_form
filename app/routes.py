import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from flask import Blueprint, jsonify, request, render_template, redirect, url_for
from sqlalchemy import func # 집계함수
from config import db
from app.models import Question, Choice, Answer, User, AgeStatus, GenderStatus

route_bp = Blueprint("survey_routes", __name__)


@route_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.get_json()

        # 데이터 유효성 검사
        name = data.get("name")
        age = data.get("age")
        gender = data.get("gender")
        email = data.get("email")

        if not all([name, age, gender, email]):
            return jsonify({"message": "공백란이 존재하면 안됩니다."}), 400

        # 나이 및 성별 상태 확인
        try:
            age_status = AgeStatus[age]
            gender_status = GenderStatus[gender]
        except KeyError:
            return jsonify({"message": "잘못된 나이 또는 성별 선택입니다."}), 400

        # 이메일 중복 확인
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "이미 존재하는 이메일입니다."}), 400

        # 사용자 객체 생성 및 데이터베이스에 추가
        new_user = User(name=name, age=age_status, gender=gender_status, email=email)
        db.session.add(new_user)
        db.session.commit()

        # 성공 메시지 및 user_id 반환
        return jsonify({"message": "회원가입 성공!", "user_id": new_user.id})

    # GET 요청 후 signup 페이지 렌더링
    return render_template("signup.html")

@route_bp.route("/question/<int:question_id>")
def question(question_id):

    return render_template("question.html", question_id=question_id)


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
        choice_id = request.form.get('answer')

        if not user_id or not choice_id:
            return jsonify({"msg" : "User ID or choice Id is missiing"}), 400
        
        # 답변 저장
        new_answer = Answer(user_id = user_id, choice_id = choice_id)
        db.session.add(new_answer)
        db.session.commit()

        # 다음 질문으로 이동
        next_question = Question.query.filter_by(step = step + 1, is_active = True).first()
        if next_question:
            return redirect(url_for('survey_routes.survey', step = next_question.step, user_id = user_id))
        
        # 마지막 질문이면 설문 완료 페이지로 이동
        return redirect(url_for('survey_routes.survey_complete', user_id = user_id))
    
@route_bp.route('/survey/complete')
def survey_complete():
    user_id = request.args.get('user_id')
    return render_template('results.html', user_id = user_id)

# 결과페이지
@route_bp.route('/results/stats', methods=['GET'])
def get_results_stats():
    # 총 응답 수 
    total_responses_query = db.session.query(
        Choice.answer,  
        func.count(Answer.id).label("response_count")  
    ).join(Answer, Choice.id == Answer.choice_id).group_by(Choice.answer).all()

    # 총 응답 수 데이터 구성
    total_responses = {
        "labels": [record[0] for record in total_responses_query],
        "values": [record[1] for record in total_responses_query]
    }

    # 나이별 분포 
    age_distribution_query = db.session.query(
        User.age, func.count(User.id)
    ).group_by(User.age).all()
    age_distribution = {
        "labels": [age[0].value for age in age_distribution_query],  
        "values": [age[1] for age in age_distribution_query]
    }

    # 성별 분포 
    gender_distribution_query = db.session.query(
        User.gender, func.count(User.id)
    ).group_by(User.gender).all()
    gender_distribution = {
        "labels": [gender[0].value for gender in gender_distribution_query],  
        "values": [gender[1] for gender in gender_distribution_query]
    }

    # 질문별 선택지 비율
    question_charts = []
    for question in Question.query.all():  
        choices = Choice.query.filter_by(question_id=question.id).all()
        choice_labels = [choice.answer for choice in choices]
        choice_counts = [
            db.session.query(func.count(Answer.id))
            .filter(Answer.choice_id == choice.id)
            .scalar()
            for choice in choices
        ]
        question_charts.append({
            "labels": choice_labels,
            "values": choice_counts
        })

    # JSON 데이터로 반환
    return jsonify({
        "total_responses": total_responses,
        "age_distribution": age_distribution,  
        "gender_distribution": gender_distribution,  
        "question_charts": question_charts  
    })