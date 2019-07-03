# SProxyPool

本项目的目标是提供一个可用的高匿名IP代理池，通过Mac及linux平台测试，如果使用linux平台请自行更换相应geckodriver

## 运行环境
- python3.6.3
    - 网络请求
        - aiohttp
        - requests
    - 进程，异步
        - asyncio
        - multiprocessing
    - 网页解析
        - lxml
        - re
        - base64
        - js2py
- Redis
- 相关依赖
    > pip install -r requirements.txt

## 实现的功能
- 利用asyncio和aiohttp实现异步并发请求
- 利用js2py解除cookie限制，以及实现对js加密数据的解密
- 结合selenium，破解cookie反爬
- proxy验证过程中
    > 为解决匿名验证<http://httpbin.org>网站响应过慢问题，利用flask+uwsgi+nginx搭建简单网站系统，并开放接口
    获取X-Forwarded-For参数值，最终验证proxy是否高匿名
    
    > 关于验证策略，为验证结果不稳定的问题，防止代理有效性的误判，将对代理进行三次验证。
    具体策略是，爬取到的代理初始分值为60分，验证成功设置为100分，失败减20，每次从原始代理库按照分数
    从低到高且分值小于100分的原则取值，如果三次验证都失败，则直接删除该代理。可以通过settings配置验证的次数。
- 爬虫组件，可以根据不同网站的网页布局自由定制解析函数

## 安装运行
- 安装redis数据库，并在settings配置
- 根据自身系统，选择安装相应的geckodriver
    > https://github.com/mozilla/geckodriver/releases
- 安装依赖
    > pip install -r requirements.txt
- 运行程序
    > python run.py
- 检查代理
    > python proxycheck.py
- 结合supervisor运行定时任务
    > 相关文件为timedtask.py

    
