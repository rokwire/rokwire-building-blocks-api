from flask_login import UserMixin

from db import get_db


class User(UserMixin):
    def __init__(self, id_, netid, fname, lname, email, uin, phone):
        self.id = id_
        self.netid = netid
        self.fname = fname
        self.lname = lname
        self.email = email
        self.uin = uin
        self.phone = phone

    @staticmethod
    def get(user_id):
        conn = get_db()
        cur = conn.cursor()
        cur.execute("SELECT * FROM USERS WHERE id = ?", (user_id,))
        user_record = cur.fetchone()
        if not user_record:
            return None

        user = User(id_=user_record['id'], netid=user_record['netid'], fname=user_record['fname'],
                    lname=user_record['lname'], email=user_record['email'], uin=user_record['uin'],
                    phone=user_record['phone'])

        return user

    @staticmethod
    def create(netid, fname, lname, email, uin, phone):
        conn = get_db()
        cur = conn.cursor()

        cur.execute("INSERT INTO USERS (netid, fname, lname, email, uin, phone) VALUES (?,?,?,?,?,?)", (netid, fname,
                                                                                                        lname, email,
                                                                                                        uin, phone,))
        conn.commit()
        user = User(id_=cur.lastrowid, netid=netid, fname=fname, lname=lname, email=email, uin=uin, phone=phone)

        return user
