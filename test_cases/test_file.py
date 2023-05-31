import unittest
import os
import pandas as pd
from dataframe_main.main import convert_original_file, EmailSender
from unittest.mock import patch

class TestMyCode(unittest.TestCase):
    def setUp(self):
        # Создаем временный файл
        self.df = pd.DataFrame({'date': ['2019-04-02']*5, 'event': ['click']*5,
                        'platform': ['android', 'android', 'ios', 'web', 'android'],
                        'ad_id': [121288]*5, 'ad_cost_type':['CPM']*5, 'ad_cost':[187.4]*5,
                        'time_only': ['22:39:16', '22:40:29', '22:40:31', '22:44:14', '22:48:26']})
        self.tmp_file_path = 'test_dataframe.csv'
        self.df.to_csv(self.tmp_file_path, index=False)

    def tearDown(self):
        # Удаляем временный файл
        os.remove(self.tmp_file_path)

    def test_convert_original_file(self):
        # Создаем result, которая будет хранить результат работы convert_original_file
        result = convert_original_file(self.tmp_file_path)

        # Проверяем, что результат соответствует ожидаемому
        expected_result = pd.DataFrame({'platform': ['android', 'ios', 'web'], 'views': [0, 0, 0], 'clicks': [3, 1, 1]})
        pd.testing.assert_frame_equal(result, expected_result)

    def test_send_email(self):
        # Создаем объект EmailSender
        sender = EmailSender("kakayato@pochta.com", "password", self.df)

        # Замокать smtplib.SMTP_SSL
        with patch('smtplib.SMTP_SSL') as mock_smtp:
            # Отправляем сообщение
            to_email = "recipient@example.com"
            sender.send_email(self.tmp_file_path, to_email)

            # Проверяем вызовы методов mock_smtp
            instance = mock_smtp.return_value
            instance.login.assert_called_with("kakayato@pochta.com", "password")
            instance.send_message.assert_called()
            instance.quit.assert_called()

