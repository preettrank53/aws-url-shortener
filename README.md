# AWS URL Shortener

![Python](https://img.shields.io/badge/Python-3.11-blue) ![FastAPI](https://img.shields.io/badge/FastAPI-green) ![AWS](https://img.shields.io/badge/AWS-FF9900?logo=amazon-aws&logoColor=white) ![DynamoDB](https://img.shields.io/badge/DynamoDB-4053D6?logo=amazondynamodb&logoColor=white) ![License](https://img.shields.io/badge/License-MIT-yellow) ![Status](https://img.shields.io/badge/Status-Active%20Development-orange)

A production-ready URL Shortener built entirely on AWS, demonstrating scalable cloud architecture.

## Overview

This repository contains a high-performance, production-ready URL Shortener designed to leverage native AWS services for maximum scale, resilience, and minimal latency. The application is built using FastAPI on Python 3.11 and integrates with AWS DynamoDB for fast key-value lookups.

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
- **Database**: AWS DynamoDB (for low-latency, scalable key-value storage)
- **Infrastructure as Code**: AWS CloudFormation (Automation templates)
- **Compute / Hosting**: AWS App Runner / AWS ECS Fargate

## Getting Started

### Prerequisites

- Python 3.11+
- AWS CLI configured with appropriate credentials/permissions
- Local DynamoDB (optional, for local development testing)

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
   DYNAMODB_TABLE=url-shortener-table
   AWS_REGION=us-east-1
   ```

5. Run the development server:
   ```bash
   uvicorn app.main:app --reload
   ```

## Deployment on AWS

Refer to the `aws/` directory for cloud-native deployment details:
- **`aws/cloudformation/`**: Contains CloudFormation templates for deploying AWS resources (DynamoDB Table, ECS/Fargate, App Runner, IAM Roles).
- **`aws/scripts/`**: Automation scripts to streamline deployments, migrations, and environment configuration.

## License

This project is licensed under the MIT License - see the LICENSE file for details.