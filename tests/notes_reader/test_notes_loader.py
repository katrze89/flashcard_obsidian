import builtins
import os
from io import StringIO

import pytest

from app.models.note_models import Note
from app.notes_reader.notes_loader import MarkdownNotesLoader

CORRECT_PATH = "/home/kasia/Dokumenty/flashcards-ai-obsidian-pro/tests/notes_reader/data"


@pytest.fixture
def notes_loader():
    return MarkdownNotesLoader(".", ["python", "#pytest", "#docker"])


@pytest.fixture(scope="session")
def note_docker():
    return """
    # Docker
    
    Multiline Content
    Multiline Content
    
    #docker#pytest #python
    """


@pytest.fixture()
def file_md(note_docker):
    return StringIO(note_docker)


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
    path = "data.json"
    with pytest.raises(ValueError, match=" is not a valid path"):
        MarkdownNotesLoader(path, ["python", "#pytest", "#docker"])


def test_correct_number_of_detected_files(monkeypatch, notes_loader):
    expected_files = ["Pytest fixtures.md", "Pytest plugins.md", "Docker.md", "Pytest.md", "Coverage.md"]

    def stub_listdir(*args):
        return expected_files + ["cos.log"]

    monkeypatch.setattr(os, "listdir", stub_listdir)

    file_list = notes_loader.get_file_list()
    assert file_list == expected_files


def test_when_no_files_raise_error(monkeypatch, notes_loader):
    def stub_listdir(*args):
        return []

    monkeypatch.setattr(os, "listdir", stub_listdir)
    with pytest.raises(FileNotFoundError, match="No markdown files found."):
        notes_loader.get_file_list()


def test_when_no_markdown_files_raise_error(monkeypatch, notes_loader):
    def stub_listdir(*args):
        return ["cos.log", "main.py"]

    monkeypatch.setattr(os, "listdir", stub_listdir)
    with pytest.raises(FileNotFoundError, match="No markdown files found."):
        notes_loader.get_file_list()


def test_load_file(monkeypatch, file_md, note_docker):
    def fake_open(file, mode="r", encoding=None):
        assert mode == "r"
        assert encoding == "utf-8"
        return file_md

    monkeypatch.setattr(builtins, "open", fake_open)

    result = MarkdownNotesLoader.load_file("file1.md")
    assert result == note_docker


def test_load_file_non_utf8(monkeypatch):
    def fake_open(*args, **kwargs):
        raise UnicodeEncodeError("utf-8", "", 0, 1, "Invalid start byte")

    monkeypatch.setattr(builtins, "open", fake_open)

    with pytest.raises(UnicodeEncodeError):
        MarkdownNotesLoader.load_file("file1.md")


# TODO FIleNotFOundError
# TODO OSError
# TODO UnicodeDecodeError


@pytest.mark.parametrize(
    "tags, length, titles",
    [
        (["python", "#pytest", "#docker"], 4, ["Pytest fixtures", "Pytest plugins", "Docker", "Pytest"]),
        (["#docker"], 1, ["Docker"]),
        (["python", "#docker"], 2, ["Docker", "Pytest"]),
        (["something"], 0, []),
    ],
)
def test_load_notes_filter(monkeypatch, tags, length, titles):
    def stub_listdir(*args):
        return ["Pytest fixtures.md", "Pytest plugins.md", "Docker.md", "Pytest.md"]

    monkeypatch.setattr(os, "listdir", stub_listdir)

    def fake_open(file, mode="r", encoding=None):
        file = file[2:-3]
        if file in ["Docker"]:
            return StringIO("#docker")
        if file in ["Pytest fixtures", "Pytest plugins"]:
            return StringIO("#pytest")
        if file in ["Pytest"]:
            return StringIO("#python")
        return None

    monkeypatch.setattr(builtins, "open", fake_open)

    def fake_getmtime(*args):
        return 100000000

    monkeypatch.setattr(os.path, "getmtime", fake_getmtime)
    loader = MarkdownNotesLoader(".", tags)
    notes = loader.load()

    assert len(notes) == length

    for note in notes:
        assert isinstance(note, Note)
        assert note.title in titles


# TODO zmien tak aby mockowalo metode klasy a nie czastkowa
