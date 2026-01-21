-- 1. Tổng doanh thu toàn công ty
SELECT SUM(revenue) AS total_revenue
from dbo.sales_data_cleaned;

-- 2. Doanh thu theo năm
SELECT YEAR(order_date) as year,
		sum(revenue) as revenue
from dbo.sales_data_cleaned
group by year(order_date)
order by year;

--3. Doanh thu theo tháng
SELECT 
	year(order_date) as year,
	MONTH(order_date) as month,
	sum(revenue) as revenue
from dbo.sales_data_cleaned
group by year(order_date),month(order_date)
order by year, month;

--4. Doanh thu theo region
SELECT region as region, sum(revenue) as revenue
from dbo.sales_data_cleaned
group by region
order by revenue desc;

--5. Top store có doanh thu cao nhất
SELECT top 5
	store_id,
	sum(revenue) as revenue
from dbo.sales_data_cleaned
group by store_id
order by revenue desc;

--6.Top product bán chạy
SELECT product_id, sum(revenue) as revenue
from dbo.sales_data_cleaned
group by product_id
order by product_id desc;

--7.Phân loại đơn hàng theo giá trị
SELECT 
    order_id,
    revenue,
    CASE 
        WHEN revenue >= 100000000 THEN 'High Value'
        WHEN revenue >= 50000000 THEN 'Medium Value'
        ELSE 'Low Value'
    END AS order_type
FROM dbo.sales_data_cleaned;


--8.Top 3 store mỗi region
SELECT *
FROM (
    SELECT 
        region,
        store_id,
        SUM(revenue) AS revenue,
        RANK() OVER (
            PARTITION BY region
            ORDER BY SUM(revenue) DESC
        ) AS rank_in_region
    FROM dbo.sales_data_cleaned
    GROUP BY region, store_id
) t
WHERE rank_in_region <= 3;


--9.Doanh thu tích lũy theo thời gian
SELECT 
    order_date,
    SUM(revenue) AS daily_revenue,
    SUM(SUM(revenue)) OVER (
        ORDER BY order_date
    ) AS cumulative_revenue
FROM dbo.sales_data_cleaned
GROUP BY order_date
ORDER BY order_date;

--10.Tăng trưởng % MoM
SELECT 
    year,
    month,
    SUM(revenue) AS revenue,
    ROUND(
        (
            SUM(revenue) - LAG(SUM(revenue)) OVER (ORDER BY year, month)
        ) * 100.0
        / LAG(SUM(revenue)) OVER (ORDER BY year, month),
        2
    ) AS mom_growth_percent
FROM dbo.sales_data_cleaned
GROUP BY year, month
ORDER BY year, month;


