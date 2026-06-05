# linkx.club 文章管理 API 文档

本文档介绍了 linkx.club 后端服务的 API 接口说明。

## 基础信息

- **Base URL**: `http://localhost:3034` (本地) 或生产环境域名
- **认证方式**: Bearer Token (仅写操作需要)
- **请求头**: `Authorization: Bearer <YOUR_API_KEY>`

---

## 1. 获取文章列表

获取所有已发布的文章摘要列表。

- **URL**: `/api/articles`
- **Method**: `GET`
- **Auth**: 不需要
- **响应示例**:
  ```json
  [
    {
      "id": 55,
      "title": "文章标题",
      "description": "摘要...",
      "country": "vn",
      "country_name": "越南",
      "tag": "供应链",
      "date": "2026-06-05",
      "cover": "/images/cover.jpg"
    }
  ]
  ```

## 2. 获取单篇文章详情

获取指定 ID 的文章完整内容。

- **URL**: `/api/article/:id`
- **Method**: `GET`
- **Auth**: 不需要
- **响应示例**:
  ```json
  {
    "id": 55,
    "title": "文章标题",
    "content_html": "<p>正文内容...</p>",
    "country": "vn",
    "tag": "供应链",
    ...
  }
  ```

## 3. 创建文章

新增一篇博文。

- **URL**: `/api/article`
- **Method**: `POST`
- **Auth**: **需要**
- **请求体示例**:
  ```json
  {
    "title": "新文章标题",
    "description": "摘要内容",
    "country": "th",
    "tag": "电动车",
    "content_html": "<p>正文...</p>",
    "cover": "https://...",
    "author": "linkx.club"
  }
  ```
- **成功响应**: `201 Created`
  ```json
  { "id": 67 }
  ```

## 4. 更新文章

修改现有文章的内容。

- **URL**: `/api/article/:id`
- **Method**: `PUT`
- **Auth**: **需要**
- **请求体示例**: (仅发送需要修改的字段)
  ```json
  {
    "title": "修改后的标题"
  }
  ```
- **成功响应**: `200 OK`
  ```json
  { "success": true }
  ```

## 5. 删除文章

永久删除指定文章。

- **URL**: `/api/article/:id`
- **Method**: `DELETE`
- **Auth**: **需要**
- **成功响应**: `200 OK`
  ```json
  { "success": true }
  ```

---

## 错误处理

- `401 Unauthorized`: 未提供有效的 API KEY。
- `404 Not Found`: 文章不存在。
- `400 Bad Request`: JSON 格式错误或缺少必要字段。
