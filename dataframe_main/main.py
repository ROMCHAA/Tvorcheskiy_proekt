import pandas as pd
import smtplib
import os
from accessify import private

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

original_file_version = r"C:\Users\venia\Downloads\ads_data_121288_-_ads_data_121288_2.csv"


def convert_original_file(original_file_version):
    df = pd.read_csv(original_file_version)
    new_df = df.groupby('platform').agg(
        {'event': [('views', lambda x: (x == 'view').sum()), ('clicks', lambda x: (x == 'click').sum())]})
    new_df.columns = new_df.columns.droplevel(0)
    new_df = new_df.reset_index()
    new_df.to_csv('dataframe.csv', index=False)
    return new_df


class EmailSender:
    def __init__(self, sender_email, password, dataset):
        self.sender_email = sender_email
        self.password = password
        self.dataset = dataset

    def create_message(self, to_email):
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = to_email
        msg['Subject'] = "Dataset"
        return msg

    @private
    def server_processing(self, msg):
        server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
        server.login(self.sender_email, self.password)
        server.send_message(msg)
        server.quit()

    def send_email(self, file_path, to_email):
        # Создание сообщения
        msg = self.create_message(to_email)

        # Конвертация датасета в HTML-таблицу
        html = self.dataset.to_html()

        # Добавление таблицы в сообщение
        msg.attach(MIMEText(html, 'html'))

        # Отправка сообщения
        self.server_processing(msg)


# Создаем датасет
dataset = convert_original_file(original_file_version)

# Функция convert_original_file будет сохранять файл в текущей дирекории, поэтому будем находить ссылку
current_directory = os.getcwd()
file_path = os.path.join(current_directory, '../dataframe.csv')

# Непосредственная отправка сообщения
login = 'p4kveniamin@yandex.ru'
password = 'gfhjkmlkzndjhxtcrjujghjtrnf'
sender = EmailSender(login, password, dataset)
to_email = "veniaminpak.nsu@mail.ru"
sender.send_email(file_path, to_email)
