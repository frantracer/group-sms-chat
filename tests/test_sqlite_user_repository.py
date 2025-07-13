import pytest

from group_sms_chat.domain.exceptions import PhoneNumberAlreadyExistsError, UserAlreadyExistsError
from group_sms_chat.domain.user import HashedPassword, PhoneNumber, User, Username, UserPassword
from group_sms_chat.infrastructure.sqlite.user_repository import SQLiteUserRepository


@pytest.mark.asyncio
async def test_create_user() -> None:
    repo = SQLiteUserRepository(file_path=":memory:")

    user = User(
        username=Username("testuser"),
        phone_number=PhoneNumber("+1234567890"),
        hashed_password=HashedPassword.from_string(UserPassword("password123"))
    )

    await repo.add_user(user)
    retrieved_user = await repo.get_user(user.username)
    assert retrieved_user == user


@pytest.mark.asyncio
async def test_get_non_existent_user() -> None:
    repo = SQLiteUserRepository(file_path=":memory:")

    retrieved_user = await repo.get_user(Username("nonexistent"))
    assert retrieved_user is None


@pytest.mark.asyncio
async def test_create_same_username_twice_raises_an_error() -> None:
    repo = SQLiteUserRepository(file_path=":memory:")

    user = User(
        username=Username("testuser"),
        phone_number=PhoneNumber("+1234567890"),
        hashed_password=HashedPassword.from_string(UserPassword("password123"))
    )

    user2 = User(
        username=Username("testuser"),
        phone_number=PhoneNumber("+0987654321"),
        hashed_password=HashedPassword.from_string(UserPassword("anotherpassword"))
    )

    await repo.add_user(user)
    with pytest.raises(UserAlreadyExistsError):
        await repo.add_user(user2)


@pytest.mark.asyncio
async def test_create_existing_phone_number_raises_an_error() -> None:
    repo = SQLiteUserRepository(file_path=":memory:")

    user = User(
        username=Username("testuser"),
        phone_number=PhoneNumber("+1234567890"),
        hashed_password=HashedPassword.from_string(UserPassword("password123"))
    )

    user2 = User(
        username=Username("anotheruser"),
        phone_number=PhoneNumber("+1234567890"),
        hashed_password=HashedPassword.from_string(UserPassword("anotherpassword"))
    )

    await repo.add_user(user)
    with pytest.raises(PhoneNumberAlreadyExistsError):
        await repo.add_user(user2)


@pytest.mark.asyncio
async def test_get_user_by_phone_number() -> None:
    repo = SQLiteUserRepository(file_path=":memory:")

    user = User(
        username=Username("testuser"),
        phone_number=PhoneNumber("+1234567890"),
        hashed_password=HashedPassword.from_string(UserPassword("password123"))
    )

    await repo.add_user(user)
    retrieved_user = await repo.get_user_by_phone_number(user.phone_number)
    assert retrieved_user == user
