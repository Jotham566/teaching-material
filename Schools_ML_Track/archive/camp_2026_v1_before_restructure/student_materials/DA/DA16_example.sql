-- Worked example; your independent task belongs in a separate SQL file.
SELECT s.sale_id, s.item, p.category FROM sales AS s LEFT JOIN products AS p ON s.item = p.item ORDER BY s.sale_id;
