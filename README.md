# Supermomos event management

## Architecture

![Architecture Diagram](./docs/architecture.png)

## Sequence Diagram

![Sequence Diagram](./docs/sequence.png)

## Key Features

- User and event data management (CRUD)
- Registration tracking
- Filtering and analytics on user engagement
- Transactional outbox pattern for email sending via worker
- UTM-based email performance tracking

## Technology Stack

- Python 3.12
- FastAPI
- Celery
- PynamoDB (DynamoDB ORM)
- DynamoDB
- AWS SES
- Localstack (for test)
- Docker + Docker Compose

## Limitations of DynamoDB

### ❗ Requirement: Efficient querying on large datasets  
While DynamoDB offers high scalability and low-latency lookups, it is **not well-suited** for flexible, multi-attribute queries over large datasets, especially when combining multiple filters dynamically (e.g., `job_title`, `company`, `city`, `state`).

### ❗ Requirement: Combine multiple filters in a single query  
To support all filter combinations with high performance in DynamoDB, we would need to create multiple GSIs (Global Secondary Indexes). However, this quickly becomes expensive and hard to manage as filter permutations grow.

## Suggested Improvement

### ✅ Use OpenSearch for Advanced Filtering & Analytics

I recommend offloading filtering and analytical workloads to **OpenSearch**, which supports:

- Full-text search
- Boolean queries with multiple filters
- Aggregations for UTM-based analytics
- Near real-time indexing of events and users

This approach provides:

- Lower cost for complex filtering
- Much faster query performance on large datasets
- Better support for future analytical features

### Data Sync Strategy

We can sync changes from DynamoDB to OpenSearch using: DynamoDB Streams
