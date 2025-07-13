import pytest

from group_sms_chat.domain.group import Group, GroupName, GroupUser
from group_sms_chat.domain.user import PhoneNumber, Username
from group_sms_chat.infrastructure.sqlite.group_repository import SQLiteGroupRepository


@pytest.mark.asyncio
async def test_create_group() -> None:
    repo = SQLiteGroupRepository(file_path=":memory:")

    group = Group(
        name=GroupName(root="testgroup"),
        users={
            GroupUser(
                username=Username(root="user1"),
                user_group_phone_number=PhoneNumber(root="+1234567890")
            ),
            GroupUser(
                username=Username(root="user2"),
                user_group_phone_number=PhoneNumber(root="+0987654321")
            )
        }
    )

    await repo.create_or_update_group(group)

    found_groups = await repo.find_groups_by_name(GroupName(root="testgroup"))
    assert len(found_groups) == 1
    assert found_groups[0].name == group.name
    assert found_groups[0].users == group.users


@pytest.mark.asyncio
async def test_update_existing_group() -> None:
    repo = SQLiteGroupRepository(file_path=":memory:")

    # Create initial group
    initial_group = Group(
        name=GroupName(root="updategroup"),
        users={
            GroupUser(
                username=Username(root="user1"),
                user_group_phone_number=PhoneNumber(root="+1234567890")
            )
        }
    )
    await repo.create_or_update_group(initial_group)

    # Update the group with different users
    updated_group = Group(
        name=GroupName(root="updategroup"),
        users={
            GroupUser(
                username=Username(root="user2"),
                user_group_phone_number=PhoneNumber(root="+0987654321")
            ),
            GroupUser(
                username=Username(root="user3"),
                user_group_phone_number=PhoneNumber(root="+1122334455")
            )
        }
    )
    await repo.create_or_update_group(updated_group)

    # Verify the group was updated
    found_groups = await repo.find_groups_by_name(GroupName(root="updategroup"))
    assert len(found_groups) == 1
    assert found_groups[0].name == updated_group.name
    assert found_groups[0].users == updated_group.users

    # Verify old user is not in the group anymore
    user1_groups = await repo.find_user_groups(Username(root="user1"))
    assert len(user1_groups) == 0


@pytest.mark.asyncio
async def test_find_groups_by_name_partial_match() -> None:
    repo = SQLiteGroupRepository(file_path=":memory:")

    # Create multiple groups
    user_group = GroupUser(
        username=Username(root="user1"),
        user_group_phone_number=PhoneNumber(root="+1234567890")
    )
    groups = [
        Group(name=GroupName(root="testgroup1"), users={user_group}),
        Group(name=GroupName(root="testgroup2"), users={user_group}),
        Group(name=GroupName(root="anothergroup"), users={user_group}),
        Group(name=GroupName(root="testproject"), users={user_group}),
    ]

    for group in groups:
        await repo.create_or_update_group(group)

    # Search for groups containing "test"
    found_groups = await repo.find_groups_by_name(GroupName(root="test"))
    assert len(found_groups) == 3
    found_names = {str(group.name) for group in found_groups}
    assert found_names == {"testgroup1", "testgroup2", "testproject"}


@pytest.mark.asyncio
async def test_find_groups_by_name_no_matches() -> None:
    repo = SQLiteGroupRepository(file_path=":memory:")

    group = Group(name=GroupName(root="testgroup"), users=set())
    await repo.create_or_update_group(group)

    found_groups = await repo.find_groups_by_name(GroupName(root="nonexistent"))
    assert len(found_groups) == 0


@pytest.mark.asyncio
async def test_find_user_groups() -> None:
    repo = SQLiteGroupRepository(file_path=":memory:")

    # Create multiple groups with overlapping users
    group1 = Group(
        name=GroupName(root="group1"),
        users={
            GroupUser(
                username=Username(root="user1"),
                user_group_phone_number=PhoneNumber(root="+1111111111")
            ),
            GroupUser(
                username=Username(root="user2"),
                user_group_phone_number=PhoneNumber(root="+2222222222")
            )
        }
    )

    group2 = Group(
        name=GroupName(root="group2"),
        users={
            GroupUser(
                username=Username(root="user1"),
                user_group_phone_number=PhoneNumber(root="+1111111111")
            ),
        }
    )

    group3 = Group(
        name=GroupName(root="group3"),
        users={
            GroupUser(
                username=Username(root="user2"),
                user_group_phone_number=PhoneNumber(root="+2222222222")
            )
        }
    )

    await repo.create_or_update_group(group1)
    await repo.create_or_update_group(group2)
    await repo.create_or_update_group(group3)

    # Find groups for user1
    user1_groups = await repo.find_user_groups(Username(root="user1"))
    assert len(user1_groups) == 2
    user1_group_names = {str(group.name) for group in user1_groups}
    assert user1_group_names == {"group1", "group2"}

    # Find groups for user2
    user2_groups = await repo.find_user_groups(Username(root="user2"))
    assert len(user2_groups) == 2
    user2_group_names = {str(group.name) for group in user2_groups}
    assert user2_group_names == {"group1", "group3"}

    # Find groups for user3
    user3_groups = await repo.find_user_groups(Username(root="user3"))
    assert len(user3_groups) == 0
