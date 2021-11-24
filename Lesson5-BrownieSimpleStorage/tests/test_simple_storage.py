from brownie import SimpleStorage, accounts


def test_deploy():
    # Arrange
    account = accounts[0]

    # Act
    simple_storage = SimpleStorage.deploy({"from": account})
    starting_value = simple_storage.retrieve()
    expected = 0

    # Assert
    assert starting_value == expected


# brownie test -k test_updating_storage //// To only test this function
def test_updating_storage():
    # Arrange
    account = accounts[0]
    simple_storage = SimpleStorage.deploy({"from": account})

    # Act
    simple_storage.store(15, {"from": account})
    stored_value = simple_storage.retrieve()
    expected = 15

    # Assert
    assert stored_value == expected
