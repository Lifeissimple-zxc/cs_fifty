SELECT
    SUM(energy * CAST(duration_ms AS REAL) / total_duration) / SUM(energy) AS weighted
FROM songs
CROSS JOIN (SELECT SUM(duration_ms) AS total_duration FROM songs)
