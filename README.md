# WeChatServer
A weixin server framwork based flask

----


# 微信公众号服务器
基于flask搭建的微信公众号服务器


#### tools
tools 包用来定义一些工具类或方法
verify：该文件内是用来做认证的装饰器
- isServer：该装饰器用于认证消息是否来自微信服务器


## 工作进度总结
- 2019.6.20 10:20  完成了服务器的基本搭建，公众号与服务器可以正常的绑定与通信
- 2019.6.20 18:25  添加了后台系统模块和api接口模块，功能未明确

## 数据操作接口使用方式
当数据从微信服务器传送过来，服务器自身访问接口对数据进行存储（用户发送的明文消息等）

当发生用户行为，根据不同的用户行为调用不同的接口对数据进行存储。

后台系统可以调用数据接口访问用户交互数据

后台系统在对用户做出数据响应的行为后，追加用户交互数据

后台系统不存在主观意识上的数据修改行为

服务器调用的接口与后台系统调用的接口不能使用相同的接口，以免造成混淆

----



# API
### 1.自定义菜单管理

#### url

>  http://localhost:5000/api/v0.1/cgi-bin/menu

#### 1.1 创建自定义菜单

##### Request

- method： post
- body 
> json数据示例

```json
 {
     "button":[
     {    
          "type":"click",
          "name":"今日歌曲",
          "key":"V1001_TODAY_MUSIC"
      },
      {
           "name":"菜单",
           "sub_button":[
           {    
               "type":"view",
               "name":"搜索",
               "url":"http://www.soso.com/"
            },
            {
               "type":"click",
               "name":"赞一下我们",
               "key":"V1001_GOOD"
            }]
       }]
 }
```

- 参数说明

| 参数       | 必须                               | 说明                                                         |
| ---------- | ---------------------------------- | ------------------------------------------------------------ |
| button     | 是                                 | 一级菜单数组，个数应为1~3个                                  |
| sub_button | 否                                 | 二级菜单数组，个数应为1~5个                                  |
| type       | 是                                 | 菜单的响应动作类型，view表示网页类型，click表示点击类型，miniprogram表示小程序类型 |
| name       | 是                                 | 菜单标题，不超过16个字节，子菜单不超过60个字节               |
| key        | click等点击类型必须                | 菜单KEY值，用于消息接口推送，不超过128字节                   |
| url        | view、miniprogram类型必须          | 网页 链接，用户点击菜单可打开链接，不超过1024字节。 type为miniprogram时，不支持小程序的老版本客户端将打开本url。 |
| media_id   | media_id类型和view_limited类型必须 | 调用新增永久素材接口返回的合法media_id                       |
| appid      | miniprogram类型必须                | 小程序的appid（仅认证公众号可配置）                          |
| pagepath   | miniprogram类型必须                | 小程序的页面路径                                             |

##### Response

> 正确响应json数据

```json
{"errcode":0,"errmsg":"ok"}
```

> 错误响应json数据

```json
{"errcode":40018,"errmsg":"invalid button name size"}
```

#### 1.2 查询自定义菜单

##### Request

- method：get

##### Response

> 正确响应json数据

```json
{
    "menu": {
        "button": [
            {
                "type": "click", 
                "name": "今日歌曲", 
                "key": "V1001_TODAY_MUSIC", 
                "sub_button": [ ]
            }, 
            {
                "type": "click", 
                "name": "歌手简介", 
                "key": "V1001_TODAY_SINGER", 
                "sub_button": [ ]
            }, 
            {
                "name": "菜单", 
                "sub_button": [
                    {
                        "type": "view", 
                        "name": "搜索", 
                        "url": "http://www.soso.com/", 
                        "sub_button": [ ]
                    }, 
                    {
                        "type": "view", 
                        "name": "视频", 
                        "url": "http://v.qq.com/", 
                        "sub_button": [ ]
                    }, 
                    {
                        "type": "click", 
                        "name": "赞一下我们", 
                        "key": "V1001_GOOD", 
                        "sub_button": [ ]
                    }
                ]
            }
        ]
    }
}
```

#### 1.3 删除自定义菜单

##### Request

- method：delete

##### Response

> 正常示例

```json
{"errcode":0,"errmsg":"ok"}
```

### 2.标签管理

#### URL

> http://localhost:5000/api/v0.1/cgi-bin/tags

#### 2.1 创建标签

##### Request

- method：post
- form-data

| 参数 | 说明           |
| ---- | -------------- |
| name | 创建的标签名称 |

##### Response

> 正常示例

```json
{   "tag":{ "id":134, "name":"广东"   } }
```

#### 2.2 查询已建标签

##### Request

- method：get

##### Response

> 正常示例

```json
{   
"tags":[{       
    "id":1,       
    "name":"每天一罐可乐星人",      
    "count":0 //此标签下粉丝数
},
{   
    "id":2,   
    "name":"星标组",   
    "count":0
},
{   
    "id":127,  
    "name":"广东",  
    "count":5 
 }   
] }
```

#### 2.3 修改标签

##### Request

- method: put
- form-data

| 参数 | 说明     |
| ---- | -------- |
| id   | 标签ID   |
| name | 标签名称 |

##### Response

> 正确响应

```json
{   "errcode":0,   "errmsg":"ok" }
```

#### 2.4 删除标签

##### Request

- method： delete
- form-data

| 参数 | 说明   |
| ---- | ------ |
| id   | 标签ID |

##### Response

> 正确响应

```json
{   "errcode":0,   "errmsg":"ok" }
```

### 3.用户标签管理

#### URL

> http://localhost:5000/api/v0.1/cgi-bin/user/tags

#### 3.1 拉取指定标签下的用户列表/拉取指定用户下的标签列表

##### Request

- method： get
- params

| 参数   | 说明                     | 特别说明                                         |
| ------ | ------------------------ | ------------------------------------------------ |
| tagid  | 要获取用户列表的标签ID   | 该参数如果没有则表示执行拉取指定用户下的标签列表 |
| openid | 要获取用户列表的起始位置 | 如果没有传递tagid则表示要查询标签列表的用户      |

##### Response

> 指定tagid时，查询的json数据

```json
{  
    "count":2,//这次获取的粉丝数量   
    "data":{//粉丝列表
    	"openid":[  
    		"ocYxcuAEy30bX0NXmGn4ypqx3tI0",    
    		"ocYxcuBt0mRugKZ7tGAHPnUaOW7Y"  ]  
	},  
    "next_openid":"ocYxcuBt0mRugKZ7tGAHPnUaOW7Y"//拉取列表最后一个用户的openid 
}
```

> 未指定tagid时，查询的json数据

```json
{   "tagid_list":[134, 2]//被置上的标签列表 }
```

> 当两个参数都不存在时，返回异常数据

```json
{ "errcode": -1, "errmsg":"参数缺失或参数错误" }
```

#### 3.2 批量为用户打标签

##### Request

- method: put
- form-data

| 参数        | 说明                 |
| ----------- | -------------------- |
| openid_list | 要打上标签的用户列表 |
| tagid       | 要打上的标签的ID     |

##### Response

> 正确响应json

```json
{   "errcode":0, "errmsg":"ok" }
```

#### 3.3 批量为用户取消标签

##### Request

- method: delete
- form-data

| 参数        | 说明                 |
| ----------- | -------------------- |
| openid_list | 要取消标签的用户列表 |
| tagid       | 要取消的标签的ID     |

##### Response

> 正确响应json

```json
{   "errcode":0, "errmsg":"ok" }
```

### 4.用户备注接口

#### URL

> http://localhost:5000/api/v0.1/cgi-bin/user/remark

#### Response

- method: put
- form-data

| 参数   | 说明                     |
| ------ | ------------------------ |
| openid | 要添加备注的用户的openid |
| remark | 要添加的备注信息         |

#### Response

> 正常响应json数据

```json
{ "errcode":0, "errmsg":"ok" }
```

> 错误时响应json数据

```json
{ "errcode":40013, "errmsg":"invalid appid" }
```





## wms

后台管理系统。注册用户可以管理微信公众号的部分信息，查看历史交互记录，分析用户行为等等业余。不同用户管理员赋予不同权限则可以进行不同的操作。管理员具有所有权和赋权权限。





### 认证系统

token登录认证

登录后在客户端存入cookie包含用户名和token信息

接口访问要在请求中添加token

