# DScope

中山大学 2024 年分布式系统大作业。

DScope = **D**istributed **Scope**，分布式系统概念可视化系统。

目前支持模拟与可视化的分布式概念有:

- 逻辑时钟 (logical-clock)
- 向量时钟 (vector-clock)

## 1. 环境配置

### 1.1 前端

```bash
cd dscope/
docker compose up -d
```

这会起一个叫做 `dscope_shiviz` 的容器，使用 Ningx 容器运行着 DScope 的前端服务。

### 1.2 模拟器

```bash
pip install -r requirements.txt
pip install -e . --use-pep517
dscope --version
```

预期得到输出 `DScope <version>`。

## 2. 超参数设置

### 2.1 前端

前端默认监听 `localhost:4564`，可以在 `.env` 中修改 `SHIVIZ_PORT`。

### 2.2 模拟器

目前支持模拟的分布式场景有:

- 逻辑时钟 (logical-clock)
- 向量时钟 (vector-clock)

模拟器的超参数可以在 `dscope/settings.py` 中修改。

## 3. 案例演示

### 3.1 逻辑向量

首先启动前端，确保 `localhost:4564` 可以访问。

运行模拟器，生成逻辑时钟的日志，此日志默认保存在 `log/logical-clock.log`。

```bash
dscope --simulator logical-clock
```

此时访问前端，在 `Example Logs` 中选择 `Logical Clock`，可以发现日志内容**动态**地渲染在页面上，点击 `Visualize` 按钮即可看到逻辑时钟的可视化演示。

<div style="display: flex;">
  <img src="assets/logical_clock_1.jpg" alt="logical_clock_1.jpg" width="45%" />
  <img src="assets/logical_clock_2.jpg" alt="logical_clock_2.jpg" width="45%" />
</div>

### 3.2 时钟向量

首先启动前端，确保 `localhost:4564` 可以访问。

运行模拟器，生成逻辑时钟的日志，此日志默认保存在 `log/vector-clock.log`。

```bash
dscope --simulator logical-clock
```

此时访问前端，在 `Example Logs` 中选择 `Vector Clock`，可以发现日志内容**动态**地渲染在页面上，点击 `Visualize` 按钮即可看到逻辑时钟的可视化演示。

<div style="display: flex;">
  <img src="assets/vector_clock_1.jpg" alt="vector_clock_1.jpg" width="45%" />
  <img src="assets/vector_clock_2.jpg" alt="vector_clock_2.jpg" width="45%" />
</div>