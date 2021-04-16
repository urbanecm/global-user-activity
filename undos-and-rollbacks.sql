SELECT
	REPLACE(DATABASE(), "_p", "") AS wiki_db,
	rev_id,
	rev_timestamp,
	actor_name,
	ctd_name
FROM change_tag
JOIN change_tag_def ON ct_tag_id=ctd_id
JOIN revision ON rev_id=ct_rev_id
JOIN actor ON actor_id=rev_actor
WHERE
	ctd_name IN ("mw-undo", "mw-rollback")
;
