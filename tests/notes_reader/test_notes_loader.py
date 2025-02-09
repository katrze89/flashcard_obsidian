import pytest

from app.notes_reader.notes_loader import MarkdownNotesLoader


@pytest.fixture(scope="session")
def note_docker():
    return """
    # Docker
    
    Multiline Content
    Multiline Content
    
    #docker#pytest #python
    """


# @pytest.fixture(scope="session")
# def file_md(note_docker):
#     return StringIO(note_docker)


def test_tags_are_normalized():
    tags = ["python", "#pytest", "#python", "Python", "  docker"]
    loader = MarkdownNotesLoader(".", tags)
    assert loader.tags == {"#pytest", "#python", "#docker"}


# TODO add more test cases for tags func
def test_find_tags_in_multiline_note(note_docker):
    loader = MarkdownNotesLoader(".", [])
    assert loader.find_tags(note_docker) == {"#docker", "#pytest", "#python"}


def test_check_tags_from_note_with_all_tags():
    loader = MarkdownNotesLoader(".", ["python", "#pytest"])
    assert loader.check_tags({"#pytest", "#python"})


def test_check_tags_from_note_with_not_all_tags():
    loader = MarkdownNotesLoader(".", ["python", "#pytest", "#docker"])
    assert loader.check_tags({"#unittest", "#docker"})


def test_check_tags_from_note_without_matching_tags():
    loader = MarkdownNotesLoader(".", ["python", "#pytest"])
    assert not loader.check_tags({"#unittest", "#docker"})

# TODO add all tests you think should be here 
# TODO model for flashcard (taki sam jak do Note tlko do Flashcarda)