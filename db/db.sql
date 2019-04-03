CREATE TABLE ACCOUNT_INFO(
	A_USERNAME VARCHAR(80), #stores username
    A_EMAIL VARCHAR(80) NOT NULL UNIQUE, #stores email address
    A_PASSWORD VARCHAR(255) NOT NULL, #stores password
    A_CREATION_DATE TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, #stores timestamp of account creation automatically when new account added to this table
    PRIMARY KEY(A_USERNAME)
);

