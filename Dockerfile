FROM python:3.9
MAINTAINER lyy


# Set the working directory
WORKDIR /flask_microblog

# Copy the requirements.txt file
COPY ./requirements.txt /flask_microblog/requirements.txt

# Upgrade pip
RUN pip install --upgrade pip

# Install the dependencies from requirements.txt
RUN pip install -r requirements.txt -i https://mirrors.aliyun.com/pypi/simple/

EXPOSE 5000

# Run the Django server
CMD ["python", "microblog.py"]
