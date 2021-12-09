---
title: vue项目实例学习
---

# Vue

* cli 搭建项目
* vue ui可视化

* token工作原理



* main.js: 入口文件
* APP.vue: 根组件



## 表单

通过element-ui组件



* 数据绑定 

  1. el-form: `:model="form"`

  2. el-form-item: `v-model="form.name"`

  3. `form`在script中定义表单



* 表单验证

  1. el-form : `:rules="rules"`

  2.  rules 在script中定义
  3. el-form-item: prop指定不同验证规则



* 表单重置
  1. 在el-form 中使用`ref=""`拿到表单实例对象
  2. 调用表单实例的方法 resetFields 来重置表单
     1. 通过this可以获得该组件实例对象



* 对整个表单进行预验证
  1. 调用表单实例的方法 validate



## 请求

配置使用 axios 发送http请求



* 根据预验证的结果来决定是否发起 POST 请求：
  * 带表单数据的POST请求
* 需要使用异步`async` 来获取正确的后端返回的数据
  * 使用`{data:res}=await this.$http.post`来析构出data数据
* ==注意==：需要使用`stringify`把数据从json格式转成字符串 [qs.stringify()、qs.parse()的使用 - 简书 (jianshu.com)](https://www.jianshu.com/p/7e64878fb210)
* ==注意：==：`v-model`默认获得是字符串
  * 输入数字的话 使用`v-model.number`获得数字



## 弹框提示

element-ui: Message消息提示



## 登录成功之后

1. 登录之后，后端分发给我们的 token，保存到客户端的 sessionStorage中
   1. 项目中除了登录之外的其他API接口，必须在登录之后才能访问
   2. token 只应在当前网站打开期间生效，所以要将token保存在 sessionStorage 中
2. 通过编程式导航，跳转到后台主页，路由地址是 /home



* 编程式导航到其他主页：`this.$router.push('/')`



## 路由导航守卫控制访问权限

`router.beforeEach((to, from, next) => )` 回调函数：

* to: 将要访问的路径
* from：从哪个路径跳转来
* next：表示放行
  * `next()` 放行
  * `next('/login')` :强制跳转



## 编写退出

* 清除session



# 主页编写

* 注册ele组件el-container, 
* ==组件名：== 类名选择器



## 子路由

使用 e-menu自带的子路由实现组件跳转



## 面包屑导航

element ui



## 卡片视图区域

element ui



## 获取列表数据

* 使用created 生命周期函数调用获取列表数据函数

## 渲染列表数据

element-ui table：自动遍历list并渲染

* scope.row很好用



## 作用域插槽



## 添加用户

* 对话框 elem
* 表单



## 修改用户

* 通过作用于插槽：`slot-scope='scope'`
  * scope.row获得该行数据



## 删除用户



# Git

**创建新工作分支**

* git status
* git checkout -b login
* git branch

**合并、上传分支**

* git add : 添加到暂存区
* git commit -m "完成登录功能" : 提交到本地仓库
* git checkout master: 切换到master分支
* git merge login :合并到mster
* git push : 将master分支推送到远程仓库
* git push -u origin login: 将本地分支推送到远程仓库，并命名为login

# 遇到的问题：

* 烦人的 `eslint` ?
  * 编写`.prettierrc` 来格式化为符合 eslint 语法的形式
  * 修改`eslintrc.js`

* > Couldn’t parse bundle asset 文件路径\dist\js\chunk-vendors.js".
  > Analyzer will use module sizes from stats file.

  * 装less 和 less-loader依赖
  * less-loader 版本过高 [vue安装less-loader和less依赖报错问题 - 黛黛318 - 博客园 (cnblogs.com)](https://www.cnblogs.com/daidai318/p/14669320.html)

* vue ui / Vue前端项目 / Django 后端项目
  * 端口冲突
  * Django:  http://127.0.0.1:8000
  * vue ui: http://127.0.0.1:4040
  * Vue: http://127.0.0.1:4000
  
* 前端和后端 跨域问题：只需要配置一下后端
  * [Django+Vue跨域配置与经验 - kingkongk - 博客园 (cnblogs.com)](https://www.cnblogs.com/kingkongk/p/12982219.html)
  
* login 页面传递参数[关于Vue中两个vue页面传数据 - chalkbox - 博客园 (cnblogs.com)](https://www.cnblogs.com/chalkbox/p/12549437.html)



# Vue和Django项目整合

* 解决session为 null



# 美化

* elementui图片走马灯
* [(84条消息) vue+elementUI框架 实现走马灯图片高度自适应_weixin_45115895的博客-CSDN博客_elementui 走马灯高度](https://blog.csdn.net/weixin_45115895/article/details/108792741?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2~default~OPENSEARCH~default-1.highlightwordscore&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2~default~OPENSEARCH~default-1.highlightwordscore)
* 加过滤器
* 加分页：el-pagination
