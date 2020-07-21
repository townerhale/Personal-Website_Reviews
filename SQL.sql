CREATE TABLE users
(
	userid integer primary key,
	firstname character varying(40) NOT NULL,
	lastname character varying(40) NOT NULL,
	email character varying(40) NOT NULL,
	password character varying(40) NOT NULL,
	bio varchar(500),

	CONSTRAINT users_email_key UNIQUE (email)

);

INSERT INTO users (firstname, lastname, email, password, bio) VALUES ('Emil', 'Pop', 'Emil@Pop.com', 'password', 'uea student');

CREATE TABLE reviews
(
	reviewid integer primary key,
	reviewtitle character varying(40) NOT NULL,
	reviewdate date NOT NULL,
	reviewrating int NOT NULL,
	reviewauthor int NOT NULL,
	reviewtext varchar(5000) NOT NULL,
	up_votes integer,
	down_votes integer
);

INSERT INTO reviews (reviewtitle, reviewdate, reviewrating, reviewauthor, reviewtext) VALUES ('Title', '2018-10-08', 5, 1, 'Text text text text text');

CREATE TABLE admins
(
    adminid int NOT NULL,  -- User ID
    FOREIGN KEY (adminid) REFERENCES users(userid)
);

INSERT INTO admins VALUES (1);

CREATE TABLE comments
(
    commentid integer primary key,
	commentreviewid integer NOT NULL,
	commentuserid integer NOT NULL,
	commentdate date NOT NULL,
	comment varchar(1000) NOT NULL,
    FOREIGN KEY (commentreviewid) REFERENCES reviews(reviewid)
);