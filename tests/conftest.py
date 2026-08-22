import pytest

from fastapi.testclient import TestClient

from app.main import app
from app.database.mongodb import users_collection


class LoggingTestClient(TestClient):

    def request(self, method, url, **kwargs):

        print(
            f"      [HTTP] client.{method.lower()}("
            f"\"{url}\")"
        )

        response = super().request(
            method,
            url,
            **kwargs
        )

        print(
            f"      [HTTP] response -> "
            f"{response.status_code}"
        )

        return response


@pytest.fixture
def client():

    print("   [FIXTURE client] setup")
    print("   [FIXTURE client] entering TestClient context")

    with LoggingTestClient(app) as test_client:

        print("   [FIXTURE client] yielding test_client")

        yield test_client

        print("   [FIXTURE client] test finished")

    print("   [FIXTURE client] exited TestClient context")
    print("   [FIXTURE client] teardown complete")


@pytest.fixture(autouse=True)
def clean_users_collection():

    print("   [FIXTURE database] setup")
    print("   [FIXTURE database] deleting users before test")

    users_collection.delete_many({})

    print("   [FIXTURE database] database ready")

    yield

    print("   [FIXTURE database] teardown")
    print("   [FIXTURE database] deleting users after test")

    users_collection.delete_many({})

    print("   [FIXTURE database] database clean")


def pytest_runtest_setup(item):

    print("\n")
    print("=" * 70)
    print(f"PYTEST START: {item.name}")
    print("=" * 70)
    print("[PYTEST] preparing test")


def pytest_runtest_call(item):

    print(f"[PYTEST] executing: {item.name}")


def pytest_runtest_teardown(item):

    print(f"[PYTEST] teardown: {item.name}")