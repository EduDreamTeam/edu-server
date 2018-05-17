CREATE TABLE languages
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    title VARCHAR(128)
);
CREATE TABLE translations
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    src_word_id INT(11),
    tgt_word_id INT(11),
    CONSTRAINT translations_ibfk_1 FOREIGN KEY (src_word_id) REFERENCES words (id),
    CONSTRAINT translations_ibfk_2 FOREIGN KEY (tgt_word_id) REFERENCES words (id)
);
CREATE INDEX tgt_word_id ON translations (tgt_word_id);
CREATE UNIQUE INDEX uc ON translations (src_word_id, tgt_word_id);
CREATE TABLE users
(
    login VARCHAR(128) PRIMARY KEY NOT NULL,
    password VARCHAR(128),
    firstName VARCHAR(128),
    lastName VARCHAR(128),
    email VARCHAR(128)
);
CREATE TABLE users_translations
(
    user_login VARCHAR(128),
    translation_id INT(11),
    CONSTRAINT users_translations_ibfk_1 FOREIGN KEY (user_login) REFERENCES users (login),
    CONSTRAINT users_translations_ibfk_2 FOREIGN KEY (translation_id) REFERENCES translations (id)
);
CREATE INDEX translation_id ON users_translations (translation_id);
CREATE INDEX user_login ON users_translations (user_login);
CREATE TABLE words
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    text VARCHAR(128),
    language_id INT(11),
    CONSTRAINT words_ibfk_1 FOREIGN KEY (language_id) REFERENCES languages (id)
);
CREATE INDEX language_id ON words (language_id);
CREATE TABLE results
(
    id INT(11) PRIMARY KEY NOT NULL AUTO_INCREMENT,
    user_login VARCHAR(128),
    result FLOAT,
    date DATETIME,
    CONSTRAINT results_ibfk_1 FOREIGN KEY (user_login) REFERENCES users (login)
);
CREATE INDEX user_login ON results (user_login);