FROM python:latest

# Install dependencies.
ADD main.py /main.py
RUN pip install certifi==2020.6.20
RUN pip install chardet==3.0.4
RUN pip install Deprecated==1.2.10
RUN pip install idna==2.10
RUN pip install PyJWT==1.7.1
RUN pip install urllib3==1.25.9
RUN pip install wrapt==1.12.1
RUN pip install requests
RUN pip install pygithub
CMD ["python", "/main.py"]