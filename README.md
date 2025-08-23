# 🕵️‍♂️ Audit Platform

Микросервисная платформа для сетевого аудита,c мониторингом и анализом инфраструктуры. Включает интеграцию с NetBox, Kafka, gRPC и экспортом метрик через Prometheus и доступом к Grafana.

---

## 📦 Структура репозитория

```
.
├── ApiGateway       # FastAPI шлюз с REST и gRPC клиентами
├── Audit            # Воркеры аудита (Kafka consumer, NetBox discovery)
├── NetBox           # gRPC-обёртка над NetBox API
├── deployment       # Docker Compose + Prometheus + конфиги
└── .gitignore
```
---

## 🧠 Возможности

- REST и gRPC доступ к данным NetBox
- Kafka consumer/producer воркеры
- Обнаружение новых устройств и подсетей
- Экспорт метрик FastAPI в Prometheus

---
## 🏗 Архитектура

```mermaid
flowchart TD
    client["Внешний клиент / Планировщик
Инициирует аудит или получает список доступных целей"] 
        -- REST: POST /audit/run --> api_gateway
    client -- REST: GET /audit/targets --> api_gateway

    %% API Gateway
    api_gateway["API Gateway / Оркестратор
FastAPI сервис
gRPC клиент к NetBox
Publisher в Kafka audit_requests
(опц.) читает audit_results"] 
        -- gRPC: GetTargets --> netbox_service
    api_gateway -->|publish audit_requests| kafka_queue
    kafka_queue -->|subscribe audit_results| api_gateway

    %% NetBox-сервис
    netbox_service["NetBox-воркер
FastAPI + gRPC сервер
REST клиент к NetBox DCIM/IPAM API
Кэширует данные в Redis"] 
        -- REST: /api/dcim/devices/, /api/ipam/prefixes/, /api/ipam/ip-addresses/ --> netbox_api
    netbox_service -->|write cache| redis_cache

    %% Kafka очередь
    kafka_queue["Kafka
Шина событий
Топики:
audit_requests, audit_results"]

    %% Discovery+Audit воркер
    kafka_queue -->|subscribe audit_requests| discovery_audit
    discovery_audit["Discovery+Audit воркер
Python asyncio (SSH/SNMP/gNMI по мере готовности)
Сравнивает с эталоном из NetBox
Publisher в Kafka audit_results"] 
        -- gRPC: GetDevices, GetSubnets, GetIPs --> netbox_service
    discovery_audit -- SSH/SNMP/gNMI --> network_equipment

    %% Мониторинг
    api_gateway -->|/metrics| prometheus
    netbox_service -->|/metrics| prometheus
    discovery_audit -->|/metrics| prometheus
    prometheus["Prometheus
Сбор метрик"] --> grafana["Grafana
Дашборды по сети и сервисам"]

    %% Классы
    classDef service fill:#1f77b4,stroke:#333,stroke-width:1px,color:#fff;
    classDef storage fill:#2ca02c,stroke:#333,stroke-width:1px,color:#fff;
    classDef queue fill:#9467bd,stroke:#333,stroke-width:1px,color:#fff;
    classDef equipment fill:#7f7f7f,stroke:#333,stroke-width:1px,color:#fff;
    classDef monitoring fill:#ff7f0e,stroke:#333,stroke-width:1px,color:#fff;
    classDef client fill:#ffcc00,stroke:#333,stroke-width:1px,color:#000;

    %% Привязка классов
    class client client;
    class api_gateway,netbox_service,discovery_audit service;
    class netbox_api,redis_cache storage;
    class kafka_queue queue;
    class network_equipment equipment;
    class prometheus,grafana monitoring;
```

## 🛠 Зависимости

- Python 3.13
- Docker + Docker Compose
- Poetry (для локальной разработки)
- Cloudsmith Token (для приватных пакетов)

---
---

## 📍 Автор

**Aleksandr Yurlov**  
GitHub: [@AlexYrlv](https://github.com/AlexYrlv)

---

## 📜 License

MIT License

