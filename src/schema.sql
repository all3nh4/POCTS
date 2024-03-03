DROP TABLE IF EXISTS AlertSubscription;

CREATE TABLE AlertSubscription(
    id INTEGER PRIMARY KEY AUTOINCREMENT 
    email TEXT UNIQUE NOT NULL 
    trend_keyword = TEXT UNIQUE NOT NULL
    frequency = TEXT UNIQUE NOT NULL
);