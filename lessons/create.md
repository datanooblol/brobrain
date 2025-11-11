# Creating Database Tables

## Basic CREATE TABLE Syntax

```sql
CREATE TABLE table_name (
    column_name data_type constraints,
    column_name data_type constraints,
    ...
);
```

## Handling Existing Tables

```sql
-- Check if table exists first (safe approach)
CREATE TABLE IF NOT EXISTS table_name (
    column_name data_type constraints
);

-- Drop existing table first (destructive)
DROP TABLE IF EXISTS table_name;
CREATE TABLE table_name (
    column_name data_type constraints
);

-- Replace existing table (MySQL/some databases)
CREATE OR REPLACE TABLE table_name (
    column_name data_type constraints
);
```

## Common Data Types

### Numeric Types
- `INTEGER` / `INT` - Whole numbers
- `DECIMAL(p,s)` - Fixed-point numbers (p=precision, s=scale)
- `FLOAT` / `REAL` - Floating-point numbers

### Text Types
- `VARCHAR(n)` - Variable-length string (max n characters)
- `CHAR(n)` - Fixed-length string (exactly n characters)
- `TEXT` - Large text data

### Date/Time Types
- `DATE` - Date only (YYYY-MM-DD)
- `TIME` - Time only (HH:MM:SS)
- `DATETIME` / `TIMESTAMP` - Date and time

### Boolean
- `BOOLEAN` - True/false values

## Common Constraints

### Column Constraints
- `NOT NULL` - Column cannot be empty
- `UNIQUE` - All values must be unique
- `PRIMARY KEY` - Unique identifier for each row
- `DEFAULT value` - Default value if none provided
- `CHECK (condition)` - Custom validation rule

### Table Constraints
- `PRIMARY KEY (column1, column2)` - Composite primary key
- `FOREIGN KEY (column) REFERENCES other_table(column)` - Links to another table
- `UNIQUE (column1, column2)` - Composite unique constraint

## Example: User Table

```sql
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE,
    age INTEGER CHECK (age >= 0 AND age <= 150)
);
```

## Example: Orders Table with Foreign Key

```sql
CREATE TABLE orders (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL CHECK (total_amount >= 0),
    order_date DATE DEFAULT CURRENT_DATE,
    status VARCHAR(20) DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES users(id)
);
```

## Key Points

1. **Primary Key** - Every table should have one
2. **NOT NULL** - Use for required fields
3. **Data Types** - Choose appropriate size/type for your data
4. **Constraints** - Enforce data integrity at database level
5. **Foreign Keys** - Maintain relationships between tables