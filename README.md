# AWS URL Shortener

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-green) ![LangGraph](https://img.shields.io/badge/LangGraph-purple) ![PostgreSQL](https://img.shields.io/badge/PostgreSQL-blue) ![Qdrant](https://img.shields.io/badge/Qdrant-red) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

A production-ready URL Shortener built entirely on AWS, demonstrating scalable cloud architecture.

## Overview

This repository contains a high-performance, production-ready URL Shortener designed to leverage native AWS services for maximum scale, resilience, and minimal latency. The application is built using FastAPI on Python 3.11 and integrates with PostgreSQL and Qdrant.

## Project Structure

The project structure is organized as follows:

```
aws-url-shortener/
├── app/
│   ├── templates/        (HTML files)
│   ├── static/
│   │   ├── css/          (CSS files)
│   │   ├── js/           (JavaScript files)
│   │   └── images/       (Image files)
├── aws/
│   ├── cloudformation/   (IaC templates - future)
│   └── scripts/          (Setup scripts)
├── docs/
│   └── images/           (Architecture diagrams)
├── .gitignore
└── README.md
```

## Technology Stack

- **Backend Framework**: FastAPI (Python 3.11)
- **Database**: PostgreSQL (Relational metadata mapping)
- **Vector Database**: Qdrant (Semantic search/mapping)
- **State Management**: LangGraph (Dynamic flow and orchestrations)
- **Infrastructure as Code**: AWS CloudFormation (Automation templates)

## Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL
- Qdrant Instance
- AWS CLI configured with appropriate permissions

### Local Environment Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aws-url-shortener
   ```

2. Create a virtual environment and activate it:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Configure environment variables in a `.env` file at the root:
   ```env
   DATABASE_URL=postgresql://user:password@localhost:5420/dbname
   QDRANT_HOST=localhost
   QDRANT_PORT=6333
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Deployment on AWS

Refer to the `aws/` directory for cloud-native deployment details:
- **`aws/cloudformation/`**: Contains CloudFormation templates for deploying AWS resources (ECS/Fargate, RDS PostgreSQL, App Runner, etc.).
- **`aws/scripts/`**: Automation scripts to streamline deployments, migrations, and environment configuration.

## License

This project is licensed under the MIT License - see the LICENSE file for details.