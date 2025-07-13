FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim

RUN apt update && apt install -y make

WORKDIR /app

COPY group_sms_chat ./group_sms_chat
COPY requirements.txt ./requirements.txt
COPY pyproject.toml ./pyproject.toml
COPY Makefile ./Makefile

RUN make install

EXPOSE 9022

CMD ["make", "run"]
