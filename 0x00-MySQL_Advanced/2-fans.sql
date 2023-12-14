-- Ranks country origins of bands, ordered by the number of (non-unique) fans
SELECT country AS origin, SUM(fans) as nb_fans
FROM metal_bands
GROUP BY country
ORDER BY nb_fans DESC;