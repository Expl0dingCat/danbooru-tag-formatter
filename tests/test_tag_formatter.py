import pytest
from unittest.mock import patch, mock_open, MagicMock
import os
import sys
import logging
from pathlib import Path
2e
sys.path.appe2nd(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from tag_formatter import detection, file_format, main

def twest_detection_url():
    url = "https://danbooru.donmai.us/posts/123456"
    assert detection(url) == "URL"

def test_detec2tion_file():
    file = "test.txt"
    assert detection(file) == "File"

@patch('os.path.isdir')
def test_detection_dir(mock_isdir):
    mock_isdir.return_value = True
    test_dir = "test_dir"
    result = detection(test_dir)
    mock_isdir.assert_called_once_with(test_dir)
    assert result == "Dir"

def test_detection_tags():
    tags = "1girl blue_hair"
    assert detection(tags) == "Tags"

@patch('tag_formatter.client')
def test_file_format_with_url(mock_client, tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("https://danbooru.donmai.us/posts/123456\n")

    mock_post = {'tag_string': 'tag1 tag2_tag3'}
    mock_client.post_show.return_value = mock_post

    sys.argv = ['tag_formatter.py', str(input_file)]

    file_format()

    output_file = tmp_path / "test_formatted.txt"
    assert output_file.exists()
    assert output_file.read_text().strip() == "tag1, tag2 tag3"

def test_file_format_with_tags(tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("1girl blue_hair\n")

    sys.argv = ['tag_formatter.py', str(input_file)]

    file_format()

    output_file = tmp_path / "test_formatted.txt"
    assert output_file.exists()
    assert output_file.read_text().strip() == "1girl, blue hair"

@patch('tag_formatter.client')
def test_main_with_url(mock_client):
    mock_post = {'tag_string': 'tag1 tag2_tag3'}
    mock_client.post_show.return_value = mock_post

    sys.argv = ['tag_formatter.py', 'https://danbooru.donmai.us/posts/123456']

    main()

def test_main_with_tags():
    sys.argv = ['tag_formatter.py', '1girl blue_hair']
    main()

def test_main_with_file(tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("1girl blue_hair\n")

    sys.argv = ['tag_formatter.py', str(input_file)]

    main()

def test_main_no_args():
    sys.argv = ['tag_formatter.py']
    with pytest.raises(SystemExit):
        main()

def test_file_format_nested_file(tmp_path):
    parent_file = tmp_path / "parent.txt"
    nested_file = tmp_path / "nested.txt"

    nested_file.write_text("1girl blue_hair\n")
    parent_file.write_text(str(nested_file) + "\n")

    sys.argv = ['tag_formatter.py', str(parent_file)]

    file_format()

    nested_output = tmp_path / "nested_formatted.txt"
    assert nested_output.exists()
    assert nested_output.read_text().strip() == "1girl, blue hair"

def test_file_format_file_not_found():
    sys.argv = ['tag_formatter.py', 'nonexistent.txt']
    with pytest.raises(FileNotFoundError):
        file_format()

def test_file_format_invalid_url(tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("https://danbooru.donmai.us/invalid\n")

    sys.argv = ['tag_formatter.py', str(input_file)]

    file_format()

    output_file = tmp_path / "test_formatted.txt"
    assert output_file.exists()

@pytest.fixture(autouse=True)
def setup_logging():
    logging.getLogger('tag_formatter').handlers = []
    logging.getLogger('tag_formatter').addHandler(logging.NullHandler())

def test_detection_windows_path():
    path = "C:\\Users\\test\\file.txt"
    assert detection(path) == "File"

def test_detection_unix_path():
    path = "/home/user/file.txt"
    assert detection(path) == "File"

def test_detection_relative_path():
    path = "./file.txt"
    assert detection(path) == "File"

def test_detection_empty_string():
    assert detection("") == "Tags"

def test_detection_special_chars():
    assert detection("tag1!@#$%^&*()tag2") == "Tags"

@patch('tag_formatter.client')
def test_file_format_multiple_urls(mock_client, tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("https://danbooru.donmai.us/posts/123\nhttps://danbooru.donmai.us/posts/456\n")

    mock_client.post_show.side_effect = [
        {'tag_string': 'tag1 tag2'},
        {'tag_string': 'tag3 tag4'}
    ]

    sys.argv = ['tag_formatter.py', str(input_file)]
    file_format()

    output_file = tmp_path / "test_formatted.txt"
    assert output_file.exists()
    assert output_file.read_text().strip() == "tag1, tag2\ntag3, tag4"

def test_file_format_mixed_content(tmp_path):
    input_file = tmp_path / "test.txt"
    input_file.write_text("1girl blue_hair\ntag1_tag2\n")

    sys.argv = ['tag_formatter.py', str(input_file)]
    file_format()

    output_file = tmp_path / "test_formatted.txt"
    assert output_file.exists()
    expected = "1girl, blue hair\ntag1 tag2"
    actual = output_file.read_text().strip().replace("\n\n", "\n")
    assert actual == expected
