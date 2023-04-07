SELECT messages.*
FROM (
    SELECT MAX(message_date) AS 'maxdate', IF (from_user = '$u', to_user, from_user) AS 'user'
    FROM messages
    WHERE from_user = '$u' or to_user = '$u'
    GROUP BY user
) AS a
INNER JOIN messages ON a.maxdate = message_date
ORDER BY message_date DESC