FROM amd64/python:3.11.4
COPY . /app
WORKDIR /app
RUN python -m venv venv2
ENV VIRTUAL_ENV=/app/venv2
ENV PATH="$VIRTUAL_ENV/bin:$PATH"
RUN pip install -U pip
RUN pip install pywin32-amd64
RUN pip install --upgrade setuptools
RUN pip install wmi 
RUN pip install -r requirements.txt
CMD python application.py