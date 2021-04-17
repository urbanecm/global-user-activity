CREATE TABLE undos (
	wiki_db VARCHAR(10) NOT NULL,
	rev_id INT(8) UNSIGNED NOT NULL,
	rev_timestamp VARCHAR(14) NOT NULL,
	actor_name VARCHAR(255) NOT NULL,
	ctd_name VARCHAR(255) NOT NULL,

	INDEX (rev_timestamp),
	PRIMARY KEY(wiki_db, rev_id)
);
