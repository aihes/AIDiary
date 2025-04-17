--@exclude_input=ai_business_tech.aidc_managed_agent_new,ai_business_tech.aidc_agent_relation
--odps sql
--********************************************************************--
--author:aihe
--create time:2024-10-15 16:16:23
--********************************************************************--

-- 创建存储MCP使用统计数据的表
CREATE TABLE IF NOT EXISTS mcp_usage_stats
(
    tenant_code            STRING COMMENT '租户代码'
    ,creator_name          STRING COMMENT '创建者名称'
    ,creator_id            STRING COMMENT '创建者ID'
    ,agent_code            STRING COMMENT '智能体代码'
    ,agent_name            STRING COMMENT '智能体名称'
    ,deployed_status       BIGINT COMMENT '部署状态'
    ,gmt_create            STRING COMMENT '创建时间'
    ,gmt_modified          STRING COMMENT '修改时间'
    ,mcp_count             BIGINT COMMENT 'MCP关联数量'
    ,env                   STRING COMMENT '环境'
    ,subject_id            STRING COMMENT 'MCP服务地址'
)
COMMENT 'MCP使用统计数据'
PARTITIONED BY
(
    ds                     STRING COMMENT '分区日期'
)
LIFECYCLE 365
;

-- 1. 按租户统计MCP使用情况
INSERT OVERWRITE TABLE mcp_usage_stats PARTITION (ds = '${bizdate}')
SELECT  a.tenant_code
        ,a.creator_name
        ,a.creator_id
        ,a.agent_code
        ,a.name AS agent_name
        ,a.deployed_status
        ,a.gmt_create
        ,a.gmt_modified
        ,COUNT(r.id) AS mcp_count
        ,a.env
        ,r.subject_id
FROM    ai_business_tech.aidc_managed_agent_new a
LEFT JOIN ai_business_tech.aidc_agent_relation r
ON      a.id = r.managed_agent_id
AND     r.type = 7
AND     r.pt = '${bizdate}'
AND     r.is_deleted = 0
WHERE   a.pt = '${bizdate}'
AND     a.is_deleted = 0
AND     r.type = 7
GROUP BY a.tenant_code
         ,a.creator_name
         ,a.creator_id
         ,a.agent_code
         ,a.name
         ,a.deployed_status
         ,a.gmt_create
         ,a.gmt_modified
         ,a.env
         ,r.subject_id
;

-- 2. 按时间维度统计MCP创建趋势
SELECT  TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd') AS create_date
        ,COUNT(DISTINCT agent_code) AS new_agent_count
        ,SUM(mcp_count) AS new_mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
GROUP BY TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd')
ORDER BY create_date
;

-- 3. 按创建者统计MCP使用情况
SELECT  creator_name
        ,creator_id
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
GROUP BY creator_name
         ,creator_id
ORDER BY mcp_count DESC
LIMIT 20
;

-- 4. 按环境统计MCP使用情况
SELECT  env
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
GROUP BY env
;

-- 5. 按部署状态统计MCP使用情况
SELECT  deployed_status
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
GROUP BY deployed_status
;

-- 6. 统计每个智能体关联的MCP数量分布
SELECT  mcp_count_range
        ,COUNT(DISTINCT agent_code) AS agent_count
FROM    (
            SELECT  agent_code
                    ,CASE
                        WHEN mcp_count = 0 THEN '0'
                        WHEN mcp_count = 1 THEN '1'
                        WHEN mcp_count BETWEEN 2 AND 5 THEN '2-5'
                        WHEN mcp_count BETWEEN 6 AND 10 THEN '6-10'
                        ELSE '10+'
                    END AS mcp_count_range
            FROM    mcp_usage_stats
            WHERE   ds = '${bizdate}'
        ) t
GROUP BY mcp_count_range
ORDER BY CASE
            WHEN mcp_count_range = '0' THEN 1
            WHEN mcp_count_range = '1' THEN 2
            WHEN mcp_count_range = '2-5' THEN 3
            WHEN mcp_count_range = '6-10' THEN 4
            ELSE 5
         END
;

-- 7. 统计最近7天MCP使用趋势（需要历史数据）
-- 注意：此查询需要历史分区数据，如果没有历史数据，可能无法执行
SELECT  ds
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds BETWEEN TO_CHAR(DATEADD(TO_DATE('${bizdate}', 'yyyymmdd'), -6, 'dd'), 'yyyymmdd')
                AND '${bizdate}'
GROUP BY ds
ORDER BY ds
;

-- 8. 查看租户维度的MCP使用TOP10
SELECT  tenant_code
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
GROUP BY tenant_code
ORDER BY mcp_count DESC
LIMIT 10
;

-- 9. 查看基础统计数据
SELECT  COUNT(DISTINCT agent_code) AS total_agent_count
        ,COUNT(DISTINCT tenant_code) AS total_tenant_count
        ,COUNT(DISTINCT creator_id) AS total_creator_count
        ,SUM(mcp_count) AS total_mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
;

-- 10. 查看最近创建的带MCP的智能体
SELECT  agent_code
        ,agent_name
        ,creator_name
        ,tenant_code
        ,gmt_create
        ,mcp_count
        ,subject_id
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
AND     mcp_count > 0
ORDER BY gmt_create DESC
LIMIT 20
;

-- 11. 统计MCP服务地址分布
SELECT  subject_id
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,SUM(mcp_count) AS mcp_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
AND     subject_id IS NOT NULL
GROUP BY subject_id
ORDER BY agent_count DESC
LIMIT 20
;

-- 12. 分析MCP服务地址的域名分布
SELECT  REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1) AS domain
        ,COUNT(DISTINCT agent_code) AS agent_count
        ,COUNT(DISTINCT subject_id) AS endpoint_count
FROM    mcp_usage_stats
WHERE   ds = '${bizdate}'
AND     subject_id IS NOT NULL
GROUP BY REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1)
ORDER BY agent_count DESC
LIMIT 20
;
