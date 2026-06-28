# Database Schema - URL Shortener

## RDS MySQL

### Table: urls
| Column | Type | Description |
|--------|------|-------------|
| id | INT AUTO_INCREMENT | Primary Key |
| original_url | TEXT | The full long URL |
| short_code | VARCHAR(10) | The short code (e.g., abc123) |
| created_by | VARCHAR(255) | Email of creator |
| created_at | DATETIME | When URL was shortened |
| total_clicks | INT | Total number of clicks |

### Table: clicks
| Column | Type | Description |
|--------|------|-------------|
| id | INT AUTO_INCREMENT | Primary Key |
| short_code | VARCHAR(10) | Links to urls table |
| clicked_at | DATETIME | When the click happened |
| ip_address | VARCHAR(45) | Visitor IP address |
| country | VARCHAR(100) | Visitor country |

## DynamoDB

### Table: url-cache
| Attribute | Type | Description |
|-----------|------|-------------|
| short_code (PK) | String | Partition key for fast lookup |
| original_url | String | The full long URL |
| created_at | String | Creation timestamp |

### Table: click-analytics
| Attribute | Type | Description |
|-----------|------|-------------|
| short_code (PK) | String | Partition key |
| clicked_at (SK) | String | Sort key for time queries |
| ip_address | String | Visitor IP |
| country | String | Visitor country |
| expires_at | Number | TTL - auto delete after 90 days |

## Why Both Databases?

- RDS MySQL = Permanent storage, complex queries, reports
- DynamoDB = Ultra-fast lookups, URL redirect (milliseconds)
