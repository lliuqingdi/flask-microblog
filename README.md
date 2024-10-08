# learn flask
# 环境安装
## 1.windows下安装依赖
### pip install -r requirements.txt
### python版本要求3.8以上

## 2.linux下安装，以centos7为例
### (1)安装docker
### (2)来到项目根目录
### (3)输入docker build -t flask_blog .
### (4)构建完镜像后，docker run -id --name=microblog -d -v .:/flask_microblog -p 5000:5000 flask_blog:latest