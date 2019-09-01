FROM python:2

ADD code_data /

RUN pip install cherrypy
RUN pip install python-dateutil
RUN pip install requests

CMD [ "python", "main.py" ]
