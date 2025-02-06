-- init-scripts/01_extensions.sql

-- Enable required PostgreSQL extensions
CREATE EXTENSION IF NOT EXISTS vector;      -- Enables vector similarity search capabilities
CREATE EXTENSION IF NOT EXISTS pg_trgm;     -- Provides trigram matching for text search
CREATE EXTENSION IF NOT EXISTS btree_gin;   -- Allows GIN indexes on more data types
CREATE EXTENSION IF NOT EXISTS "uuid-ossp"; -- Adds UUID generation capabilities
CREATE EXTENSION IF NOT EXISTS unaccent;   -- Removes accents from text for better search

CREATE OR REPLACE FUNCTION slugify(value TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN regexp_replace(
        regexp_replace(
            lower(unaccent(value)),
            '[^a-z0-9\-_]+', '-', 'gi'
        ),
        '(-+$|^-+)', '', 'g'
    );
END;
$$
 LANGUAGE plpgsql STRICT IMMUTABLE;

-- Optional: Set any extension-specific configurations
ALTER SYSTEM SET vectors.max_dim = 1536;   -- Configure maximum vector dimensions for your use case