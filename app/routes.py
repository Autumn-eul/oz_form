from flask import Blueprint, request, jsonify, redirect, url_for, render_template
from app.models import User, db, AgeStatus, GenderStatus

# 블루프린트 설정
route_bp = Blueprint("auth", __name__, template_folder="templates")

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
