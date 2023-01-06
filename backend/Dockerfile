FROM python:3.11

RUN mkdir backend
WORKDIR /backend

COPY /pyproject.toml /backend
RUN pip3 install --no-chache-dir poetry
RUN poetry config virtualenvs.create false
RUN poetry install

EXPOSE 48569

COPY . .

CMD ["uvicorn", "main:application", "--host", "0.0.0.0", "--port", "48569", "--reload"]