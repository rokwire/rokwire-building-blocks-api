#  Copyright 2021 Board of Trustees of the University of Illinois.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.

import controllers.configs as cfg
import utils.mongoutils as mongoutils

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

"""
check if the logged in user is a superuser
"""
def check_if_superuser(login_id):
    sp_list = cfg.ADMIN_USERS.split(",")

    if login_id in sp_list:
        return True
    else:
        return False

"""
check if the logged in user is a reviewer
"""
def check_if_reviewer(login_id):
    # check if the logged in id is admin user
    is_superuser = check_if_superuser(login_id)

    if is_superuser:
        return True

    # check if the logged in id is in reviewers database
    list_reviewers = mongoutils.list_reviewers()

    if list_reviewers is not None:
        # extract out the usernames from the list
        users = []
        for reviewer in list_reviewers:
            users.append(reviewer["githubUsername"])

        if login_id in users:
            return True

    return False

def establish_smtp_connection():
    """
    Method to establish SMTP connection
    Args: None
    Returns:
        connection (obj): SMTP object
        smtp_error (str): Error string
        smtp_code (str): Error code
    """
    mail_from = cfg.SENDER_EMAIL
    password = cfg.SENDER_EMAIL_PASSWORD
    connection = smtplib.SMTP(host=cfg.SMTP_HOST, port=cfg.SMTP_PORT)
    try:
        connection.ehlo()
    except smtplib.SMTPHeloError as ex:
        return None, ex.smtp_error, ex.smtp_code
    try:
        connection.starttls()
    except smtplib.SMTPConnectError as ex:
        return None, ex.smtp_error, ex.smtp_code
    try:
        connection.login(mail_from, password)
    except smtplib.SMTPAuthenticationError as ex:
        return None, ex.smtp_error, ex.smtp_code
    return connection, '', ''


def test_smtp_connection(connection):
    """
    Method to test the SMTP connection
    Args:
        connection (obj): SMTP object
    Returns:
        (bool): True if connection is open, False if not
    """
    try:
        status = connection.noop()[0]
    except smtplib.SMTPServerDisconnected as ex:
        status = -1
    return True if status == 250 else False


def quit_smtp_connection(connection):
    """
    Method to quit the SMTP connection
    Args:
        connection (obj): SMTP object
    Returns:
        (bool): True if connection is closed successfully, False if not
        smtp_error (str): Error string if failure, empty string if success
        smtp_code (str): Error code if failure, empty string if success
    """
    # quit connection if connection exists
    if test_smtp_connection(connection):
        try:
            connection.quit()
            return True, ' ', ' '
        except smtplib.SMTPResponseException as ex:
            return False, ex.smtp_error, ex.smtp_code
        except smtplib.SMTPException as ex:
            return False, ex.strerror, ex.errno


def send_email(mail_to, subject, message, connection):
    """
    Method to send email to a user and print if success or failure
    Args:
        mail_to (str): email id of recipient
        subject (str): subject of the email
        message (str): message of the email
        connection (obj): SMTP object
    Returns:
        (bool): True if success, False if failure
        (str): Error code is failure, empty string if success
        (str): Error message if failure, empty string if success
    """
    mail_subject = subject
    mail_body = message
    mail_from = cfg.SENDER_EMAIL

    mimemsg = MIMEMultipart()
    mimemsg['From'] = mail_from
    mimemsg['To'] = mail_to
    mimemsg['Subject'] = mail_subject
    mimemsg.attach(MIMEText(mail_body, 'plain'))

    if not test_smtp_connection(connection):
        connection, error_str, error_code = establish_smtp_connection()
        if error_code:
            return False, error_str, error_code
    try:
        connection.send_message(mimemsg)
    except smtplib.SMTPResponseException as ex:
        return False, ex.smtp_error, ex.smtp_code
    except smtplib.SMTPException as ex:
        return False, ex.strerror, ex.errno
    return True, ' ', ' '

