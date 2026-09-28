-- Worked example; your independent task belongs in a separate SQL file.
SELECT COUNT(*) AS missing_units FROM sales WHERE units IS NULL;
SELECT MIN(units) AS smallest, MAX(units) AS largest FROM sales;
