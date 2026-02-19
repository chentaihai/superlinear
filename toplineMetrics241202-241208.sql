SELECT
    -- 流量与参与度
    SUM(dm.visitors) AS total_visitors,
    SUM(dm.page_views) AS total_page_views,
    -- 转化漏斗
    SUM(dm.add_to_carts) AS total_add_to_carts,
    SUM(dm.checkouts) AS total_checkouts,
    SUM(dm.purchases) AS total_purchases,
    -- 收入指标
    SUM(dm.total_revenue) AS total_revenue,
    SUM(dm.total_revenue) / SUM(dm.purchases) AS avg_order_value,
    -- 质量与服务
    SUM(dm.return_rate * dm.purchases) / SUM(dm.purchases) AS weighted_return_rate,
    SUM(dm.support_tickets) AS total_support_tickets,
    -- 核心转化率
    ROUND(100.0 * SUM(dm.purchases) / SUM(dm.visitors), 2) AS conversion_rate
FROM daily_metrics dm
JOIN dates d ON dm.date_id = d.date_id
WHERE d.date BETWEEN '2024-12-02' AND '2024-12-08';
