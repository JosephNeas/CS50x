SELECT title FROM movies, stars, people WHERE movies.id = stars.movie_id AND stars.person_id = people.id AND people.name = "Johnny Depp" AND movies.title IN
(SELECT title FROM movies, stars, people WHERE movies.id = stars.movie_id AND stars.person_id = people.id
AND people.name = "Helena Bonham Carter");