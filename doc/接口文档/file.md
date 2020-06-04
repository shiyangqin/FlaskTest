# 文件模块

+ [文件上传](#文件上传)
+ [文件下载](#文件下载)

## 文件上传

url: /file/upload

method：post

params：file

return：
```python
{
    "status": "ok",
    "data": "E:\\me\\Qinsy\\flask_test\\file\\1586505723.9923966"
}
```

___
## 文件下载

url: /file/download

method：get

params：
```python
{
    "file_path": "E:\\me\\Qinsy\\flask_test\\file\\1586505723.9923966",
    "file_path": "test.xls"
}
```

return：test.xls
