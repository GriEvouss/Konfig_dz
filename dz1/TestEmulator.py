import unittest
import os
import tempfile
import toml
from unittest.mock import patch, mock_open
from emulator import Emulator, load_config


class TestEmulator(unittest.TestCase):

    def setUp(self):
        # Задаем параметры конфигурации для тестов
        self.config = {
            "username": "major_slava",
            "hostname": "localhost",
            "vfs_path": "virtual_filesystem.tar",
            "startup_script": "startup_commands.txt"
        }
        self.emulator = Emulator(self.config['username'], self.config['hostname'])

    @patch('os.listdir')
    def test_execute_command_ls(self, mock_listdir):
        mock_listdir.return_value = ['file1.txt', 'file2.txt']
        result = self.emulator.execute_command("ls")
        self.assertEqual(result, "file1.txt\nfile2.txt")

    def test_execute_command_exit(self):
        result = self.emulator.execute_command("exit")
        self.assertFalse(result)

    @patch('os.chdir')
    def test_execute_command_cd_success(self, mock_chdir):
        result = self.emulator.execute_command("cd /some/path")
        self.assertEqual(result, "Перешли в /some/path")
        mock_chdir.assert_called_once_with("/some/path")

    @patch('os.chdir')
    def test_execute_command_cd_failure(self, mock_chdir):
        mock_chdir.side_effect = FileNotFoundError
        result = self.emulator.execute_command("cd /wrong/path")
        self.assertEqual(result, "Не удалось найти путь: /wrong/path")

    def test_execute_command_history(self):
        self.emulator.execute_command("ls")
        self.emulator.execute_command("cd /some/path")
        self.emulator.execute_command("ls")
        result = self.emulator.execute_command("history")
        self.assertIn("ls", result)
        self.assertIn("cd /some/path", result)

    def test_execute_command_date(self):
        with patch('time.strftime', return_value="2023-01-01 12:00:00"):
            result = self.emulator.execute_command("date")
            self.assertEqual(result, "2023-01-01 12:00:00")

    @patch('builtins.open', new_callable=mock_open, read_data='ls\ncd /test\nexit\n')
    @patch('os.path.exists', return_value=True)
    def test_execute_startup_commands(self, mock_exists, mock_open):
        self.emulator.execute_startup_commands("startup_commands.txt")
        self.assertIn("ls", self.emulator.history)
        self.assertIn("cd /test", self.emulator.history)
        self.assertIn("exit", self.emulator.history)

    @patch('os.path.exists', return_value=False)
    def test_execute_startup_commands_file_not_found(self, mock_exists):
        result = self.emulator.execute_startup_commands("nonexistent.txt")
        self.assertEqual(result, "Файл nonexistent.txt не найден.")


if __name__ == '__main__':
    unittest.main()