SELECT * FROM messages WHERE (from_user = '$current' AND to_user = '$address')
OR (from_user = '$address' and to_user = '$current') ORDER BY message_date