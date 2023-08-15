SELECT title FROM movies WHERE "year" = 2008;

SELECT birth FROM people WHERE "name" = 'Emma Stone';

SELECT title FROM movies WHERE "year" >= 2018 ORDER BY title ASC;

SELECT COUNT(*) AS cont_movie FROM ratings WHERE rating = 10;

SELECT title, "year" FROM movies WHERE title LIKE 'Harry Potter%' ORDER BY 2 ASC;

SELECT
    AVG(rating)
FROM ratings
INNER JOIN movies
    ON ratings.movie_id = movies.id
    AND movies.year = 2012;

SELECT
    movies.title,
    ratings.rating
FROM ratings
INNER JOIN movies
    ON ratings.movie_id = movies.id
    AND movies.year = 2010
ORDER BY 2 DESC, 1 ASC;

SELECT
    "name"
FROM people
WHERE id IN (SELECT
                person_id
             FROM stars
             WHERE movie_id IN (SELECT id FROM movies WHERE title LIKE '%Toy Story%'));

SELECT
    "name"
FROM people
WHERE id IN (SELECT
                person_id
             FROM stars
             WHERE movie_id IN (SELECT id FROM movies WHERE "year" = 2004 ))
ORDER BY birth ASC

SELECT
   "name"
FROM people
WHERE id IN (SELECT person_id
             FROM directors
             WHERE movie_id IN (SELECT movie_id FROM ratings WHERE rating >= 9));

SELECT movies.title
FROM ratings
INNER JOIN movies ON ratings.movie_id = movies.id
WHERE movie_id IN (
    SELECT movie_id FROM stars WHERE person_id IN (SELECT id FROM people WHERE "name" = 'Chadwick Boseman')
)
ORDER BY ratings.rating DESC
LIMIT 5;

SELECT
    movies.title
FROM stars
INNER JOIN people
    ON stars.person_id = people.id
    AND stars.person_id IN (SELECT id FROM people WHERE "name" IN ('Johnny Depp', 'Helena Bonham Carter'))
INNER JOIN movies
    ON stars.movie_id = movies.id
GROUP BY 1
HAVING SUM(CASE WHEN people.name IN ('Johnny Depp', 'Helena Bonham Carter') THEN 1 ELSE 0 END) >= 2;

SELECT "name"
FROM people
WHERE
    id NOT IN (SELECT id FROM people WHERE "name" = 'Kevin Bacon' AND birth = 1958)
    AND id IN (
        SELECT person_id FROM stars WHERE movie_id IN (
            SELECT movie_id
            FROM stars
            WHERE person_id IN (SELECT id FROM people WHERE "name" = 'Kevin Bacon' AND birth = 1958)
        )
    );