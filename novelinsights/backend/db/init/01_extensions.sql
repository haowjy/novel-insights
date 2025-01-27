-- init-scripts/01_extensions.sql

-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS vector;      -- Enables vector similarity search capabilities
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- Provides trigram matching for text search
CREATE EXTENSION IF NOT EXISTS btree_gin;   -- Allows GIN indexes on more data types
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Adds UUID generation capabilities

-- Optional: Set any extension-specific configurations
ALTER SYSTEM SET vectors.max_dim = 1536;   -- Configure maximum vector dimensions for your use case