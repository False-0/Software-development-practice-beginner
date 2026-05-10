# API 接口文档

## 概述

本文档详细描述了医学刷题系统的API接口，包括用户管理、题目浏览、收藏和历史记录等功能模块。

## 基础URL

```
http://localhost:8000
```

## 认证方式

大部分接口需要认证，认证通过在请求头中添加 `Authorization` 字段实现：

```
Authorization: token值
```

## 响应格式

所有接口返回JSON格式数据，通用响应结构如下：

```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```

## 接口详情

### 用户管理模块

#### 1. 用户注册

- **接口地址**: `POST /api/user/register`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

- **请求示例**:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "注册成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "bio": "这个人很懒，什么都没留下",
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg"
    }
  }
}
```

#### 2. 用户登录

- **接口地址**: `POST /api/user/login`
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| username | string | 是 | 用户名 |
| password | string | 是 | 密码 |

- **请求示例**:

```json
{
  "username": "example_user",
  "password": "example_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "登录成功",
  "data": {
    "token": "用户访问令牌",
    "userInfo": {
      "id": 1,
      "username": "example_user",
      "nickname": null,
      "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
      "bio": "这个人很懒，什么都没留下"
    }
  }
}
```

#### 3. 获取用户信息

- **接口地址**: `GET /api/user/info`
- **请求头**: 需要认证
- **响应示例**:

```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "username": "example_user",
    "nickname": null,
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这个人很懒，什么都没留下"
  }
}
```

#### 4. 更新用户信息

- **接口地址**: `PUT /api/user/update`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| nickname | string | 否 | 昵称 |
| avatar | string | 否 | 头像URL |
| gender | string | 否 | 性别 |
| bio | string | 否 | 个人简介 |
| phone | string | 否 | 手机号 |

- **请求示例**:

```json
{
  "bio": "这是我的个人简介"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "更新成功",
  "data": {
    "id": 1,
    "username": "example_user",
    "nickname": null,
    "avatar": "https://fastly.jsdelivr.net/npm/@vant/assets/cat.jpeg",
    "gender": "unknown",
    "bio": "这是我的个人简介"
  }
}
```

#### 5. 修改用户密码

- **接口地址**: `PUT /api/user/password`
- **请求头**: 需要认证
- **请求参数**:

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| oldPassword | string | 是 | 当前密码 |
| newPassword | string | 是 | 新密码 |

- **请求示例**:

```json
{
  "oldPassword": "current_password",
  "newPassword": "new_password"
}
```

- **响应示例**:

```json
{
  "code": 200,
  "message": "密码修改成功",
  "data": null
}
```

### 题目浏览模块

#### 1. 获取所有科目列表
- **接口地址**: GET /api/question/subjects
- **请求参数**: (Query 参数)

|参数名|类型|必填|说明|
|skip	|int	|否	|跳过条数|默认 0|
|limit|	int	|否	|每页条数|默认 100|

- **请求示例**:
plaintext
GET http://localhost:8000/api/question/subjects?skip=0&limit=10

- **响应示例**:
```json
{
  "code": 200,
  "message": "获取科目列表成功",
  "data": [
    {
      "id": 1,
      "name": "内科",
      "created_at": "2025-01-01T12:00:00",
      "updated_at": "2025-01-01T12:00:00"
    },
    {
      "id": 2,
      "name": "外科",
      "created_at": "2025-01-01T12:00:00",
      "updated_at": "2025-01-01T12:00:00"
    }
  ]
}
```

#### 2. 根据科目 ID 获取章节列表

- **接口地址**: GET /api/question/chapters
- **请求参数**: (Query 参数)
|参数名|	类型	|必填	|说明|
|subjectId	|int	|是	|科目 ID|
|page	|int	|否	|页码|默认 1|
|pageSize	|int	|否	|每页条数,默认 100，最大 100|

- **请求示例**:
plaintext
GET http://localhost:8000/api/question/chapters?subjectId=1&page=1&pageSize=10

- **响应示例**:
```json
{
  "code": 200,
  "message": "获取章节列表成功",
  "data": {
    "list": [
      {
        "id": 1,
        "subject_id": 1,
        "name": "呼吸系统疾病",
        "created_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T12:00:00"
      },
      {
        "id": 2,
        "subject_id": 1,
        "name": "循环系统疾病",
        "created_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T12:00:00"
      }
    ],
    "total": 20,
    "hasMore": true
  }
}
```

#### 3. 根据章节 ID 获取题目列表
- **接口地址**: GET /api/question/list
- **请求参数**: (Query 参数)
|参数名	|类型	|必填	|说明|
|chapterId|	int	|是	|章节 ID|
|page	|int	|否	|页码，默认 1|
|pageSize	|int	|否	|每页条数，默认 10，最大 100|

- **请求示例**:
plaintext
GET http://localhost:8000/api/question/list?chapterId=1&page=1&pageSize=5

- **响应示例**:
```json
{
  "code": 200,
  "message": "获取题目列表成功",
  "data": {
    "list": [
      {
        "id": 1,
        "chapter_id": 1,
        "title": "肺炎链球菌肺炎的典型症状是？",
        "option_a": "发热伴寒战",
        "option_b": "咳粉红色泡沫痰",
        "option_c": "持续胸痛",
        "option_d": "进行性呼吸困难",
        "answer": "A",
        "created_at": "2025-01-01T12:00:00",
        "updated_at": "2025-01-01T12:00:00"
      }
    ],
    "total": 50,
    "hasMore": true
  }
}
```

#### 4. 获取单个题目详情
- **接口地址**: GET /api/question/detail
- **请求参数**: (Query 参数)
|参数名|	类型|	必填	|说明|
|id	|int	|是	|题目 ID|
- **请求示例**:
plaintext
GET http://localhost:8000/api/question/detail?id=1
- **响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "id": 1,
    "title": "肺炎链球菌肺炎的典型症状是？",
    "optionA": "发热伴寒战",
    "optionB": "咳粉红色泡沫痰",
    "optionC": "持续胸痛",
    "optionD": "进行性呼吸困难",
    "answer": "A",
    "chapterId": 1,
    "createdAt": "2025-01-01T12:00:00"
  }
}
```
#### 5. 用户提交答题结果
- **接口地址**: POST /api/question/submit
- **认证要求**: 需要在请求头携带 Authorization: token值
- **请求参数**: (Query 参数)
|参数名	|类型|	必填|	说明|
|question_id|	int|	是	|题目 ID|
|answer	|string	|是	|用户答案（A/B/C/D）|
- **请求示例**:
plaintext
POST http://localhost:8000/api/question/submit?question_id=1&answer=A
Headers:
Authorization: your_token_here
- **响应示例**:
```json
{
  "code": 200,
  "message": "提交答案成功",
  "data": {
    "status": "success",
    "is_correct": true,
    "correct_answer": "A"
  }
}
```

### 做对题目模块

#### 1. 获取做对题目列表
- **接口地址**: GET /api/correct/list
- **请求头**: 需要认证
- **请求参数** (Query 参数):
|参数名|	类型|	必填|	说明|
|page	|int	|否	|页码，默认 1|
|pageSize	|int	|否|	每页条数，默认 10，最大 100|
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取做对题目成功",
  "data": {
    "list": [
      {
        "correctId": 1,
        "createdAt": "2025-01-01T12:00:00",
        "id": 1,
        "title": "肺炎链球菌肺炎的典型症状是？",
        "optionA": "发热伴寒战",
        "optionB": "咳粉红色泡沫痰",
        "optionC": "持续胸痛",
        "optionD": "进行性呼吸困难",
        "answer": "A",
        "chapterId": 1
      }
    ],
    "total": 20,
    "hasMore": true
  }
}
```

#### 2. 删除单条做对记录
- **接口地址**: DELETE /api/correct/delete/{questionId}
- **请求头**: 需要认证
- **响应示例**:
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```

#### 3. 清空所有做对记录
- **接口地址**: DELETE /api/correct/clear
- **请求头**: 需要认证
- **响应示例**:
```json
{
  "code": 200,
  "message": "清空成功",
  "data": null
}
```

### 收藏题目模块

#### 1. 检查题目收藏状态
- **接口地址**: GET /api/favorite/check
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**（Query 参数）:
|参数名|	类型	|必填|	说明|
|question_id	|int	|是	|题目 ID|
- **请求示例**:
plaintext
GET http://localhost:8000/api/favorite/check?question_id=1001
- **响应示例**:
```json
{
  "code": 200,
  "message": "检查收藏状态成功",
  "data": {
    "isFavorite": true
  }
}
```

#### 2. 添加题目收藏
- **接口地址**: POST /api/favorite/add
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**:
|参数名|	类型	|必填	|说明|
|questionId	|int	|是	|题目 ID（注：参数别名映射，实际接收 question_id）|
- **请求示例**:
```json
{
  "questionId": 1001
}
```
- **响应示例**:
```json
{
  "code": 200,
  "message": "收藏成功",
  "data": null
}
```

#### 3. 取消题目收藏
- **接口地址**: DELETE /api/favorite/cancel/{question_id}
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**:
|参数名|	类型|	必填	|说明|
|question_id|	int|	是	|题目 ID|
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/favorite/cancel/1001
- **响应示例**:
```json
{
  "code": 200,
  "message": "取消收藏成功",
  "data": null
}
```
- **响应示例**:
```json
{
  "code": 404,
  "message": "收藏不存在",
  "data": null
}
```

#### 4. 获取收藏列表（分页）
- **接口地址**: GET /api/favorite/list
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**:
|参数名|	类型|	必填|	说明|
|page	int	|否|	页码，默认 1，最小值 1|
|pageSize	|int	|否	|每页条数，默认 10，最小值 1，最大值 100|
- **请求示例**:
plaintext
GET http://localhost:8000/api/favorite/list?page=1&pageSize=10
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取收藏列表成功",
  "data": {
    "list": [
      {
        "id": 1001,
        "title": "医学基础选择题",
        "content": "以下不属于人体八大系统的是？",
        "type": "single_choice",
        "difficulty": "easy",
        "favoriteId": 1,
        "favoriteTime": "2024-05-20T12:30:00"
      }
    ],
    "total": 1,
    "hasMore": false
  }
}
```

#### 5. 清空全部收藏
- **接口地址**: DELETE /api/favorite/clear
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**: 无
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/favorite/clear
- **响应示例**:
```json
{
  "code": 200,
  "message": "清空收藏成功",
  "data": null
}
```

- **基础 URL**
plaintext
http://localhost:8000
- **认证方式**
部分接口（发布帖子、发布评论、删除帖子 / 评论）需要认证，认证通过在请求头中添加 Authorization 字段实现：
plaintext
Authorization: token值
- **响应格式**
所有接口返回 JSON 格式数据，通用响应结构如下：
```json
{
  "code": 200,
  "message": "success",
  "data": {}
}
```


### 论坛帖子模块

#### 1. 获取帖子列表（分页）
- **接口地址**: GET /api/forum/list
- **请求参数**: 
|参数名|	类型|	必填	|说明|
|page	|int	|否	|页码，默认值 1，最小值 1|
|pageSize|	int	|否	|每页条数，默认值 10，取值范围 1-100|
- **请求示例**:
plaintext
GET http://localhost:8000/api/forum/list?page=1&pageSize=10
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取帖子列表成功",
  "data": {
    "list": [
      {
        "postId": 1,
        "title": "论坛帖子标题示例",
        "viewCount": 20,
        "createdAt": "2024-01-01T12:00:00"
      }
    ],
    "total": 50,
    "hasMore": true
  }
}
```

#### 2. 获取热门帖子 TOP10
- **接口地址**: GET /api/forum/hot
- **请求参数**: 无
- **请求示例**:
plaintext
GET http://localhost:8000/api/forum/hot
- **响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "list": [
      {
        "postId": 1,
        "title": "热门帖子标题",
        "viewCount": 100
      },
      {
        "postId": 2,
        "title": "第二热门帖子",
        "viewCount": 90
      }
    ]
  }
}
```

#### 3. 发布帖子
- **接口地址**: POST /api/forum/create
- **请求头**: 需要认证
- **请求参数**: 
|参数名|	类型	|必填|	说明|
|title	|string|	是|	帖子标题|
|content|	string	|是	|帖子内容|
- **请求示例**:
```json
{
  "title": "我的新帖子",
  "content": "这是帖子的详细内容..."
}
```
- **响应示例**:
```json
{
  "code": 200,
  "message": "发布帖子成功",
  "data": null
}
```

#### 4. 获取帖子详情（含评论）
- **接口地址**: GET /api/forum/detail/{post_id}
- **请求参数**: 
|参数名	|类型	|必填|	说明|
|post_id	|int|	是|	帖子 ID|
- **请求示例**:
plaintext
GET http://localhost:8000/api/forum/detail/1
- **响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "postId": 1,
    "title": "帖子标题",
    "content": "帖子详细内容",
    "viewCount": 21,
    "createdAt": "2024-01-01T12:00:00",
    "comments": [
      {
        "commentId": 1,
        "username": "test_user",
        "content": "这是一条评论",
        "createdAt": "2024-01-01T13:00:00"
      }
    ]
  }
}
```

#### 5. 删除自己的帖子
- **接口地址**: DELETE /api/forum/post/{post_id}
- **请求头**: 需要认证
- **请求参数**: 
|参数名|	类型|	必填|	说明|
|post_id	|int	|是|	帖子 ID|
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/forum/post/1
- **响应示例**:
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```
- **异常响应示例（删除他人帖子）**:
```json
{
  "code": 403,
  "message": "只能删除自己的帖子",
  "data": null
}
```

### 论坛评论模块

#### 1. 发布评论
- **接口地址**: POST /api/forum/comment
- **请求头**: 需要认证
- **请求参数**: 
|参数名|	类型	|必填|	说明|
|postId|	int|	是|	所属帖子 ID|
|content|	string|	是|	评论内容|
- **请求示例**:
```json
{
  "postId": 1,
  "content": "这是我对帖子的评论内容"
}
```
- **响应示例**:
```json
{
  "code": 200,
  "message": "评论成功",
  "data": null
}
```

#### 2. 删除自己的评论
- **接口地址**: DELETE /api/forum/comment/{comment_id}
- **请求头**: 需要认证
- **请求参数**:
|参数名	|类型	|必填	|说明|
|comment_id|	int	|是	|评论 ID|
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/forum/comment/1
- **响应示例**:
```json
{
  "code": 200,
  "message": "删除成功",
  "data": null
}
```
- **异常响应示例（删除他人评论）**:
```json
{
  "code": 403,
  "message": "只能删除自己的评论",
  "data": null
}
```

### 错题管理模块

#### 1. 获取错题列表
- **接口地址**: GET /api/error/list
- **请求头**: 需要认证（Authorization: token值）
- **请求参数**:
|参数名	|类型|	必填	|说明|
|page	|int|	否|	页码，默认 1，最小值 1|
|pageSize	|int|	否|	每页条数，默认 10，最小值 1，最大值 100|
- **请求示例**:
plaintext
GET http://localhost:8000/api/error/list?page=1&pageSize=10
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取错题列表成功",
  "data": {
    "list": [
      {
        "id": 1,  // 题目ID
        "chapterId": 3,  // 章节ID（驼峰别名）
        "title": "医学常识题示例",  // 题目内容
        "optionA": "选项A内容",  // 选项A
        "optionB": "选项B内容",  // 选项B
        "optionC": "选项C内容",  // 选项C
        "optionD": "选项D内容",  // 选项D
        "answer": "A",  // 正确答案
        "errorId": 1,  // 错题记录ID
        "wrongCount": 3,  // 做错次数
        "createdAt": "2024-05-20T14:30:00"  // 错题首次添加时间
      }
    ],
    "total": 20,  // 错题总数
    "hasMore": true  // 是否有下一页
  }
}
```

#### 2. 删除单条错题
- **接口地址**: DELETE /api/error/delete/{question_id}
- **请求头**: 需要认证（Authorization: token值）
- **路径参数**:
|参数名	|类型	|必填	|说明|
|question_id	|int|	是	|要删除的题目 ID|
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/error/delete/1
- **成功响应**:
```json
{
  "code": 200,
  "message": "删除错题成功",
  "data": null
}
```
- **异常响应（错题不存在）**:
```json
{
  "code": 404,
  "message": "错题不存在",
  "data": null
}
```

#### 3. 清空所有错题
- **接口地址**: DELETE /api/error/clear
- **请求头**: 需要认证（Authorization: token值）
- **请求示例**:
plaintext
DELETE http://localhost:8000/api/error/clear
- **响应示例**:
```json
{
  "code": 200,
  "message": "清空错题本成功",
  "data": null
}
```

#### 4. 获取错题统计信息
- **接口地址**: GET /api/error/statistics
- **请求头**: 需要认证（Authorization: token值）
- **响应示例**:
```json
{
  "code": 200,
  "message": "查询成功",
  "data": {
    "totalErrorCount": 50,  // 总错题数
    "todayErrorCount": 5,  // 今日新增错题数
    "topChapterId": 3,  // 今日错题最多的章节ID
    "topChapterNum": 3  // 今日该章节错题数
  }
}
```

#### 5. 获取章节错题分布（折线图专用）
- **接口地址**: GET /api/error/chapter-distribution
- **请求头**: 需要认证（Authorization: token值）
- **响应示例**:
```json
{
  "code": 200,
  "message": "获取章节错题分布成功",
  "data": {
    "list": [
      {
        "chapterName": "第一章 基础医学",
        "count": 10
      },
      {
        "chapterName": "第二章 临床医学",
        "count": 15
      }
    ]
  }
}
```

### 刷题排行榜模块

#### 1. 获取排行榜信息
- **接口地址**: GET /api/rank/info
- **请求头**: 需要认证（Authorization: token值）
- **接口描述**: 获取当前用户的刷题排名、个人刷题统计信息，以及全站刷题量前三的用户信息
- **请求参数**: 无
- **响应示例**:
```json
{
  "code": 200,
  "message": "success",
  "data": {
    "myRank": 5,
    "totalDone": 120,
    "totalCorrect": 98,
    "correctRate": 81.67,
    "top3": [
      {
        "username": "top_user1",
        "totalDone": 500
      },
      {
        "username": "top_user2",
        "totalDone": 450
      },
      {
        "username": "top_user3",
        "totalDone": 400
      }
    ]
  }
}
```
- **响应参数说明**:
| 参数名 | 类型 | 说明 |
|--------|------|------|
| myRank | int | 当前用户的刷题排名（无数据时返回 9999） |
| totalDone | int | 当前用户总做题数 |
| totalCorrect | int | 当前用户总做对题数 |
| correctRate | float | 当前用户做题正确率（保留 2 位小数） |
| top3 | array | 刷题量前三的用户列表 |
| top3 [].username | string | 前三名用户的用户名 |
| top3 [].totalDone | int | 前三名用户的总做题数 |
