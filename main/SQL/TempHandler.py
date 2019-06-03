from main.SQL.mysql import Temp,db
from datetime import datetime
from sqlalchemy.exc import InvalidRequestError

def insert(temp):
    try:
        temp.time = datetime.now()
        db.session.add(temp)
        db.session.commit()
        return True
    except InvalidRequestError:
        db.session.rollback()
    except Exception as e:
        print(e)
        return False


def query():
    return Temp.query.all()

def query_end():
    return Temp.query.order_by(Temp.time.desc()).first()


if __name__ == '__main__':
    print(query_end().to_json())