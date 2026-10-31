-- Worked example; your independent task belongs in a separate SQL file.
SELECT item, SUM(units * unit_price_ugx) AS revenue_ugx FROM sales GROUP BY item ORDER BY revenue_ugx DESC, item;
