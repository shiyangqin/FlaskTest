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
    "data": {
        "file_name": "Antiy.txt",
        "file_md5": "8000c660bc3002b44b9fec2f7a5a203f",
        "file_path": "E:\\me\\OA\\file\\8000c660bc3002b44b9fec2f7a5a203f"
    }
}
```

___
## 文件下载

url: /file/download/<file_md5>

method：get

params：无

return：file
