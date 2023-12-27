##############################################
# 基于centos7构建python3运行环境
# 构建命令: 在Dockerfile文件目录下执行 docker build   -t python:37 --build-arg takskid=1 --build-arg type=1 .
# 容器启动命令:
# docker run -itd --name con_name --restart always --privileged=true -v /root/lib/site-packages:/usr/local/python3/lib/python3.7/site-packages  -v /root/test/install:/root/install/ -v /root/darknet/vcrawl:/root/python/vcrawl  image_name  /usr/sbin/init
# 进入容器：docker exec -it con_name /bin/bash
##############################################
FROM centos:7.6.1810
MAINTAINER thor # 指定作者信息
RUN set -ex \
    # 预安装所需组件
    && yum install -y wget tar libffi-devel zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gcc make initscripts \
    && wget https://www.python.org/ftp/python/3.7.9/Python-3.7.9.tgz \
    && tar -zxvf Python-3.7.9.tgz \
    && cd Python-3.7.9 \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean \
    && yum install -y epel-release \
    && yum install -y python-pip \
    && yum install xz-devel -y \
    && yum install python-backports-lzma -y \
    && pip install backports.lzma \
    && yum install mesa-libGL -y \
    && yum install telnet -y \
    && yum install net-tools -y \
    && ./configure prefix=/usr/local/python3 \
    && make \
    && make install \
    && make clean
# 设置默认为python3
RUN set -ex \
    # 备份旧版本python
    && mv /usr/bin/python /usr/bin/python27 \
    && mv /usr/bin/pip /usr/bin/pip27 \
    # 配置默认为python3
    && ln -s /usr/local/python3/bin/python3.7 /usr/bin/python \
    && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip
# 修复因修改python版本导致yum失效问题
RUN set -ex \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/bin/yum \
    && sed -i "s#/usr/bin/python#/usr/bin/python2.7#" /usr/libexec/urlgrabber-ext-down \
    && yum install -y deltarpm
# 基础环境配置
RUN set -ex \
    # 修改系统时区为东八区
    && rm -rf /etc/localtime \
    && ln -s /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && yum install -y vim \
    # 安装定时任务组件
    && yum -y install cronie

# 添加镜像配置
RUN set -ex \
    # 下载
    && curl -O http://ftp.gnu.org/gnu/glibc/glibc-2.18.tar.gz \
    && tar zxf glibc-2.18.tar.gz \
    && cd glibc-2.18 \
    && mkdir build \
    && cd build \
    && ../configure --prefix=/usr \
    && make -j2 \
    && make install \
    && yum install gtk2 -y \
    && yum install gtk3 -y \
    && yum install alsa-lib-devel -y

# 支持中文
RUN yum install kde-l10n-Chinese -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
# 更新pip版本
RUN pip install --upgrade pip
ENV LC_ALL zh_CN.UTF-8

WORKDIR /root/python/deploy
#COPY requirements.txt .
#RUN set -ex \
#    && python -m pip install -i https://pypi.tuna.tsinghua.edu.cn/simple -r requirements.txt

CMD ./start.sh ${takskid} ${type}

