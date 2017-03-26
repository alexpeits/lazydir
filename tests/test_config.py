import os
import unittest
try:
    import unittest.mock as mock
except ImportError:
    import mock

from lazydir import load_json, load_yaml, get_config, FT_MAP, ext
from lazydir import ConfigurationError

THIS_FILE = __file__


class TestExtensions(unittest.TestCase):

    TEST_FILENAME = 'path/to/file.test'
    TEST_EXT = TEST_FILENAME.split('.')[1]

    def test_map_register(self):
        with mock.patch.dict(FT_MAP, values={}, clear=True):
            @ext(self.TEST_EXT)
            def test_func():
                pass
            self.assertIs(FT_MAP[self.TEST_EXT], test_func)

    def test_map_call(self):
        mock_func = mock.MagicMock()
        exists_mock = mock.MagicMock(return_value=True)
        with mock.patch.dict(FT_MAP, values={}, clear=True):
            @ext(self.TEST_EXT)
            def test_func(config_path):
                mock_func()
            with mock.patch('os.path.exists', new=exists_mock):
                get_config(self.TEST_FILENAME)
        mock_func.assert_called_once_with()

    def test_error_path_not_exists(self):
        exists_mock = mock.MagicMock(return_value=False)
        with self.assertRaises(ConfigurationError):
            with mock.patch('os.path.exists', new=exists_mock):
                get_config(self.TEST_FILENAME)
