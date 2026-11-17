-- Worked example; your independent task belongs in a separate SQL file.
SELECT item, units FROM sales WHERE item = 'Book' AND units >= 5 ORDER BY units DESC, sale_id LIMIT 5;
