from main.SQL.mysql import Image,db
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

def insert(image):
    try:
        image.time = datetime.now()
        db.session.add(image)
        db.session.commit()
        return True
    except InvalidRequestError:
        db.session.rollback()
    except Exception as e:
        print(e)
        return False


def query():
    return Image.query.all()


if __name__ == '__main__':
    for i in query():
        print(i.to_json())