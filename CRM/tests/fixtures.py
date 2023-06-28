import pytest 

from user_profile.models import UserProfileModel,User


@pytest.fixture
def create_user(db):
    return User.objects.create(username="Ahmed",password="12345678")



@pytest.fixture
def create_user_profile(db,create_user):
    return UserProfileModel.objects.create(user = create_user)