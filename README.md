# 🌍 Universal Product Price Comparison Tool

A generic, country-aware product price comparison API built using **FastAPI** and enhanced using **LLMs** for **relevance filtering** and **product validation**.

---

## 🚀 Features

- 🌐 Search product prices from **any country**
- 🧠 LLM-based validation to ensure product relevance
- 📦 Works across **all categories** of online products
- 📊 Returns results which are relevant to the user's query
- 🔗 Direct links to product pages
- 🐳 Fully dockerized for consistent deployment

---

## 📡 API Overview

| Method | Endpoint                                 | Description                                | Request Body Example                                  |
|--------|------------------------------------------|--------------------------------------------|--------------------------------------------------------|
| POST   | `/v0/products/product-search-request`     | Fetches product prices from multiple sites | `{ "country": "US", "query": "iPhone 16 Pro, 128GB" }` |

---
## 🧾 Sample Queries

```json
{ "country": "US", "query": "iPhone 16 Pro, 128GB" }
{ "country": "IN", "query": "boAt Airdopes 311 Pro" }
```

---

## Demo Video Links - Includes Different regions based queries

- Demo Video 1
```
https://drive.google.com/file/d/1kKVqqTWAlAPXhzucI98uaoo7GEzY4kdh/view?usp=sharing
```

- Demo Video 2
```
https://drive.google.com/file/d/17mtqdo7d0ZH9Ay0iIDjiVL8ogpSBAOcW/view?usp=sharing
```

---

## 🧾 Steps to set this up locally

- Clone the github repo 
- Install Poetry into your system and refer docs for me
    ```
    brew install poetry
    ```
- Get into the poetry shell 
    ```
    poetry shell
    ```
- Install All Dependencies
    ```
    poetry install
    ```
- Run the server using uvicorn
    ```
    poetry run uvicorn app.main:app --host 0.0.0.0 --port 8030 --reload
    ```
- After running the Server
    ```
    Go to the /docs endpoint and enter your queries to the API
    Output json bodies is also added to the repo under outputs/ folder
    ```
- Docker build and run command for dockerised solutions
    ```
    docker build -t productsearch .
    docker run -d --env-file .env -p 8030:8030  productsearch 
    ```
- Curl Command for Iphone 16 Pro, 128 GB
    ```
    curl -X 'POST' \   'https://ameybhat-product-search-dpdybvgjhvdhb5d2.centralindia-01.azurewebsites.net/v0/products/product-search-request' \   -H 'accept: application/json' \   -H 'Content-Type: application/json' \   -d '{   "country": "US",   "query": "iPhone 16 Pro, 128gb" }'
    ```
- Deployed URL
    ```
    https://ameybhat-product-search-dpdybvgjhvdhb5d2.centralindia-01.azurewebsites.net/docs
    ```
