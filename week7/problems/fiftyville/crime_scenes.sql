SELECT
    id, "description"
FROM crime_scene_reports
WHERE
    "month" = 7
    AND "day" = 28
    AND "year" = 2021
    AND street = 'Humphrey Street'