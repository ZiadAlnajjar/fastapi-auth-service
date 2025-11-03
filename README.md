# FastAPI Auth Service

[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-009688?style=flat-square\&logo=fastapi\&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python Version](https://img.shields.io/badge/Python-3.13-blue?style=flat-square\&logo=python\&logoColor=white)](https://www.python.org/)
[![Database](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=flat-square\&logo=postgresql\&logoColor=white)](https://www.postgresql.org/)
[![Cache](https://img.shields.io/badge/Redis-Ready-D82C20?style=flat-square\&logo=redis\&logoColor=white)](https://redis.io/)
[![Dockerized](https://img.shields.io/badge/docker-ready-blue?style=flat-square&logo=docker)](https://www.docker.com/)
[![License: MIT](https://img.shields.io/github/license/ZiadAlnajjar/fastapi-auth-service?style=flat-square)](./LICENSE)

---

## Overview

A fully featured **authentication** service built with **FastAPI** and structured according to **Domain-Driven Design (DDD)** and **Clean Architecture** principles.

It implements **JWT-based authentication** with access and refresh tokens, **soft deletion**, **token blacklisting**, **API versioning**, and **global exception handling**, while maintaining clear separation of concerns across layers.

---

## Quick Start

> ℹ️ Configure .env file first

### Local Setup

#### 1. Install dependencies

```bash
poetry install
```

#### 2. Run database migrations

```bash
alembic upgrade head
```

#### 3. Start the server

```bash
uvicorn app.main:app --reload
```

> API will be available at `http://localhost:8000/api/v1`

### Docker Setup

```bash
docker compose up
```

> API will be available at `http://localhost:8000/api/v1`

---

## Features

* **Clean Architecture + DDD**

  * Separation of Domain, Application, Infrastructure, and Presentation layers
  * Explicit interfaces and dependency inversion
  * Organized per-module design (`modules/auth`, etc.)

* **Dual-ID Pattern**

  * Each user entity has both a private (ULID) ID and a public (UUID) ID
  * Public IDs are used in tokens and external APIs for security and abstraction

* **Authentication**

  * Access and Refresh JWT token pair
  * Token blacklisting for logout and revocation
  * JWT service supporting multiple algorithms and expiry control

* **Cookie and Header Support**

  * Tokens can be sent via:

    * `HttpOnly` `strict` cookies for browsers (secure, XSS- and CSRF-safe)
    * Authorization headers or JSON body for API clients
  * Determined dynamically by request context or headers, or explicitly via headers

* **Middleware**

  * `AuthMiddleware` for global route protection
  * Public/protected route decorators (`@public`)
  * `GlobalErrorHandlerMiddleware` for consistent error responses

* **Domain-Level Validation and Exceptions**

  * Custom exception hierarchy (`InvalidTokenTypeException`, `UserAlreadyExistsException`, etc.)
  * Unified error responses from middleware

* **CQR Pattern**

  * Commands and Queries separated under the Application layer
  * Commands: `register_user`, `logout_user`, `refresh_token`
  * Queries: `login_user`

* **Dependency Injection**

  * Service and repository wiring via `Depends()` for full inversion of control
  * Clean DI container in `core/di.py`

* **Soft Delete**

  * Global SQLAlchemy event listener that filters out soft-deleted entities
  * Consistent ORM-level delete handling

* **Database and Cache**

  * Async SQLAlchemy ORM with PostgreSQL
  * Redis-based token blacklist and cache abstraction interface
  * Connection pooling for both database and Redis

* **API Versioning**

  * `/api/v1/auth/...` structure for forward compatibility

* **Pydantic Usage**

  * DTOs and FastAPI models for requests, responses, and service contracts
  * Validation at all I/O boundaries

* **Migrations**

  * Alembic integrated with SQLAlchemy Base
  * Modular entity importing for automated migration generation

---

## API Endpoints

| Method | Endpoint         | Description                 |
| ------ | ---------------- | --------------------------- |
| `POST` | `/auth/register` | Register a new user         |
| `POST` | `/auth/login`    | Login and obtain tokens     |
| `POST` | `/auth/token`    | Refresh access token        |
| `POST` | `/auth/logout`   | Logout and blacklist tokens |

---

## Project Structure

```
app
├─ modules
│  └─ auth
│     ├─ presentation
│     │  ├─ utils
│     │  ├─ types
│     │  │  └─ requests
│     │  ├─ routes
│     │  ├─ middlewares
│     │  ├─ mappers
│     │  ├─ dtos
│     │  └─ decorators
│     ├─ infrastructure
│     │  ├─ services
│     │  ├─ security
│     │  ├─ repositories
│     │  └─ http
│     ├─ domain
│     │  ├─ services
│     │  ├─ repositories
│     │  ├─ exceptions
│     │  └─ entities
│     └─ application
│        ├─ queires
│        │  ├─ refresh_token
│        │  └─ login_user
│        ├─ dtos
│        └─ commands
│           ├─ register_user
│           └─ logout_user
│
├─ presentation
│  └─ middlewares
│
├─ infrastructure
│  ├─ cache
│  ├─ repositories
│  └─ database
│
├─ domain
│  ├─ exceptions
│  ├─ repositories
│  └─ services
│
└─ core
```
