简单部署方式：
- 建立数据库：server(web版使用的数据库)和local(单机版使用的数据库)
- 修改数据库配置，settings.py
- 安装项目运行依赖：pip install from requirement.txt 
- 启动项目自带的服务器：python manage.py runserver 0.0.0.0:8000(端口号可以自己修改)

调用方式：
> 以分卷为单位进行生成
>
> 8000：端口号，根据自己部署时配置修改

http://localhost:8000/get_pdf/?gid={参数1}&grpid={参数2}

传入的参数为：
- 参数1：gid
- 参数2：grpid

返回结果为生成的文件路径
