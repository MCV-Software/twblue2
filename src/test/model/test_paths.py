# -*- coding: utf-8 -*-
""" A set of tests for path generation. """
import os
import pytest
from unittest import mock
# We rely in app_path from this module as we cannot reproduce always the app path using pytest. So we asume platform utils is right.
from platform_utils.paths import app_path as get_app_path # type: ignore
from model import paths

def test_setup_when_portable():
    paths.mode = "portable"
    paths.setup()
    assert paths.mode == "portable" # No change

def test_setup_when_installed():
    with mock.patch("glob.glob", return_value=["uninstall.exe"]):
        paths.setup()
        assert paths.mode == "installed"

def test_app_path() -> None:
    app_path: str = paths.app_path()
    # This should point to the src path, as tests are running from there.
    assert app_path == get_app_path()

def test_locale_path() -> None:
    assert paths.locale_path() == os.path.join(get_app_path(), "locales")

def test_sound_path() -> None:
    assert paths.sound_path() == os.path.join(get_app_path(), "sounds")

@mock.patch.dict(os.environ, dict(HOME="/home/manuel/", AppData="C:\\users\\manuel\\AppData\\roaming"))
@pytest.mark.parametrize("is_portable, platform", [
    (True, "Windows"),
    (False, "Windows"),
    (True, "Linux"),
    (False, "Linux"),
    (True, "Darwin"),
    (False, "Darwin")
])
def test_logs_path(is_portable: bool, platform: str) -> None:
    mode: str
    expected_result: str
    if is_portable:
        mode = "portable"
    else:
        mode = "installed"
    with mock.patch("os.path.exists", return_value=False) as exists_mock:
        with mock.patch("os.mkdir") as mkdir_mock:
            with mock.patch.object(paths, "mode", mode):
                with mock.patch("platform.system", return_value=platform):
                    p: str = paths.logs_path()
                    if platform == "Windows":
                        if mode == "portable":
                            expected_result = os.path.join(get_app_path(), "logs")
                        else:
                            expected_result = os.path.join(paths.data_path(), "logs")
                    else:
                        expected_result = os.path.join(paths.data_path(), "logs")
                    assert p == expected_result
                    assert exists_mock.called_once_with(p)
                    assert mkdir_mock.called_once_with(p)

@mock.patch.dict(os.environ, dict(HOME="/home/manuel/", AppData="C:\\users\\manuel\\AppData\\roaming"))
@pytest.mark.parametrize("is_portable, platform", [
    (True, "Windows"),
    (False, "Windows"),
    (True, "Linux"),
    (False, "Linux"),
    (True, "Darwin"),
    (False, "Darwin")
])
def test_config_path(is_portable: bool, platform: str):
    mode: str
    expected_result: str
    if is_portable:
        mode = "portable"
    else:
        mode = "installed"
    with mock.patch("os.path.exists", return_value=False) as exists_mock:
        with mock.patch("os.mkdir") as mkdir_mock:
            with mock.patch.object(paths, "mode", mode):
                with mock.patch("platform.system", return_value=platform):
                    p = paths.config_path()
                    if platform == "Windows":
                        if mode == "portable":
                            expected_result = os.path.join(get_app_path(), "config")
                        else:
                            expected_result = os.path.join(paths.data_path(), "config")
                    else:
                        expected_result = os.path.join(paths.data_path(), "config")
                    assert p == expected_result
                    assert exists_mock.called_once_with(p)
                    assert mkdir_mock.called_once_with(p)

@mock.patch.object(os.path, "sep", "\\")
@mock.patch.object(paths, "mode", "portable")
@mock.patch("platform.system", return_value="Windows")
def test_config_path_custom_directory(platform_system: mock.Mock) -> None:
    directory: str = "C:\\users\\manuel\\downloads"
    with mock.patch("os.path.exists", return_value=False) as exists_mock:
        with mock.patch("os.mkdir") as mkdir_mock:
            with mock.patch.object(paths, "directory", directory):
                p: str = paths.config_path()
                expected_result: str = os.path.join(directory, "config")
                assert p == expected_result

@mock.patch.object(os.path, "sep", "\\")
@mock.patch.object(paths, "mode", "portable")
@mock.patch("platform.system", return_value="Windows")
def test_logs_path_custom_directory(platform_system: mock.Mock) -> None:
    directory: str = "C:\\users\\manuel\\downloads"
    with mock.patch("os.path.exists", return_value=False) as exists_mock:
        with mock.patch("os.mkdir") as mkdir_mock:
            with mock.patch.object(paths, "directory", directory):
                p: str = paths.logs_path()
                expected_result: str = os.path.join(directory, "logs")
                assert p == expected_result
