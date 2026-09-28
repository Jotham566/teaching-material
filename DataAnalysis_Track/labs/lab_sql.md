# Lab: SQL — getting the rows you asked for
### Sessions 3, 4 and 5 · Riverside Distributors · `data/riverside.db`

Open `riverside.db` in **DB Browser for SQLite**: File, Open Database, then
the *Execute SQL* tab. Nothing to install beyond the browser itself, and
nothing you type here can damage the file as long as you only write SELECT.

**The tables.** Six of them, and the shape matters more than the names:

| Table | Rows | One row is |
|---|---|---|
| `customers` | 401 | a business that buys from us |
| `products` | 120 | something we sell |
| `reps` | 12 | a sales rep, who belongs to one region |
| `orders` | 6,000 | one order, on one date, by one rep |
| `order_items` | 20,234 | one product on one order |
| `returns` | 501 | one returned line, with a reason |

`orders` has one row per order and `order_items` has one row per product on
that order. That single fact is behind most wrong answers in SQL, so say it
out loud before you start.

**Revenue, for the whole course, is** `quantity * unit_price_ugx *
(1 - discount)`. Amounts are Ugandan shillings.

---

## The eight questions

Work them in order. Each one has the query and the answer, so check yourself
as you go rather than at the end. Write the query before you read the answer:
reading it first feels like learning and is not.

### 1. How many orders are in the database?

```sql
SELECT COUNT(*) FROM orders;
```

**Answer:** 6,000

Start here so you have a number to check every later filter against.

### 2. How many were delivered, and how many cancelled?

```sql
SELECT status, COUNT(*) AS orders
FROM orders
GROUP BY status
ORDER BY orders DESC;
```

**Answer:** Delivered 4,837, Pending, Cancelled 575

Three statuses, and from here on every revenue question has to say which of them it counts.

### 3. Compare COUNT(*) with COUNT(customer_id) on the orders table. Why do they differ?

```sql
SELECT COUNT(*) AS rows_in_table,
       COUNT(customer_id) AS rows_with_a_customer
FROM orders;
```

**Answer:** 6,000 rows, 5,828 with a customer

COUNT(*) counts rows. COUNT(column) counts rows where that column is not NULL. The gap is 172 walk-in orders with no customer recorded, and it is the single most useful thing in this session.

### 4. Which sales channel is used most?

```sql
SELECT channel, COUNT(*) AS orders
FROM orders
GROUP BY channel
ORDER BY orders DESC;
```

**Answer:** WhatsApp 1,237, Field visit 1,206, Online 1,201, Walk-in 1,183, Phone 1,173

GROUP BY plus ORDER BY on the aggregate. Note you can order by something you computed.

### 5. Which customer segments have more than 80 customers?

```sql
SELECT segment, COUNT(*) AS customers
FROM customers
GROUP BY segment
HAVING COUNT(*) > 80
ORDER BY customers DESC;
```

**Answer:** Supermarket 103, Institution 85

HAVING filters groups; WHERE filters rows. Try it with WHERE and read the error: that error is worth more than the answer.

### 6. What is total revenue across every order line, before any filtering?

```sql
SELECT SUM(quantity * unit_price_ugx * (1 - discount)) AS revenue_ugx
FROM order_items;
```

**Answer:** UGX 10,758,894,480

Revenue is a calculation, not a column, and this is the definition used for the rest of the course: quantity x price x (1 - discount).

### 7. Now revenue for delivered orders only.

```sql
SELECT SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount))
         AS revenue_ugx
FROM order_items oi
JOIN orders o ON o.order_id = oi.order_id
WHERE o.status = 'Delivered';
```

**Answer:** UGX 8,751,705,520

The first join. UGX 2,007,188,960 of the unfiltered total is sitting in pending and cancelled orders, which is why 'revenue' with no qualifier is not an answer.

### 8. Revenue by region, delivered orders only.

```sql
SELECT c.region,
       SUM(oi.quantity * oi.unit_price_ugx * (1 - oi.discount))
         AS revenue_ugx
FROM order_items oi
JOIN orders o    ON o.order_id    = oi.order_id
JOIN customers c ON c.customer_id = o.customer_id
WHERE o.status = 'Delivered'
GROUP BY c.region
ORDER BY revenue_ugx DESC;
```

**Answer:** Eastern UGX 2,514,623,935, Northern UGX 2,107,303,745, Central UGX 2,022,616,760, Western UGX 1,810,419,785

Three tables. And a trap: this total is LOWER than the delivered total above, because joining to customers drops the 172 walk-in orders. That is UGX 390,632,335 of revenue gone with no warning.


---

## Session 5: the report the sales manager actually wants

> Revenue by rep by month for 2025, net of returns.

Ranking and running totals are deliberately NOT part of this. SQL does both,
with window functions, and they are a session's worth of new ideas eight days
after your first SELECT. Export this result and rank it in the spreadsheet,
where you are already fluent.

Build it in three steps, using two CTEs and a final SELECT. A CTE is just a named query you can use
like a table, and three short named steps are readable by somebody who did
not write them, which nested subqueries are not.

```sql
WITH lines AS (
    -- step 1: one row per order line, with its month and its rep
    SELECT o.rep_id,
           substr(o.order_date, 1, 7)                        AS month,
           oi.line_no,
           oi.quantity * oi.unit_price_ugx * (1 - oi.discount) AS gross_ugx
    FROM order_items oi
    JOIN orders o ON o.order_id = oi.order_id
    WHERE o.status = 'Delivered'
      AND o.order_date >= '2025-01-01'
      AND o.order_date < '2026-01-01'
),
net AS (
    -- step 2: subtract what came back. LEFT JOIN, because most lines have
    -- no return and an INNER JOIN here would silently keep only the
    -- returned ones.
    SELECT l.rep_id, l.month,
           SUM(l.gross_ugx) AS gross_ugx,
           SUM(COALESCE(rt.quantity_returned, 0) * oi.unit_price_ugx
               * (1 - oi.discount)) AS returned_ugx
    FROM lines l
    JOIN order_items oi ON oi.line_no = l.line_no
    LEFT JOIN (
        -- Combine repeat return events first, so each sales line stays once.
        SELECT line_no, SUM(quantity_returned) AS quantity_returned
        FROM returns GROUP BY line_no
    ) rt ON rt.line_no = l.line_no
    GROUP BY l.rep_id, l.month
)
-- step 3: name the reps and show each monthly net amount
SELECT r.region,
       r.rep_name,
       n.month,
       ROUND(n.gross_ugx)                      AS gross_ugx,
       ROUND(n.returned_ugx)                   AS returned_ugx,
       ROUND(n.gross_ugx - n.returned_ugx)     AS net_ugx
FROM net n
JOIN reps r ON r.rep_id = n.rep_id
ORDER BY r.region, r.rep_name, n.month;
```

**Check it against these,** which are the top three reps by 2025 revenue
before returns are taken off:

- **Hellen Hakizimana** — UGX 1,204,303,210
- **Brian Lubega** — UGX 976,461,330
- **David Wanyama** — UGX 915,808,445

Total value of everything returned, across both years: **UGX 197,830,550**.

### What to hand in
Submit one `.sql` file. The automatic mark is 25 points each for the correct
rep/month grain, gross amount, returned amount and net amount. Use the six
output columns shown above, with no duplicate rep/month keys. Amounts are
checked within 1 UGX after rounding; extra or missing rows reduce credit.
Add a SQL comment naming which rep you would talk to first and why. Discuss
that judgement in class; it is not a separately marked prose submission.

---

## Break it on purpose

Do these three after it works. Each takes one minute and each teaches
something that will otherwise cost you a day.

1. **Change the `LEFT JOIN` on the grouped returns to `JOIN`.** Revenue collapses, because
   now only the returned lines survive. Note the new number.
2. **Remove `WHERE o.status = 'Delivered'`.** Revenue rises by
   UGX 2,007,188,960, all of it from orders nobody paid for.
3. **Join `orders` to `customers` with an ordinary `JOIN`** and total the
   revenue. It falls by UGX 390,632,335, because 172 walk-in orders
   have no customer to join to. Nothing warns you. The only tell is that the
   row count moved, which is why you check the row count after every join.
