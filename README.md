# dailynews  60s读懂世界
一个很简单的每日早报小插件

[api地址](http://dwz.2xb.cn/zaob) 感谢api作者
## 安装方法
### 懒人法
&emsp;&emsp;将`dailynews.py`丢入任意一个已启用模块中然后重启hoshino
### 不是懒人法
* 在`HoshinoBot\hoshino\modules`下新建一个文件夹
* 将`dailynews.py`放入其中
* 在 `HoshinoBot\hoshino\config\__bot__.py` 文件的 `MODULES_ON` 里加入新建的文件夹的名字
* 重启hoshino
## 依赖要求
aiocqhttp>=1.4
>如果你的[Hoshino](https://github.com/Ice-Cirno/HoshinoBot)一直保持最新版本，那一定符合此要求

如果你在使用旧版本并且不愿意更新，可以将代码中两处使用`MessageSegment.image`的地方将`cache`参数去掉，该参数的作用是避免重复下载
## 使用方式
[启用 dailynews] 插件默认禁用，需要手动开启

启用后，将会在每天早上发送一份早报

[@bot 今日早报] （测试用）手动获取一份早报
## 注意
* 该api使用量应该不小，所以一天过去的越久，早报图片的发送次数越多，在晚上发送可能会风控
* 自动推送偶尔会发生读取json出错的情况，推测可能是网络波动
## 鸣谢
[Hoshino](https://github.com/Ice-Cirno/HoshinoBot) <s>星乃真好玩</s>

[早报api](http://dwz.2xb.cn/zaob) <s>虽然我不知道这个api哪里来的也不知道是谁写的</s>
## License
This project is licensed under [GLWTPL](https://github.com/me-shaon/GLWTPL/blob/master/LICENSE)
