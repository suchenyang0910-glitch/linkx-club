# linkx.club 部署指南

本文档说明如何将 linkx.club 项目部署到服务器环境。

## 环境要求

- **Node.js**: v14.0 或更高版本
- **OS**: Linux (推荐), Windows, 或 macOS

## 1. 准备工作

1. **克隆代码**:
   ```bash
   git clone <repository-url>
   cd linkx-club-new
   ```

2. **安装依赖**:
   ```bash
   npm install
   ```

3. **配置环境变量**:
   在项目根目录创建 `.env` 文件或设置系统环境变量：
   ```bash
   ARTICLE_API_KEY=your_secret_key_here
   ```

## 2. 启动服务

### 开发模式 (直接运行)
```bash
node article-server.js
```
服务将运行在 `http://0.0.0.0:3034`。

### 生产模式 (使用 PM2 推荐)
为了确保服务崩溃后能自动重启，建议使用 PM2：

1. **安装 PM2**:
   ```bash
   npm install pm2 -g
   ```

2. **启动应用**:
   ```bash
   pm2 start article-server.js --name "linkx-portal"
   ```

3. **查看状态**:
   ```bash
   pm2 status
   ```

## 3. 自动化测试 (部署前检查)

在部署或发布新版本前，务必运行 E2E 测试以确保页面渲染正常：

```bash
# 确保服务已启动
npm run test:e2e
```

## 4. 静态资源与反向代理 (Nginx)

建议使用 Nginx 作为反向代理，并开启 SSL (HTTPS)。

**Nginx 配置示例**:
```nginx
server {
    listen 80;
    server_name linkx.club;

    location / {
        proxy_pass http://127.0.0.1:3034;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

## 5. 数据持久化

所有文章数据存储在 `data/articles.json` 中。请确保该目录具有写权限。
**备份建议**: 定期冷备份 `data/articles.json` 文件。
