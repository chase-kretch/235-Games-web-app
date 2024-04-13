import pytest

from games import create_app
from games.adapters import memory_repository, repository_populate
import games.adapters.repository as repo

"""
This file is for setting up the test client and load required informations to pytest client
Since this file is only for loading info, there is no test cases here.
"""



@pytest.fixture
def in_memory_repo():
    # This initialise memory repo for unit testing and load it up on pytest fixture
    repo = memory_repository.MemoryRepository()
    repository_populate.populate(repo)
    return repo


@pytest.fixture
def client():
    my_app = create_app({
        'Testing': True,
        'WTF_CSRF_ENABLED': False,
        'REPOSITORY': 'memory'
    })
    return my_app.test_client()

class AuthenticationManager:
    def __init__(self, client):
        self.__client = client

    def login(self, user_name='admin', password='ABCdef1234'):
        return self.__client.post(
            '/authentication/login',
            data={'user_name': user_name, 'password': password}
        )

    def logout(self):
        return self.__client.get('/authentication/logout')

@pytest.fixture
def auth(client):
    return AuthenticationManager(client)