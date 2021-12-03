from scripts.advanced_collectible.create_metadata import upload_to_ipfs


def test_uload_ipfs():
    # Arrange
    img_uri = 0
    file_path = "./img/charles1.jpg"
    # Act
    img_uri = upload_to_ipfs(file_path)
    # Assert
    assert img_uri != 0