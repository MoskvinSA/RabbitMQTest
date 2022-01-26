import pika
import time
import argparse
# This file contain the test for producer of RabbitMQ
# The messages are pushed to the queue and can be saved on the disk.
# This is SYNC version

# HOW TO USE:
# Open terminal and type: python3 producerSync.py -n p1 -t 100 -m nosave -q queue1
# The first argument is the name which will be shown in the final table
# The second argument is count of seconds while the producer is working
# The second argument can be 'save' or 'nosave'. If the argument is 'save' message will be saved on disk.
# The last one set the queue name which will be used for push the messages.

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-n', '--name', help = "The name which will be shown in the final table.", type=str, required=True)
    parser.add_argument('-t', '--time', help = "Time while the action is performing.", type=int, required=True)
    parser.add_argument('-m', '--mode', help = "Set 'save' or 'nosave' for saving to persistance", type=str, required=True)
    parser.add_argument('-q', '--queue', help = "The name of the queue which will be created and connected to chanel", type=str, required=True)
    parser.add_argument('-si', '--serverIp', help='The host of the RabbitMQ server', required=True)
    parser.add_argument('-u', '--user', help='The name for log in RabbitMQ server', required=True)
    parser.add_argument('-p', '--password', help='The password for log in RabbitMQ server', required=True)
    args = parser.parse_args()

    name = args.name
    workingTime = args.time
    savePers = args.mode == 'save' 
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

    channel = connection.channel()
    channel.queue_declare(queue=queueName, durable=True)

    sentMessagesCount = 0
    start = end = time.perf_counter()

    while end - start < workingTime:
        sentMessagesCount += 1
        channel.basic_publish(exchange='',
                              routing_key=queueName,
                              body='1',
                              properties=pika.BasicProperties(
                                #   if mode is 2 messages will be saved on disk
                                  delivery_mode= 2 if savePers else 1
                              ))
        end = time.perf_counter()
    
    channel.close()
    connection.close()
    print(f'{name}:{sentMessagesCount / workingTime}')

if __name__ == '__main__':
    main()