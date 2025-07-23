FROM python:3.11

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

COPY test_scheduler.py .
COPY scheduler.py .

CMD ["python3", "-m", "unittest", "test_scheduler.py", "-v"]