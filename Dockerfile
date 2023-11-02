FROM python:3.10.5
WORKDIR /app
COPY requirements.txt ./requirements.txt
RUN pip install -r requirements.txt
EXPOSE 8501
COPY . /app
RUN pip install rootmodel/packages/en_xner_package-1.0.0/dist/en_xner_package-1.0.0.tar.gz
ENTRYPOINT [ "streamlit", "run" ]
CMD ["app.py"]