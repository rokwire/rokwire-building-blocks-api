#  Copyright 2022 Board of Trustees of the University of Illinois.
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

'''
Python module for SMTP connection utils
'''

import json
import logging

import controllers.configs as cfg
import utils.jsonutils as jsonutils

from flask import g, current_app
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def init_app(app):
    """
    Method to initialize and teardown app
    Stores SMTP connection in global object
    Args:
        app (object): FlaskApp object
    Returns: None
    """
    app.teardown_appcontext(close_smtp_connection)
    g.smtp = get_smtp_connection(app)


def close_smtp_connection():
    """
    Method to close smtp connection. Called when app teardown
    Args: None
    Returns: None
    """
    connection = g.pop('smtp', None)
    if connection is not None:
        success, error_msg, error_code = quit_smtp_connection(connection)
        if not success:
            msg = {
                "reason": "Error in closing SMTP connection: " + str(error_msg),
                "error": "Error code" + str(error_code)
            }
            msg_json = jsonutils.create_log_json("SMTPConnection", "quit", msg)
            logging.error("SMTPConnection QUIT " + json.dumps(msg_json))


def get_smtp_connection(app):
    """
    Method to establish smtp connection and store in g
    Args:
        app (object): FlaskApp object
    Returns:
        g.smtp (global object): SMTP connection
    """
    if 'smtp' not in g:
        g.smtp, error_msg, error_code = establish_smtp_connection()
        if g.smtp is None:
            msg = {
                "reason": "Error in establishing SMTP connection: " + str(error_msg),
                "error": "Error code" + str(error_code)
            }
            msg_json = jsonutils.create_log_json("SMTPConnection", "GET", msg)
            logging.error("SMTPConnection GET " + json.dumps(msg_json))
    return g.smtp


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


def send_email(mail_to, subject, message):
    """
    Method to send email to a user and print if success or failure
    Args:
        mail_to (str): email id of recipient
        subject (str): subject of the email
        message (str): message of the email
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

    connection = get_smtp_connection()
    try:
        connection.send_message(mimemsg)
    except smtplib.SMTPResponseException as ex:
        return False, ex.smtp_error, ex.smtp_code
    except smtplib.SMTPException as ex:
        return False, ex.strerror, ex.errno
    return True, ' ', ' '


# currently not used
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
    try:
        connection.quit()
        return True, ' ', ' '
    except smtplib.SMTPResponseException as ex:
        return False, ex.smtp_error, ex.smtp_code
    except smtplib.SMTPException as ex:
        return False, ex.strerror, ex.errno

