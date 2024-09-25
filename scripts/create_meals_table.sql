CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
DROP TABLE IF EXISTS MEALS;
CREATE TABLE public.meals (
    TIME TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    MEAL_ID UUID NOT NULL,
    USER_ID UUID NOT NULL,
    MEAL_NAME TEXT NOT NULL,
    CALORIES DOUBLE PRECISION NOT NULL,
    PRIMARY KEY (TIME, MEAL_ID, USER_ID)
);
SELECT CREATE_HYPERTABLE('meals', 'time');