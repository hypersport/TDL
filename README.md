#TDL

TDL — ToDoList 使用 Python Flask 框架开发的一个中文版待做事项列表小应用，包括查看、添加、完成、删除、搜索、用户管理等功能。

这个应用主要是想在 Linux 平台上使用，理论上应该可以在任何装有 Python (version 2) 及相应包的平台上使用，因为本人就一直用 Linux，不能保证 Windows 以及 MacOS 平台是否能正常使用，另外还有一个原因是 Windows 和 MacOS 系统上相应的软件很多，而且这个应用主要以 Web 页面和命令行操作为主，并没有精美的 GUI 界面。

这个应用包括三部分：

- 服务端
- Web 客户端
- 命令行

通过 python run_tdl.py 启动应用，web 页面访问 [http://localhost:9468](http://localhost:9468)。

第一个启动应用时会创建 $HOME/.tdl/ 目录，该目录包括三个文件:
- README 是说明文件
- tdl.json 是应用的选择配置文件
    ```
    {
    "config_type": "default",
    "host": "localhost",
    "port": 9468
    }
    ```
    - 修改 config_type 的值，默认的 default 为 development ，还可选择 production ;
    - 修改 host 的值;
    - 修改端口 port 的值
- tdl.db 是应用的 SQLite 数据库文件。