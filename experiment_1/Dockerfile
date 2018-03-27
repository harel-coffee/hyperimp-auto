# Set parent image
FROM python:3

# Set working directory to /exp
WORKDIR /exp

# Copy the current directory contents into the container
ADD . /exp

# Install packages specified in requirements.txt
RUN pip install --trusted-host pypi.python.org -r requirements.txt
RUN pip install git+https://github.com/renatopp/liac-arff@master 
RUN pip install git+https://github.com/openml/openml-python.git@develop

# Set PYTHONPATH for hyperimp
ENV PYTHONPATH /exp

# Run experiment.py when the container launches
ENTRYPOINT ["python", "-u", "hyperimp/experiment/experiment.py"]