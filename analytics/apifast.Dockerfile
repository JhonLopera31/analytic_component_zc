FROM python:3.8-slim-buster

## Creating working directory
WORKDIR /analytics

#COPY . /python_codes
COPY *.py *.py
COPY requirements.txt requirements.txt
COPY ./json_data ./json_data
## Install dependencies
RUN pip install -r requirements.txt

#COPY all codes on image
COPY . .

CMD ["python","main_v1.py"]