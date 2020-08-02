import datetime
from unittest.mock import patch
import pytest
from rss_news import News

from ..fixtures import web_parser, raw_content, producer, proxies


@patch("parser.web_parser.WebParser.get_content")
def test_get_news_stream(get_content, web_parser, raw_content, producer, proxies):

    get_content.return_value = raw_content("rss_news_file.txt")
    producer.parser = web_parser

    stream = producer.get_news_stream(proxies)
    result = list(stream)[-1]

    assert isinstance(result, News)


@pytest.mark.parametrize(
    "title, expected_id",
    [
        ("example////1 example", "example1example"),
        ("example%%%%%%%2 example", "example2example"),
        ("*******example-3_  xx  example", "example-3_xxexample")]
)
def test_construct_id(producer, title, expected_id):

    result = producer.construct_id(title)

    assert result == expected_id


def test_unify_date(producer):
    expected = "2020-05-17 00:00:00"
    
    date = datetime.datetime(2020, 5, 17)
    result = producer.unify_date(date)

    assert result == expected


def test_format_description(producer):
    expected = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua."""

    description = """Lorem ipsum dolor sit amet, consectetur adipiscing elit, 
    sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. 
    Ut enim ad minim veniam, quis nostrud exercitation"""

    title = "Lorem ipsum"

    empty_description = ""

    result = producer.format_description(description, title)
    result_empty = producer.format_description(empty_description, title)
    assert result == expected
    assert result_empty == title


@pytest.mark.parametrize(
    "author, expected",[(None, "Unknown"), ("Test", "Test")]
)
def test_assing_author(producer, author, expected):

    result = producer.assign_author(author)

    assert result == expected