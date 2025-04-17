--@exclude_input=ai_business_tech.aidc_managed_agent_new,ai_business_tech.aidc_agent_relation
--odps sql 
--********************************************************************--
--author:aihe
--create time:2024-10-15 16:16:23
--********************************************************************--

-- 使用WITH语法定义基础数据，后续各个报表查询都基于这些数据
WITH mcp_base_data AS 
(
    -- 基础数据：关联智能体和MCP
    SELECT  a.tenant_code
            ,a.creator_name
            ,a.creator_id
            ,a.agent_code
            ,a.name AS agent_name
            ,a.deployed_status
            ,a.gmt_create
            ,a.gmt_modified
            ,r.subject_id
            ,r.id AS relation_id
            ,a.env
    FROM    ai_business_tech.aidc_managed_agent_new a
    LEFT JOIN ai_business_tech.aidc_agent_relation r
    ON      a.id = r.managed_agent_id
    AND     r.type = 7
    AND     r.pt = '${bizdate}'
    AND     r.is_deleted = 0
    WHERE   a.pt = '${bizdate}'
    AND     a.is_deleted = 0
    AND     r.type = 7
)
,mcp_agent_stats AS 
(
    -- 按智能体统计MCP使用情况
    SELECT  tenant_code
            ,creator_name
            ,creator_id
            ,agent_code
            ,agent_name
            ,deployed_status
            ,gmt_create
            ,gmt_modified
            ,env
            ,subject_id
            ,COUNT(relation_id) AS mcp_count
    FROM    mcp_base_data
    GROUP BY tenant_code
             ,creator_name
             ,creator_id
             ,agent_code
             ,agent_name
             ,deployed_status
             ,gmt_create
             ,gmt_modified
             ,env
             ,subject_id
)

-- 报表1: 总体统计
SELECT  '总体统计' AS report_name
        ,COUNT(DISTINCT agent_code) AS total_agent_count
        ,COUNT(DISTINCT tenant_code) AS total_tenant_count
        ,COUNT(DISTINCT creator_id) AS total_creator_count
        ,COUNT(DISTINCT subject_id) AS total_mcp_endpoint_count
        ,SUM(mcp_count) AS total_mcp_count
FROM    mcp_agent_stats;

-- 报表2: 按时间维度统计MCP创建趋势
SELECT  '时间维度统计' AS report_name
        ,TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd') AS create_date
        ,COUNT(DISTINCT agent_code) AS new_agent_count
        ,COUNT(DISTINCT subject_id) AS new_mcp_endpoint_count
        ,SUM(mcp_count) AS new_mcp_count
FROM    mcp_agent_stats
GROUP BY TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd')
ORDER BY create_date;

-- 报表3: 按创建者统计MCP使用情况
SELECT  '创建者统计' AS report_name
        ,creator_name
        ,creator_id
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
GROUP BY creator_name
         ,creator_id
ORDER BY mcp_count DESC
LIMIT 20;

-- 报表4: 按环境统计MCP使用情况
SELECT  '环境统计' AS report_name
        ,env
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
GROUP BY env;

-- 报表5: 按部署状态统计MCP使用情况
SELECT  '部署状态统计' AS report_name
        ,deployed_status
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
GROUP BY deployed_status;

-- 报表6: 按租户统计MCP使用情况
SELECT  '租户统计' AS report_name
        ,tenant_code
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
GROUP BY tenant_code
ORDER BY mcp_count DESC
LIMIT 10;

-- 报表7: MCP数量分布
SELECT  'MCP数量分布' AS report_name
        ,mcp_count_range
        ,COUNT(DISTINCT agent_code) AS agent_count
FROM    (
            SELECT  agent_code
                    ,CASE
                        WHEN SUM(mcp_count) = 0 THEN '0'
                        WHEN SUM(mcp_count) = 1 THEN '1'
                        WHEN SUM(mcp_count) BETWEEN 2 AND 5 THEN '2-5'
                        WHEN SUM(mcp_count) BETWEEN 6 AND 10 THEN '6-10'
                        ELSE '10+'
                    END AS mcp_count_range
            FROM    mcp_agent_stats
            GROUP BY agent_code
        ) t
GROUP BY mcp_count_range
ORDER BY CASE
            WHEN mcp_count_range = '0' THEN 1
            WHEN mcp_count_range = '1' THEN 2
            WHEN mcp_count_range = '2-5' THEN 3
            WHEN mcp_count_range = '6-10' THEN 4
            ELSE 5
         END;

-- 报表8: MCP服务地址统计
SELECT  'MCP服务地址统计' AS report_name
        ,subject_id
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
WHERE   subject_id IS NOT NULL
GROUP BY subject_id
ORDER BY agent_count DESC
LIMIT 20;

-- 报表9: MCP域名统计
SELECT  'MCP域名统计' AS report_name
        ,REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1) AS domain
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
WHERE   subject_id IS NOT NULL
GROUP BY REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1)
ORDER BY agent_count DESC
LIMIT 20;

-- 报表10: 最近创建的带MCP的智能体
SELECT  '最近创建的智能体' AS report_name
        ,agent_code
        ,agent_name
        ,creator_name
        ,tenant_code
        ,gmt_create
        ,subject_id
        ,mcp_count
FROM    mcp_agent_stats
WHERE   mcp_count > 0
ORDER BY gmt_create DESC
LIMIT 20;

-- 报表11: 按日期统计MCP增长趋势（按周汇总）
SELECT  '周增长趋势' AS report_name
        ,CONCAT('第', CAST(WEEKOFYEAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss')) AS STRING), '周') AS week_of_year
        ,COUNT(DISTINCT agent_code) AS new_agent_count
        ,COUNT(DISTINCT subject_id) AS new_mcp_endpoint_count
        ,SUM(mcp_count) AS new_mcp_count
FROM    mcp_agent_stats
GROUP BY WEEKOFYEAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'))
ORDER BY WEEKOFYEAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'));

-- 报表12: 按月统计MCP增长趋势
SELECT  '月增长趋势' AS report_name
        ,TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm') AS month
        ,COUNT(DISTINCT agent_code) AS new_agent_count
        ,COUNT(DISTINCT subject_id) AS new_mcp_endpoint_count
        ,SUM(mcp_count) AS new_mcp_count
FROM    mcp_agent_stats
GROUP BY TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm')
ORDER BY month;

-- 报表13: 按创建者部门统计MCP使用情况（如果有部门信息）
-- 注意：此查询需要有部门信息表，如果没有可以忽略
-- SELECT  '部门统计' AS report_name
--         ,dept_name
--         ,COUNT(DISTINCT creator_id) AS creator_count
--         ,COUNT(DISTINCT agent_code) AS agent_count
--         ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
--         ,SUM(mcp_count) AS mcp_count
-- FROM    mcp_agent_stats a
-- LEFT JOIN user_dept_info b
-- ON      a.creator_id = b.user_id
-- GROUP BY dept_name
-- ORDER BY mcp_count DESC;

-- 报表14: MCP使用时长分布（基于创建时间到当前的时间差）
SELECT  'MCP使用时长分布' AS report_name
        ,usage_duration_range
        ,COUNT(DISTINCT agent_code) AS agent_count
FROM    (
            SELECT  agent_code
                    ,CASE
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 7 THEN '1周内'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 30 THEN '1-4周'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 90 THEN '1-3个月'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 180 THEN '3-6个月'
                        ELSE '6个月以上'
                    END AS usage_duration_range
            FROM    mcp_agent_stats
            WHERE   mcp_count > 0
            GROUP BY agent_code
                     ,CASE
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 7 THEN '1周内'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 30 THEN '1-4周'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 90 THEN '1-3个月'
                        WHEN DATEDIFF(TO_DATE('${bizdate}', 'yyyymmdd'), TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'dd') < 180 THEN '3-6个月'
                        ELSE '6个月以上'
                    END
        ) t
GROUP BY usage_duration_range
ORDER BY CASE
            WHEN usage_duration_range = '1周内' THEN 1
            WHEN usage_duration_range = '1-4周' THEN 2
            WHEN usage_duration_range = '1-3个月' THEN 3
            WHEN usage_duration_range = '3-6个月' THEN 4
            ELSE 5
         END;

-- 报表15: 按MCP服务地址类型统计
SELECT  'MCP服务地址类型统计' AS report_name
        ,CASE
            WHEN subject_id LIKE '%/sse%' THEN 'SSE模式'
            WHEN subject_id LIKE '%/sessions/%' THEN '会话模式'
            ELSE '其他模式'
         END AS mcp_type
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS endpoint_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_agent_stats
WHERE   subject_id IS NOT NULL
GROUP BY CASE
            WHEN subject_id LIKE '%/sse%' THEN 'SSE模式'
            WHEN subject_id LIKE '%/sessions/%' THEN '会话模式'
            ELSE '其他模式'
         END;
