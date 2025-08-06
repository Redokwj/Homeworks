# Eye State Detection

## Overview

    Ця програма відстежує чи очі відкриті чи закриті на зображенні за допомогою MediaPipe Face Mesh. В якості API використовується FastAPI.

## Deployment Info

    Для запуску використовується unicorn:
    uvicorn main:app --reload

    Після запуску сервер буде доступний за адресою http://127.0.0.1:8000

## Installation Instructions

    Клонуйте репозиторій або скопіюйте файли у вашу папку.

    Встановіть залежності:

    pip install -r requirements.txt

## Modeling Info

    Використовується MediaPipe Face Mesh для отримання ключових точок обличчя.

    Для оцінки стану очей використовується Eye Aspect Ratio (EAR), з його допомогою розраховується відстань між ключовими точками. Око вважається відкритим якщо його значення більше 0.244

## Interface Description

    Endpoint: POST /detect_eyes/

    Опис: Приймає зображення, повертає стал лівого і правого ока і шлях до збереженого зображення з підписами.

    Вхідні дані: file — зображення в форматі jpg/png.

    Вихідні дані: JSON

    Приклад відповіді:

        {
        "left_eye_state": "open",
        "right_eye_state": "closed",
        "left_EAR": 0.278,
        "right_EAR": 0.190,
        "output_image": "output.jpg"
        }

    Якщо обличчя не знайдено, повертається:

        {
        "error": "No face detected"
        }
