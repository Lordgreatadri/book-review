


from src.auth.schemas import CreateUserModel, UserLoginModel



auth_prefix =f"/api/v1/auth"

# test for user creation
def test_create_user(fake_session, fake_user_service, test_client):
    data={
        "username": "Samuel",
        "email": "samuel@gmail.com",
        "first_name": "Smauel",
        "last_name": "Lordgreat",
        "phone_number": "0543645680",
        "password": "123456",
        "password_confirmation": "123456",
    }# you can create fake values here with factory-boy

    response = test_client.post(
        url=f"{auth_prefix}/register",
        json=data
    )

    user_data = CreateUserModel(**data)
    
    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(data["email"], data["username"], fake_session)
    assert fake_user_service.get_user_by_email_called_once()
    assert fake_user_service.get_user_by_email_called_once_with(data["email"], fake_session)
    assert fake_user_service.get_user_by_username_called_once()
    assert fake_user_service.get_user_by_username_called_once_with(data["username"], fake_session)
    assert fake_user_service.get_user_by_phone_number_called_once()
    assert fake_user_service.get_user_by_phone_number_called_once_with(data["phone_number"], fake_session)
    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)




def test_login(fake_session, fake_user_service, test_client):
    data={
        "username": "Samuel",
        "password": "123456",
    }# you can create fake values here with factory-boy

    response = test_client.post(
        url=f"{auth_prefix}/login",
        json=data
    )

    user_data = UserLoginModel(**data)

    assert fake_user_service.authenticate_user_called_once()
    assert fake_user_service.authenticate_user_called_once_with(user_data['username'], user_data['password'], fake_session)


