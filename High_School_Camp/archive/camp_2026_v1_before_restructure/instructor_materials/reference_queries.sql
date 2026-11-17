-- Run against camp_shop.sqlite; instructor reference, not student assessment work.
SELECT COUNT(*) AS records,SUM(units) AS units,SUM(units*unit_price_ugx) AS revenue_ugx FROM sales;
SELECT item,SUM(units),SUM(units*unit_price_ugx),COUNT(*) FROM sales GROUP BY item ORDER BY item;
SELECT p.category,SUM(s.units*s.unit_price_ugx) FROM sales s JOIN products p ON s.item=p.item GROUP BY p.category ORDER BY p.category;
SELECT COUNT(*) FROM sales WHERE units>=5;
