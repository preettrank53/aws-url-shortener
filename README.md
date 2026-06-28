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

## Development Roadmap

This project is implemented in structured phases to establish architecture, configure storage, develop the service layer, and automate cloud deployment.

### Phase 1: Foundation and S3 Static Hosting (Completed)
- Establish project workspace and directory layout.
- Configure version control guidelines and gitignore.
- Create static frontend placeholder for verification.
- Set up S3 Static Hosting and configure logs/bucket parameters.

### Phase 2: Security Groups and Database Provisioning (Completed)
- Define and provision Security Groups (sg-load-balancer, sg-ec2-app, sg-rds-database).
- Establish traffic flow constraints (RDS limited to EC2 security group, EC2 accessible via ALB).
- Provision RDS MySQL instance for permanent relational metadata.
- Provision DynamoDB tables (url-cache, click-analytics) for rapid caching and click tracing.
- Document system schema in database-schema.md.

### Phase 3: Application Development (In Progress)
- Implement backend URL shortening service using FastAPI.
- Integrate DynamoDB client logic for low-latency redirections.
- Integrate MySQL DB operations for analytical aggregation.

### Phase 4: EC2 and Load Balancer Deployment (Pending)
- Deploy Application Load Balancer and configure target groups.
- Set up EC2 instances within security constraints.
- Automate configuration with startup scripts.

## License

This project is licensed under the MIT License - see the LICENSE file for details.