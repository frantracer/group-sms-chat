install:
	rm -rf .venv
	uv venv --python=python3.13.4 .venv
	uv pip install -r requirements.txt

test:
	.venv/bin/pytest tests

run:
	.venv/bin/uvicorn group_sms_chat.app:app --port 9022 --host 127.0.0.1

lint:
	.venv/bin/ruff check group_sms_chat tests
	.venv/bin/mypy --config-file pyproject.toml group_sms_chat tests

format:
	.venv/bin/ruff check group_sms_chat tests --fix

docker-build:
	docker build -t group_sms_chat:latest .

docker-run:
	docker run -it --name group_sms_chat -p 9022:9022 group_sms_chat:latest
