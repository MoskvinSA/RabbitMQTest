import pika
import time
import argparse

# This file contain the test for consumer of RabbitMQ
# The messages are requested by queue and it delivery can be confirmed.
# This is SYNC version

# HOW TO USE:
# Open terminal and type: python3 consumerSync.py -n p1 -t 100 -m confirmMannually -q queue1
# The first argument is count of seconds while the producer is working
# The second argument can be 'confirmMannually' or 'noconfirm'. If the argument is 'confirmMannually' message will be confirmed manually.
# The last one set the queue name which will be used for delivery the messages.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help = "The name which will be shown in the final table.", type=str, required=True)
    parser.add_argument('-t', '--time', help = "Time while the action is performing.", type=int, required=True)
    parser.add_argument('-m', '--mode', help = "Set 'confirmMannually' or 'confirmMannually' for set autoconfirming", type=str, required=True)
    parser.add_argument('-q', '--queue', help = "The name of the queue which will be created and connected to chanel", type=str, required=True)
    parser.add_argument('-si', '--serverIp', help='The host of the RabbitMQ server', required=True)
    parser.add_argument('-u', '--user', help='The name for log in RabbitMQ server', required=True)
    parser.add_argument('-p', '--password', help='The password for log in RabbitMQ server', required=True)

    args = parser.parse_args()

    name = args.name
    workingTime = args.time
    confirmManually = args.mode == 'confirmMannually'
    queueName = args.queue
    hostToConnect = args.serverIp
    userName = args.user
    userPassword = args.password

    credentials = pika.PlainCredentials(userName, userPassword)
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            hostToConnect, 
            5672,
            '/',
            credentials
        )
    )

    print(hostToConnect)

    channel = connection.channel()
    channel.queue_declare(queue=queueName, durable=True)

    receivedMessageCount = 0

    def callback(ch, method, properties, body):
        nonlocal receivedMessageCount
        nonlocal workingTime
        nonlocal confirmManually
        nonlocal name
        receivedMessageCount += 1
        # emulate working process
        sum = int(body) + int(body)
        end = time.perf_counter()
        
        if confirmManually:
            ch.basic_ack(delivery_tag=method.delivery_tag)

        if end - start > workingTime:
            ch.stop_consuming()
            print(f'{name}:{receivedMessageCount / workingTime}')

    # deliver 1 message only
    channel.basic_qos(prefetch_count=1)
    #  if auto_asc = True message confirming is automatically
    channel.basic_consume(queue=queueName, on_message_callback=callback, auto_ack=not confirmManually)

    start = time.perf_counter()
    channel.start_consuming()


if __name__ == '__main__':
    main()