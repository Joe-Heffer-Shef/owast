FROM python:slim-bullseye

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt


COPY ingress ingress

CMD ["python" "-m" "flask" "ingress"]