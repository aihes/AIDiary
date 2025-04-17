# SQL脚本

本目录包含各种SQL脚本，主要用于数据分析和报表生成。

## 文件列表

- [mcp_usage_analysis.sql](./mcp_usage_analysis.sql) - MCP使用分析的基础SQL脚本
- [mcp_usage_analysis_combined.sql](./mcp_usage_analysis_combined.sql) - 使用WITH语法合并多个维度的MCP使用统计数据
- [mcp_usage_analysis_report.sql](./mcp_usage_analysis_report.sql) - 为报表生成优化的MCP使用分析SQL脚本

## 主要内容

这些SQL脚本主要用于分析MCP（模型上下文协议）的使用情况，从不同维度进行统计和分析：

1. **基础数据统计**
   - 关联智能体和MCP数据
   - 按智能体维度统计MCP关联数量

2. **多维度分析**
   - 时间维度：按创建日期统计MCP创建趋势
   - 创建者维度：统计每个创建者的MCP使用情况
   - 环境维度：按环境统计MCP使用情况
   - 部署状态维度：按部署状态统计MCP使用情况
   - 租户维度：统计每个租户的MCP使用情况

3. **分布分析**
   - 统计每个智能体关联的MCP数量分布
   - MCP服务地址分布
   - MCP域名分布

4. **趋势分析**
   - 按日、周、月统计MCP使用趋势

5. **TOP分析**
   - 查看租户维度的MCP使用TOP10
   - 查看创建者维度的MCP使用TOP20
   - 查看最近创建的带MCP的智能体
