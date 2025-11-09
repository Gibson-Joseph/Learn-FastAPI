from src.auth.schemas import UserCreateModel


auth_prefix = f"/api/v1/auth"


def test_user_creation(fake_session, fake_user_service, test_client):
    singup_data = {
        "first_name": "Gibbs",
        "last_name": "Jose",
        "email": "gibbs@yopmail.com",
        "username": "Gibbs_Jose",
        "password": "gibson627414joseph",
    }

    response = test_client.post(
        url=f"{auth_prefix}/signup",
        json=singup_data,
    )

    user_data = UserCreateModel(**singup_data)

    assert fake_user_service.user_exists_called_once()
    assert fake_user_service.user_exists_called_once_with(
        singup_data["email"], fake_session
    )

    assert fake_user_service.create_user_called_once()
    assert fake_user_service.create_user_called_once_with(user_data, fake_session)
