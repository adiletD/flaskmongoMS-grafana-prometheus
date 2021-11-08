# syntax=docker/dockerfile:1

# the python version we use
FROM python:3.7-alpine 
ADD . /app

# setting the working directory    
WORKDIR /app   

# setting the env variables for our flask app
ENV FLASK_APP=app.py     
ENV FLASK_RUN_HOST=0.0.0.0

# installing some packages
RUN apk add --no-cache gcc musl-dev linux-headers

# copying the requirements file to the image file system
COPY requirements.txt requirements.txt 

# installing the dependencies of our app  
RUN pip3 install --upgrade pip && pip3 install -r requirements.txt && pip3 install --no-cache-dir Flask flask_prometheus_metrics

# exposing the port of 15000     
EXPOSE 15000

# making our image filesystem similar to our host
COPY . .

# launching our application                                
CMD ["python3", "app.py"]               
