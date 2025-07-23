# test_case_scheduler

## Описание проекта

Реализация класса Scheduler для работы с графиком занятости работника. Основные возможности:
* Получение занятых и свободных промежутков времени на указанную дату
* Проверка доступности конкретного временного интервала
* Поиск ближайшего свободного окна для заявки заданной длительности

## Запуск

### 1. Сборка Docker-образа
```
docker build -t scheduler-tests .
```

Если проблема с 
```
RUN pip install --no-cache-dir -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt
```
то попробуйте не использовать зеркало, то есть заменить на
```
RUN pip install --no-cache-dir -r requirements.txt
```

### 2. Запуск unit-тестов
```
docker run --rm scheduler-tests
```

## Структура проекта

```
scheduler/
├── Dockerfile          # Конфигурация Docker
├── scheduler.py        # Основной класс Scheduler
├── requirements.txt    # Зависимости (requests, pytest)
└── test_scheduler.py   # Unit-тесты
```

## Формат даты и времени

* Формат даты: гггг-мм-дд (например, 2025-07-23)

* Формат времени: ЧЧ:ММ (например, 22:00)
