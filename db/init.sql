CREATE TABLE IF NOT EXISTS notifications (
              id serial CONSTRAINT notifications_pk PRIMARY KEY,
              title VARCHAR(50) NOT NULL,
              body TEXT NOT NULL,
              send_to VARCHAR(50) NOT NULL,
              send_at TIMESTAMP NOT NULL,
              is_sent BOOLEAN NOT NULL DEFAULT FALSE,
              is_deleted BOOLEAN NOT NULL DEFAULT FALSE
)
