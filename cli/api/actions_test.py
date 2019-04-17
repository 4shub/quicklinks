import unittest
import actions
import unittest.mock as mock


def empty_callback(*args, **kwargs):
    pass


def mock_open(data):
    m = mock.mock_open(read_data=data)
    m.return_value.__iter__ = lambda self: self
    m.return_value.__next__ = lambda self: next(iter(self.readline, ''))
    return m


class TestActions(unittest.TestCase):
    TEST_CONFIG = """
    google:https://google.com
    wiki:https://wikipedia.com
    """

    def test_find_key(self):
        expected_shortcut = 'google'
        expected_domain = 'https://google.com'
        m = mock_open(self.TEST_CONFIG)
        with mock.patch("builtins.open", m):
            status, shortcut, domain = actions._search_for_value_from_file(
                expected_shortcut)
            self.assertTrue(status)
            self.assertEqual(expected_shortcut, shortcut)
            self.assertEqual(expected_domain, domain)


if __name__ == '__main__':
    unittest.main()
