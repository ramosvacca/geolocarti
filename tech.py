import socket

def report_log(message, log='general_log'):

    """
    As we need to write the error messages, the message is passed along with the log, if different from general_log
    :param message: the message to be written
    :log: the log where the message will be written
    :return:
    """

    error_log = open('logs/' + log + '.txt', mode='at', encoding='UTF-8')
    error_log.write(message+'\n')

hostname = socket.gethostname()