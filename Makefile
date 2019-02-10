all: run-kafka-server run-producer run-webapp

run-kafka-server:
	docker run -d -p 2181:2181 -p 9092:9092 --env ADVERTISED_HOST='localhost' --env ADVERTISED_PORT=9092 spotify/kafka

run-producer:
	docker build --tag=producer ./producer
	docker run -d --network="host" producer

run-webapp:
	docker build --tag=webapp ./webapp
	docker run -d --network="host" webapp

test-command:
	echo "Make command successful! Woot!"

.PHONY: run-producer run-kafka-server run-webapp
