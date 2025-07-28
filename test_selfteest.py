import unittest
from unittest.mock import patch, mock_open
from selfteest import SysUtils

class TestSysUtils(unittest.TestCase):
    def setUp(self):
        self.utils = SysUtils()

    @patch('os.walk')
    @patch('os.path.getsize')
    def test_find_large_files(self, mock_getsize, mock_walk):
        mock_walk.return_value = [('/test', [], ['file1'])]
        mock_getsize.return_value = 101 * 1024 * 1024
        with patch('builtins.print') as mock_print:
            self.utils.find_large_files('/test')
            mock_print.assert_called_with('/test/file1 - 101.0 MB')

    @patch('builtins.open', new_callable=mock_open, read_data='INFO test\nERROR fail\n')
    def test_extract_errors(self, mock_file):
        with patch('builtins.open', mock_file):
            self.utils.extract_errors('log.txt', 'out.txt')
            handle = mock_file()
            handle.write.assert_called_with('ERROR fail\n')

    @patch('builtins.input', side_effect=['10', '2'])
    @patch('builtins.print')
    def test_safe_divide(self, mock_print, mock_input):
        self.utils.safe_divide()
        mock_print.assert_any_call('Result: 5.0')

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_check_disk_usage(self, mock_print, mock_run):
        mock_run.return_value.stdout = 'Filesystem Size Used Avail Use% Mounted\n/dev/disk1 100G 91G 9G 91% /'
        self.utils.check_disk_usage()
        mock_print.assert_any_call('Warning: /dev/disk1 is at 91% usage!')

    @patch('subprocess.run')
    @patch('builtins.print')
    def test_ping_server(self, mock_print, mock_run):
        mock_run.return_value.returncode = 0
        self.utils.ping_server(['localhost'])
        mock_print.assert_any_call('localhost is reachable')

    @patch('builtins.open', new_callable=mock_open, read_data='password=abc123\n')
    def test_mask_passwords(self, mock_file):
        with patch('builtins.open', mock_file):
            self.utils.mask_passwords('file.txt', 'new.txt')
            handle = mock_file()
            handle.write.assert_called_with('password=********\n')

    def test_extract_unique_words(self):
        result = self.utils.extract_unique_words(['Hello world', 'world of DevOps'])
        self.assertEqual(result, ['devops', 'hello', 'of', 'world'])

    @patch('requests.get')
    @patch('builtins.print')
    def test_get_public_ip(self, mock_print, mock_get):
        mock_get.return_value.json.return_value = {'ip': '1.2.3.4'}
        mock_get.return_value.raise_for_status = lambda: None
        self.utils.get_public_ip()
        mock_print.assert_called_with('Your IP is: 1.2.3.4')

    @patch('socket.create_connection')
    @patch('builtins.print')
    def test_is_port_open(self, mock_print, mock_conn):
        self.assertTrue(self.utils.is_port_open('host', 80))
        mock_print.assert_called_with('Port 80 on host is open.')

    def test_find_sum_pairs(self):
        with patch('builtins.print') as mock_print:
            self.utils.find_sum_pairs([1, 2, 3, 4], 5)
            mock_print.assert_called_with([(2, 3), (1, 4)])

    def test_rolling_average(self):
        with patch('builtins.print') as mock_print:
            self.utils.rolling_average([1, 2, 3, 4, 5], 3)
            mock_print.assert_called_with([2.0, 3.0, 4.0])

    def test_detect_spikes(self):
        with patch('builtins.print') as mock_print:
            self.utils.detect_spikes([1, 2, 10])
            mock_print.assert_called_with([10])

    def test_most_common_code(self):
        with patch('builtins.print') as mock_print:
            self.utils.most_common_code(['200', '404', '404'])
            mock_print.assert_called_with('404')

    def test_merge_unique_ips(self):
        with patch('builtins.print') as mock_print:
            self.utils.merge_unique_ips(['1.1.1.1'], ['1.1.1.1', '2.2.2.2'])
            mock_print.assert_called_with(['1.1.1.1', '2.2.2.2'])

if __name__ == '__main__':
    unittest.main()