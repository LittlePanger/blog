# 表结构

## index表

url -- 判断是哪个页面

title -- 网页的title标签

header_title -- header标题

header_subtitle  -- header副标题

header_img  -- header图片

is_show是否展示





## navigation 表

href -- 链接

title -- 标题

is_show是否展示



## footer 表

href -- 链接

fa -- 图标

is_show是否展示



## Article表

title-- 标题

subtitle-- 副标题

file-- 存md路径

url--链接

date-- 日期,最后修改时间

name--作者名

name_href--作者链接

content_img--文章封面

is_show是否展示





## comment表

username -- 用户名

content -- 内容

date -- 时间

ua -- 浏览器信息

is_show是否展示

可以加一个url,然后输入框多一个,如果填写了个人门户就添加个a标签





## about表

file--md的地址

about页面使用md直接生成,然后覆盖





## 待完成功能
- blog
  - 文章分类
  - 留言点赞
  - 评论树
  - **工具页面**
  - ~~加载进度条~~
  - ~~ai审核留言~~
  - 会员(头像)
- cms
  - 使用rsa加密登录
  - 限制访问次数
  - 表格,点击添加多一行,然后提交
  - 访问日志分析







