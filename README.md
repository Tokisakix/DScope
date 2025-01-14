# DScope

中山大学 2024 年分布式系统大作业。

DScope = **D**istributed **Scope**，分布式系统概念可视化系统。

## 环境配置

### 前端

```bash
cd dscope/
docker compose up -d
```

这会起一个叫做 `dscope_shiviz` 的容器，使用 Ningx 容器运行着 DScope 的前端服务。

默认入口是 `localhost:4564`，通过修改 `.env` 文件中的 `SHIVIZ_PORT` 修改前端映射端口。