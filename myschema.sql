DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;

CREATE TABLE users(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  email VARCHAR(255) NOT NULL,
  firstName VARCHAR(255) NOT NULL,
  lastName VARCHAR(255) NOT NULL,
  password VARCHAR(255) NOT NULL,
  authed BOOLEAN NOT NULL DEFAULT 0,
  UNIQUE(email)
);

CREATE TABLE posts(
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  created TIMESTAMP NOT NULL DEFAULT (datetime('now','localtime')),
  author INTEGER NOT NULL,
  title VARCHAR(255) NOT NULL,
  body VARCHAR(1000) NOT NULL,
  FOREIGN KEY (author) REFERENCES users(id)
);

INSERT INTO users(email, firstName, lastName, password, authed) VALUES(
"hortonwhy@gmail.com", "Wyatt", "Horton", "123", 1);

INSERT INTO users(email, firstName, lastName, password) VALUES(
"hortonwhy2@gmail.com", "John", "Adams", "123");


INSERT INTO posts(author, title, body) VALUES(
2, "My time in the south", "Was alright"
);

INSERT INTO posts(author, title, body) VALUES(
1, "A time from the north", "Was quite cold"
);
