CREATE SCHEMA api_json;

CREATE TABLE IF NOT EXISTS api_json.users (
    id INTEGER,
    name VARCHAR(255),
    username VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    website VARCHAR(255),
    suite VARCHAR(255),
    city VARCHAR(255),
    zipcode VARCHAR(255),
    lat VARCHAR(255),
    lng VARCHAR(255),
    catchPhrase VARCHAR(255));

CREATE TABLE IF NOT EXISTS api_json.posts (
    userId INTEGER,
    id INTEGER,
    title VARCHAR(255),
    body VARCHAR(255));
