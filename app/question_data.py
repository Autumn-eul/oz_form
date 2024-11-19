import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import db
from app.models import Question, Choice, Image, ImageStatus
from app.__init__ import create_app

def question_data():

    # 이미지 생성
    image1 = Image(
        url = "https://img1.daumcdn.net/thumb/R1280x0/?scode=mtistory2&fname=https%3A%2F%2Fblog.kakaocdn.net%2Fdn%2FqnIz2%2FbtqSdtiK7C4%2FThg8RwPPLh1slbBI8Vsksk%2Fimg.jpg",
        type = ImageStatus.sub)
    image2 = Image(
        url = "https://img.vogue.co.kr/vogue/2019/03/style_5c9c8c4ba29e7.jpg",
        type = ImageStatus.sub)
    image3 = Image(
        url = "https://img.freepik.com/premium-photo/pizza-with-pineapple-wooden-board-table_923894-1179.jpg?w=1380",
        type = ImageStatus.sub)
    image4 = Image(
        url = "https://health.chosun.com/site/data/img_dir/2023/10/19/2023101901964_0.jpg",
        type = ImageStatus.sub)

    # 이미지 추가
    db.session.add_all([image1, image2, image3, image4])
    db.session.commit()

    # 질문 생성
    questions = [
        {"title" : "탕수육 어떻게 먹어?", "step" : 1, "image" : image1},
        {"title" : "민트초코 좋아해?", "step" : 2, "image" : image2},
        {"title" : "파인애플 피자 좋아해?", "step" : 3, "image" : image3},
        {"title" : "붕어빵 어디서부터 먹어?", "step" : 4, "image" : image4}
    ]

    for q in questions:
        question = Question(title = q['title'],
                            step = q['step'],
                            image = q['image'],
                            is_active = True)
        db.session.add(question)

    db.session.commit()

    choices = [
        {"answer": "1. 부먹", "question_id": 1, "step": 1},
        {"answer": "2. 찍먹", "question_id": 1, "step": 2},
        {"answer": "3. 담먹", "question_id": 1, "step": 3},
        {"answer": "4. 뭐든 그저 맛있다", "question_id": 1, "step": 4},

        {"answer": "1. 너무 좋아", "question_id": 2, "step": 1},
        {"answer": "2. 그걸 먹을바엔 차라리 치약먹는다", "question_id": 2, "step": 2},
        {"answer": "3. 때에 따라 다르다", "question_id": 2, "step": 3},
        {"answer": "4. 아무 생각이 없다", "question_id": 2, "step": 4},

        {"answer": "1. 완전 좋아", "question_id": 3, "step": 1},
        {"answer": "2. 대체 피자에 파인애플을 왜 넣어?", "question_id": 3, "step": 2},
        {"answer": "3. 피자라면 뭐든 좋아", "question_id": 3, "step": 3},
        {"answer": "4. 아무 생각이 없다", "question_id": 3, "step": 4},

        {"answer": "1. 머리", "question_id": 4, "step": 1},
        {"answer": "2. 꼬리", "question_id": 4, "step": 2},
        {"answer": "3. 한입만 먹는다", "question_id": 4, "step": 3},
        {"answer": "4. 붕어빵을 왜 먹는지 모르겠다", "question_id": 4, "step": 4},
    ]

    for c in choices:
        choice = Choice(answer = c['answer'],
                        question_id = c['question_id'],
                        step = c['step'],
                        is_active = True)
        db.session.add(choice)

    db.session.commit()

if __name__ == '__main__':

    app = create_app()
    with app.app_context():
        question_data()
        print('Data initialized successfully!')