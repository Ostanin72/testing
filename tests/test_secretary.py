import unittest

from secretary import get_name, get_directory


class TestMain(unittest.TestCase):
    def test_get_name_true(self):
        params = (
            ("2207 876234", "Василий Гупкин"),
            ("11-2", "Геннадий Покемонов"),
            ("10006",  "Аристарх Павлов"),
            ("5455 028765", "Василий Иванов")
        )
        for i, (x, expected) in enumerate(params):
            with self.subTest(i):
                result = get_name(x)
                self.assertEqual(expected, result)


    def test_get_name_false(self):
        params = (
            ("", "Документ не найден"),
            ("1", "Документ не найден")
        )
        for i, (x, expected) in enumerate(params):
            with self.subTest(i):
                result = get_name(x)
                self.assertEqual(expected, result)


    def test_get_directory(self):
            params = (
                ("2207 876234", "1"),
                ("11-2", "1"),
                ("10006", "2"),
                ("5455 028765", "1"),
                ("", "Полки с таким документом не найдено"),
                ("1", "Полки с таким документом не найдено")
            )
            for i, (x, expected) in enumerate(params):
                with self.subTest(i):
                    result = get_directory(x)
                    self.assertEqual(expected, result)
