build:
	docker build -t trade_producer .

run: build
	docker run --network=redpanda_network trade_producer