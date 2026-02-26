USE traveldb;

CREATE TABLE IF NOT EXISTS users (
  user_id CHAR(32) PRIMARY KEY,
  username VARCHAR(120) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  -- Store creation time as Unix epoch seconds
  created_at BIGINT NOT NULL
);

CREATE TABLE IF NOT EXISTS destinations (
  destination_id CHAR(32) PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  date_from DATE NOT NULL,
  date_to DATE NOT NULL,
  description TEXT,
  location VARCHAR(255) NOT NULL,
  country VARCHAR(255) NOT NULL,
  user_id CHAR(32) NOT NULL,
  -- Store creation/update time as Unix epoch seconds
  created_at BIGINT NOT NULL,
  updated_at BIGINT NOT NULL,
  CONSTRAINT fk_dest_user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE
);