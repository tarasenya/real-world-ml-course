build:
	docker build -t trade_producer .

run: build
	docker run --network=redpanda_network trade_producer


build_lean:
	docker build -t trade_producer_lean -f LeanDockerfile .

run_lean_trade_producer:
	docker run --network=redpanda_network trade_producer_lean