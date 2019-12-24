import producer_server

BROKER_URL = "localhost:9092"


def run_kafka_server():

    input_file = "police-department-calls-for-service.json"
    topic_name = "com.udacity.phuri.kafka.sfcrime.callsforservice"

    producer = producer_server.ProducerServer(
        input_file=input_file,
        topic=topic_name,
        bootstrap_servers=BROKER_URL,
        client_id=f"{topic_name}_producer"
    )

    return producer


def feed():
    producer = run_kafka_server()
    producer.generate_data()


if __name__ == "__main__":
    feed()
