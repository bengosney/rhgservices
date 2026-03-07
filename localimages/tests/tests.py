import io
from unittest.mock import MagicMock, patch

import pytest
from PIL import Image

from localimages.storage import DevImageStorage


@pytest.fixture
def storage():
    # We point this to a temporary directory so we don't mess with real media
    return DevImageStorage(location="/tmp/test_media")


def test_storage_returns_existing_file(storage, tmp_path):
    # Setup: Create a fake file on disk
    test_file = tmp_path / "test.jpg"
    test_file.write_text("fake image content")
    storage.location = str(tmp_path)

    # Execution
    with storage.open("test.jpg") as f:
        assert f.read() == b"fake image content"


@patch("requests.get")
def test_storage_generates_placeholder_when_missing(mock_get, storage):
    # Setup: Mock the network response
    mock_response = MagicMock()
    mock_response.content = b"picsum_image_data"
    mock_response.status_code = 200
    mock_get.return_value = mock_response

    # Execution: Try to open a file that doesn't exist
    with storage.open("non_existent.jpg") as f:
        # Assertions
        assert f.read() == b"picsum_image_data"
        mock_get.assert_called_once_with("https://picsum.photos/1600/900", timeout=5)


@patch("requests.get")
def test_storage_returns_gray_fallback_on_failure(mock_get, storage):
    # Setup: Simulate a 404 or connection error
    mock_get.side_effect = Exception("Picsum is down")

    # Execution
    with storage.open("missing_image.jpg") as f:
        content = f.read()

    # Verification: Check that it's a valid JPEG and the right color
    img = Image.open(io.BytesIO(content))

    assert img.size == (1600, 900)
    # Get the color of the top-left pixel
    assert img.getpixel((0, 0)) == (163, 163, 163)
