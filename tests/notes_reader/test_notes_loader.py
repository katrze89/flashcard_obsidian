import os

import pytest

from app.models.note_models import Note
from app.notes_reader.notes_loader import MarkdownNotesLoader

CORRECT_PATH = "/home/kasia/Dokumenty/flashcards-ai-obsidian-pro/tests/notes_reader/data"


@pytest.fixture(scope="session")
def note_docker():
    return """
    # Docker
    
    Multiline Content
    Multiline Content
    
    #docker#pytest #python
    """


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


def test_create_correct_path():
    loader = MarkdownNotesLoader(CORRECT_PATH, ["python", "#pytest", "#docker"])
    assert str(loader.folder_path) == CORRECT_PATH


def test_incorrect_path():
    path = "/home/kasia/Dokumenty/flashcards-ai-obsidian-pro/tests/notes_reader/data.json"
    with pytest.raises(ValueError, match=" is not a valid path"):
        MarkdownNotesLoader(path, ["python", "#pytest", "#docker"])


def test_correct_number_of_detected_files():
    expected_len = 5
    loader = MarkdownNotesLoader(CORRECT_PATH, ["python", "#pytest", "#docker"])
    file_list = loader.get_file_list()
    assert len(file_list) == expected_len
    assert file_list == ["Pytest fixtures.md", "Pytest plugins.md", "Docker.md", "Pytest.md", "Coverage.md"]


def test_detect_no_file():
    path = "/home/kasia/Dokumenty/flashcards-ai-obsidian-pro/tests/notes_reader"
    loader = MarkdownNotesLoader(path, ["python", "#pytest", "#docker"])
    file_list = loader.get_file_list()
    assert len(file_list) == 0


def test_load_file():
    loader = MarkdownNotesLoader(CORRECT_PATH, ["python", "#pytest", "#docker"])
    loaded_file = loader.load_file(os.path.join(CORRECT_PATH, "Docker.md"))
    assert isinstance(loaded_file, str)
    assert "Logi kontenera" in loaded_file


@pytest.mark.parametrize(
    "tags, lenght, titles",
    [
        (["python", "#pytest", "#docker"], 5, ["Pytest fixtures", "Pytest plugins", "Docker", "Pytest", "Coverage"]),
        (["#docker"], 1, ["Docker"]),
        (["python", "#docker"], 2, ["Docker", "Pytest"]),
        (["jakis"], 0, []),
    ],
)
def test_load_notes_filter(tags, lenght, titles):
    loader = MarkdownNotesLoader(CORRECT_PATH, tags)
    notes = loader.load()
    assert len(notes) == lenght
    for note in notes:
        assert isinstance(note, Note)
        assert note.title in titles


# TODO model for flashcard (taki sam jak do Note tlko do Flashcarda)
