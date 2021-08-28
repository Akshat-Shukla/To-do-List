FROM python
WORKDIR /app
COPY /requirements.txt .
RUN pip install -r requirements.txt 
COPY /src .
EXPOSE 8000
CMD [".\venv\Scripts\activate"]
CMD ["uvicorn", "main:program", "--host=0.0.0.0", "--reload"]