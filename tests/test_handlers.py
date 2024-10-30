import json


async def test_create_user(client, get_user_from_database):
    user_data = {
        "name": "Боб",
        "surname": "Спанч",
        "class_number": "10",
        "exam_type": "ЕГЭ",
        "email": "bob2@ya.ru",
        "telegram": "bobsponge"
    }
    resp = client.post("/user/", data=json.dumps(user_data))
    data_from_resp = resp.json()
    assert resp.status_code == 200

    assert data_from_resp['name'] == user_data['name']
    assert data_from_resp['surname'] == user_data['surname']
    assert data_from_resp['class_number'] == user_data['class_number']
    assert data_from_resp['exam_type'] == user_data['exam_type']
    assert data_from_resp['email'] == user_data['email']
    assert data_from_resp['telegram'] == user_data['telegram']

    users_from_db = await get_user_from_database(data_from_resp["user_id"])
    assert len(users_from_db) == 1

    user_from_db = dict(users_from_db[0])
    assert user_from_db['name'] == user_data['name']
    assert user_from_db['surname'] == user_data['surname']
    assert user_from_db['class_number'] == user_data['class_number']
    assert user_from_db['exam_type'] == user_data['exam_type']
    assert user_from_db['email'] == user_data['email']
    assert user_from_db['telegram'] == user_data['telegram']
    assert user_from_db['is_active'] is True
    assert str(user_from_db['user_id']) == data_from_resp['user_id']
