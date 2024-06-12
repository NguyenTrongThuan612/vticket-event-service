from vticket_app.configs.amqp import log_channel

def send_log(log):
    log_channel.basic_publish("", "system_log", str(log).encode())