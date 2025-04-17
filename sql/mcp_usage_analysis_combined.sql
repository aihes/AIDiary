--@exclude_input=ai_business_tech.aidc_managed_agent_new,ai_business_tech.aidc_agent_relation
--odps sql 
--********************************************************************--
--author:aihe
--create time:2024-10-15 16:16:23
--********************************************************************--

-- 使用WITH语法合并多个维度的MCP使用统计数据
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
,time_dimension AS 
(
    -- 按时间维度统计
    SELECT  TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd') AS create_date
            ,COUNT(DISTINCT agent_code) AS new_agent_count
            ,COUNT(DISTINCT subject_id) AS new_mcp_endpoint_count
            ,SUM(mcp_count) AS new_mcp_count
    FROM    mcp_agent_stats
    GROUP BY TO_CHAR(TO_DATE(gmt_create, 'yyyy-mm-dd hh:mi:ss'), 'yyyy-mm-dd')
)
,creator_dimension AS 
(
    -- 按创建者统计
    SELECT  creator_name
            ,creator_id
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    GROUP BY creator_name
             ,creator_id
)
,env_dimension AS 
(
    -- 按环境统计
    SELECT  env
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    GROUP BY env
)
,status_dimension AS 
(
    -- 按部署状态统计
    SELECT  deployed_status
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    GROUP BY deployed_status
)
,tenant_dimension AS 
(
    -- 按租户统计
    SELECT  tenant_code
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,COUNT(DISTINCT subject_id) AS mcp_endpoint_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    GROUP BY tenant_code
)
,mcp_count_distribution AS 
(
    -- MCP数量分布
    SELECT  mcp_count_range
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
)
,mcp_endpoint_stats AS 
(
    -- MCP服务地址统计
    SELECT  subject_id
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    WHERE   subject_id IS NOT NULL
    GROUP BY subject_id
)
,mcp_domain_stats AS 
(
    -- MCP域名统计
    SELECT  REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1) AS domain
            ,COUNT(DISTINCT agent_code) AS agent_count
            ,COUNT(DISTINCT subject_id) AS endpoint_count
            ,SUM(mcp_count) AS mcp_count
    FROM    mcp_agent_stats
    WHERE   subject_id IS NOT NULL
    GROUP BY REGEXP_EXTRACT(subject_id, '(https?://[^/]+)', 1)
)
,recent_agents AS 
(
    -- 最近创建的智能体
    SELECT  agent_code
            ,agent_name
            ,creator_name
            ,tenant_code
            ,gmt_create
            ,subject_id
            ,mcp_count
    FROM    mcp_agent_stats
    WHERE   mcp_count > 0
)
,overall_stats AS 
(
    -- 总体统计
    SELECT  COUNT(DISTINCT agent_code) AS total_agent_count
            ,COUNT(DISTINCT tenant_code) AS total_tenant_count
            ,COUNT(DISTINCT creator_id) AS total_creator_count
            ,COUNT(DISTINCT subject_id) AS total_mcp_endpoint_count
            ,SUM(mcp_count) AS total_mcp_count
    FROM    mcp_agent_stats
)

-- 输出所有维度的统计结果
SELECT '1. 总体统计' AS analysis_type, 'MCP使用总体情况' AS analysis_detail
UNION ALL
SELECT '总体统计', CONCAT('总智能体数: ', CAST(total_agent_count AS STRING), 
                        ', 总租户数: ', CAST(total_tenant_count AS STRING), 
                        ', 总创建者数: ', CAST(total_creator_count AS STRING),
                        ', 总MCP端点数: ', CAST(total_mcp_endpoint_count AS STRING),
                        ', 总MCP关联数: ', CAST(total_mcp_count AS STRING))
FROM overall_stats
UNION ALL

SELECT '2. 时间维度统计' AS analysis_type, '按创建日期统计MCP使用趋势' AS analysis_detail
UNION ALL
SELECT create_date, CONCAT('新增智能体数: ', CAST(new_agent_count AS STRING), 
                          ', 新增MCP端点数: ', CAST(new_mcp_endpoint_count AS STRING), 
                          ', 新增MCP关联数: ', CAST(new_mcp_count AS STRING))
FROM time_dimension
ORDER BY create_date
UNION ALL

SELECT '3. 创建者TOP20' AS analysis_type, '按创建者统计MCP使用情况' AS analysis_detail
UNION ALL
SELECT CONCAT(creator_name, '(', creator_id, ')'), CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                                                         ', MCP端点数: ', CAST(mcp_endpoint_count AS STRING), 
                                                         ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM creator_dimension
ORDER BY mcp_count DESC
LIMIT 20
UNION ALL

SELECT '4. 环境统计' AS analysis_type, '按环境统计MCP使用情况' AS analysis_detail
UNION ALL
SELECT env, CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                  ', MCP端点数: ', CAST(mcp_endpoint_count AS STRING), 
                  ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM env_dimension
UNION ALL

SELECT '5. 部署状态统计' AS analysis_type, '按部署状态统计MCP使用情况' AS analysis_detail
UNION ALL
SELECT CAST(deployed_status AS STRING), CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                                             ', MCP端点数: ', CAST(mcp_endpoint_count AS STRING), 
                                             ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM status_dimension
UNION ALL

SELECT '6. 租户TOP10' AS analysis_type, '按租户统计MCP使用情况' AS analysis_detail
UNION ALL
SELECT tenant_code, CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                          ', MCP端点数: ', CAST(mcp_endpoint_count AS STRING), 
                          ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM tenant_dimension
ORDER BY mcp_count DESC
LIMIT 10
UNION ALL

SELECT '7. MCP数量分布' AS analysis_type, '统计每个智能体关联的MCP数量分布' AS analysis_detail
UNION ALL
SELECT mcp_count_range, CONCAT('智能体数: ', CAST(agent_count AS STRING))
FROM mcp_count_distribution
ORDER BY CASE
            WHEN mcp_count_range = '0' THEN 1
            WHEN mcp_count_range = '1' THEN 2
            WHEN mcp_count_range = '2-5' THEN 3
            WHEN mcp_count_range = '6-10' THEN 4
            ELSE 5
         END
UNION ALL

SELECT '8. MCP服务地址TOP20' AS analysis_type, '统计MCP服务地址分布' AS analysis_detail
UNION ALL
SELECT subject_id, CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                         ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM mcp_endpoint_stats
ORDER BY agent_count DESC
LIMIT 20
UNION ALL

SELECT '9. MCP域名TOP20' AS analysis_type, '分析MCP服务地址的域名分布' AS analysis_detail
UNION ALL
SELECT domain, CONCAT('智能体数: ', CAST(agent_count AS STRING), 
                     ', 端点数: ', CAST(endpoint_count AS STRING), 
                     ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM mcp_domain_stats
ORDER BY agent_count DESC
LIMIT 20
UNION ALL

SELECT '10. 最近创建的带MCP的智能体TOP20' AS analysis_type, '查看最近创建的带MCP的智能体' AS analysis_detail
UNION ALL
SELECT CONCAT(agent_name, '(', agent_code, ')'), CONCAT('创建者: ', creator_name, 
                                                       ', 租户: ', tenant_code, 
                                                       ', 创建时间: ', gmt_create, 
                                                       ', MCP服务地址: ', subject_id, 
                                                       ', MCP关联数: ', CAST(mcp_count AS STRING))
FROM recent_agents
ORDER BY gmt_create DESC
LIMIT 20
;

-- 如果需要单独查看某个维度的详细数据，可以使用以下查询

-- 查看基础数据
SELECT * FROM mcp_base_data LIMIT 100;

-- 查看按智能体统计的MCP使用情况
SELECT * FROM mcp_agent_stats LIMIT 100;

-- 查看时间维度统计
SELECT * FROM time_dimension ORDER BY create_date;

-- 查看创建者维度统计
SELECT * FROM creator_dimension ORDER BY mcp_count DESC LIMIT 100;

-- 查看环境维度统计
SELECT * FROM env_dimension;

-- 查看部署状态维度统计
SELECT * FROM status_dimension;

-- 查看租户维度统计
SELECT * FROM tenant_dimension ORDER BY mcp_count DESC LIMIT 100;

-- 查看MCP数量分布
SELECT * FROM mcp_count_distribution
ORDER BY CASE
            WHEN mcp_count_range = '0' THEN 1
            WHEN mcp_count_range = '1' THEN 2
            WHEN mcp_count_range = '2-5' THEN 3
            WHEN mcp_count_range = '6-10' THEN 4
            ELSE 5
         END;

-- 查看MCP服务地址统计
SELECT * FROM mcp_endpoint_stats ORDER BY agent_count DESC LIMIT 100;

-- 查看MCP域名统计
SELECT * FROM mcp_domain_stats ORDER BY agent_count DESC LIMIT 100;

-- 查看最近创建的带MCP的智能体
SELECT * FROM recent_agents ORDER BY gmt_create DESC LIMIT 100;

-- 查看总体统计
SELECT * FROM overall_stats;
