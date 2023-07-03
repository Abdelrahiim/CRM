import pytest

from user_profile.models import UserProfileModel


# ---------------------------------------------------------------
@pytest.mark.dbfixture
def test_create_user_profile(create_user_profile):
    new_user_profile = create_user_profile 
    old_user_profile = UserProfileModel.objects.all().first()
    assert new_user_profile.id == old_user_profile.id
    
    


