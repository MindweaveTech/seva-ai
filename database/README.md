# Smart AI - Database

Database schemas, migrations, and management scripts for Smart AI.

## Overview

The project uses two primary databases:
- **PostgreSQL** - Relational database for structured data, user info, chat history, health metrics
- **Weaviate** - Vector database for conversation embeddings and semantic search (RAG)

## Tech Stack

- **PostgreSQL** 15+
- **Weaviate** 1.22+
- **Alembic** - Python database migrations
- **SQLAlchemy** - ORM

## Directory Structure

```
database/
├── postgresql/
│   ├── migrations/         # Alembic migration files
│   ├── schemas/            # SQL schema definitions
│   │   ├── init.sql
│   │   ├── triggers.sql
│   │   ├── functions.sql
│   │   └── indexes.sql
│   ├── seeds/              # Seed data scripts
│   │   ├── dev_data.sql
│   │   └── seed.py
│   └── scripts/            # Utility scripts
│       ├── backup.sh
│       ├── restore.sh
│       └── maintenance.sql
├── weaviate/
│   └── schemas/
│       └── conversation_schema.json
└── README.md
```

## PostgreSQL

### Database Schema

The database consists of 12 core tables:

1. **users** - User accounts and authentication
2. **user_profiles** - Extended user information
3. **devices** - Registered devices for each user
4. **conversation_sessions** - Chat sessions
5. **chat_messages** - Individual messages
6. **health_metrics** - Health data points
7. **behavioral_patterns** - Detected user patterns
8. **alerts** - Health and behavioral alerts
9. **caregiver_relationships** - User-caregiver associations
10. **notification_preferences** - User notification settings
11. **audit_logs** - Compliance audit trail
12. **sync_queue** - Offline sync tracking

See [../docs/ARCHITECTURE.md](../docs/ARCHITECTURE.md) for detailed schema documentation.

### Setup

#### Using Docker

```bash
# Start PostgreSQL
docker run -d \
  --name seva-postgres \
  -e POSTGRES_DB=seva_ai \
  -e POSTGRES_USER=seva_user \
  -e POSTGRES_PASSWORD=seva_password \
  -p 5432:5432 \
  postgres:15-alpine
```

#### Manual Installation

1. **Install PostgreSQL**
   ```bash
   # Ubuntu/Debian
   sudo apt-get install postgresql-15

   # macOS
   brew install postgresql@15
   ```

2. **Create database**
   ```bash
   createdb seva_ai
   ```

3. **Initialize schema**
   ```bash
   psql -d seva_ai -f postgresql/schemas/init.sql
   ```

### Migrations with Alembic

Migrations are managed from the backend service:

```bash
cd ../backend

# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View history
alembic history
```

### Seeding Data

For development and testing:

```bash
# SQL seed data
psql -d seva_ai -f postgresql/seeds/dev_data.sql

# Python seed script
cd postgresql/seeds
python seed.py
```

### Backup & Restore

#### Backup

```bash
# Full backup
./postgresql/scripts/backup.sh

# Or manually
pg_dump seva_ai > backup_$(date +%Y%m%d_%H%M%S).sql

# Backup with compression
pg_dump seva_ai | gzip > backup_$(date +%Y%m%d_%H%M%S).sql.gz
```

#### Restore

```bash
# Restore from backup
./postgresql/scripts/restore.sh backup_file.sql

# Or manually
psql -d seva_ai < backup_file.sql

# From compressed backup
gunzip -c backup_file.sql.gz | psql -d seva_ai
```

#### Automated Backups

Setup cron job for daily backups:

```bash
# Edit crontab
crontab -e

# Add daily backup at 2 AM
0 2 * * * /path/to/seva-ai/database/postgresql/scripts/backup.sh
```

### Maintenance

#### Vacuum and Analyze

```bash
psql -d seva_ai -f postgresql/scripts/maintenance.sql
```

Or manually:
```sql
-- Vacuum all tables
VACUUM ANALYZE;

-- Vacuum specific table
VACUUM ANALYZE chat_messages;

-- Full vacuum (more aggressive, requires exclusive lock)
VACUUM FULL;
```

#### Index Maintenance

```sql
-- Rebuild all indexes
REINDEX DATABASE seva_ai;

-- Rebuild specific index
REINDEX INDEX idx_messages_user_time;

-- Check for missing indexes
SELECT schemaname, tablename, indexname
FROM pg_indexes
WHERE schemaname = 'public';
```

#### Monitor Performance

```sql
-- Check table sizes
SELECT
  tablename,
  pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Check slow queries
SELECT query, calls, total_time, mean_time
FROM pg_stat_statements
ORDER BY mean_time DESC
LIMIT 10;

-- Check index usage
SELECT
  schemaname,
  tablename,
  indexname,
  idx_scan,
  idx_tup_read,
  idx_tup_fetch
FROM pg_stat_user_indexes
ORDER BY idx_scan DESC;
```

### Connection Pooling

For production, use connection pooling:

**PgBouncer:**
```ini
[databases]
seva_ai = host=localhost port=5432 dbname=seva_ai

[pgbouncer]
pool_mode = transaction
max_client_conn = 1000
default_pool_size = 20
```

### Security

#### User Permissions

```sql
-- Create read-only user for analytics
CREATE USER seva_analytics WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE seva_ai TO seva_analytics;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO seva_analytics;

-- Create app user with limited permissions
CREATE USER seva_app WITH PASSWORD 'secure_password';
GRANT CONNECT ON DATABASE seva_ai TO seva_app;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO seva_app;
GRANT USAGE, SELECT ON ALL SEQUENCES IN SCHEMA public TO seva_app;
```

#### SSL Connections

```bash
# postgresql.conf
ssl = on
ssl_cert_file = '/path/to/server.crt'
ssl_key_file = '/path/to/server.key'
```

#### Encryption at Rest

Use PostgreSQL's transparent data encryption (TDE) or filesystem-level encryption (LUKS, dm-crypt).

---

## Weaviate

### Vector Database Schema

Weaviate stores conversation embeddings for semantic search in the RAG pipeline.

### Setup

#### Using Docker

```bash
docker run -d \
  --name seva-weaviate \
  -p 8080:8080 \
  -e QUERY_DEFAULTS_LIMIT=25 \
  -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=false \
  -e PERSISTENCE_DATA_PATH='/var/lib/weaviate' \
  semitechnologies/weaviate:1.22.4
```

#### Initialize Schema

```bash
# Import schema
curl -X POST http://localhost:8080/v1/schema \
  -H "Content-Type: application/json" \
  -d @weaviate/schemas/conversation_schema.json
```

### Schema Definition

```json
{
  "class": "ConversationEmbedding",
  "description": "Conversation message embeddings for semantic search",
  "vectorizer": "none",
  "properties": [
    {
      "name": "messageId",
      "dataType": ["string"],
      "description": "UUID of the chat message"
    },
    {
      "name": "userId",
      "dataType": ["string"],
      "description": "UUID of the user"
    },
    {
      "name": "text",
      "dataType": ["text"],
      "description": "Message content"
    },
    {
      "name": "timestamp",
      "dataType": ["date"],
      "description": "Message timestamp"
    },
    {
      "name": "sender",
      "dataType": ["string"],
      "description": "Message sender: user or ai"
    },
    {
      "name": "metadata",
      "dataType": ["object"],
      "description": "Additional metadata"
    }
  ]
}
```

### Backup & Restore

```bash
# Backup Weaviate data
docker exec seva-weaviate tar czf - /var/lib/weaviate > weaviate_backup.tar.gz

# Restore Weaviate data
docker exec -i seva-weaviate tar xzf - -C / < weaviate_backup.tar.gz
```

### Monitoring

```bash
# Health check
curl http://localhost:8080/v1/meta

# Check schema
curl http://localhost:8080/v1/schema

# Check object count
curl http://localhost:8080/v1/objects?limit=0
```

---

## Production Considerations

### High Availability

#### PostgreSQL
- Use streaming replication for read replicas
- Setup automatic failover with Patroni or Stolon
- Use connection pooling (PgBouncer)

#### Weaviate
- Run multi-node cluster
- Configure replication factor
- Use load balancer

### Scaling

#### PostgreSQL
- Vertical scaling: Increase CPU, RAM, storage
- Horizontal scaling: Read replicas for queries
- Partitioning: Partition large tables (chat_messages, health_metrics)

#### Weaviate
- Horizontal scaling: Add more nodes
- Sharding: Distribute data across nodes

### Monitoring

**PostgreSQL:**
- pg_stat_statements for query performance
- pg_stat_user_tables for table statistics
- Prometheus exporter for metrics

**Weaviate:**
- Prometheus metrics endpoint
- Grafana dashboards
- Custom health checks

### Costs

**Development (local):**
- Free (Docker)

**Production (AWS RDS/Self-hosted):**
- PostgreSQL RDS: $200-500/month (db.t3.medium - db.m5.large)
- Weaviate (self-hosted on EKS): $300-600/month (3 nodes)

---

## Troubleshooting

### PostgreSQL

**Connection refused**
```bash
# Check if PostgreSQL is running
sudo systemctl status postgresql

# Check logs
sudo tail -f /var/log/postgresql/postgresql-15-main.log
```

**Slow queries**
```sql
-- Enable slow query logging
ALTER SYSTEM SET log_min_duration_statement = 1000; -- Log queries > 1s
SELECT pg_reload_conf();

-- Check long-running queries
SELECT pid, now() - query_start AS duration, query
FROM pg_stat_activity
WHERE state = 'active' AND now() - query_start > interval '5 seconds'
ORDER BY duration DESC;
```

**Disk space issues**
```sql
-- Find largest tables
SELECT tablename, pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename))
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;

-- Archive old data
-- Move old messages to archive table
INSERT INTO chat_messages_archive
SELECT * FROM chat_messages WHERE created_at < NOW() - INTERVAL '1 year';

DELETE FROM chat_messages WHERE created_at < NOW() - INTERVAL '1 year';
```

### Weaviate

**Connection errors**
```bash
# Check if Weaviate is running
docker ps | grep weaviate

# Check logs
docker logs seva-weaviate
```

**Slow searches**
- Check index configuration
- Verify adequate resources (RAM)
- Consider reducing vector dimensions

## Contributing

See main repository [CONTRIBUTING.md](../CONTRIBUTING.md)

## License

MIT License - see LICENSE file for details
