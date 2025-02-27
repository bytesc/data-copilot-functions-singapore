import sqlalchemy


def from_lesson_num_to_lesson_name_func(lesson_num: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT lesson_name FROM lesson_info WHERE lesson_num=:lesson_num
                                            """),
                              {"lesson_num": lesson_num})
        conn.commit()
        lesson_result = result.fetchone()
        if lesson_result:
            return lesson_result[0]
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def from_lesson_name_to_lesson_num_func(lesson_name: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT lesson_num FROM lesson_info WHERE lesson_name=:lesson_name
                                            """),
                              {"lesson_name": lesson_name})
        conn.commit()
        lesson_result = result.fetchone()
        if lesson_result:
            return lesson_result[0]
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def from_uid_to_username_func(uid: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT username FROM user_info WHERE uid=:uid
                                            """),
                              {"uid": uid})
        conn.commit()
        user_result = result.fetchone()
        if user_result:
            return user_result[0]
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()


def from_username_to_uid_func(username: str, engine):
    conn = engine.connect()
    try:
        result = conn.execute(sqlalchemy.text("""
                        SELECT uid FROM user_info WHERE username=:username
                                            """),
                              {"username": username})
        conn.commit()
        user_result = result.fetchone()
        if user_result:
            return user_result[0]
        return None
    except Exception as e:
        print(e)
        raise e
    finally:
        conn.close()
