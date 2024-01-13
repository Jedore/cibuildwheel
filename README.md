cibuildwheel-cn
============

[![PyPI - Python Version](https://badgen.net/badge/pypi/v2.16.2.1/blue)](https://pypi.org/project/cibuildwhell-cn)

本项目完全参考 [cibuildwheel](https://github.com/pypa/cibuildwheel), 这是一个比较全面的`Python`库构建工具。

在使用`cibuildwheel`的过程中发现需要下载 Python安装包 以及 docker镜像 等其他资源，
这些资源默认都是从国外网站下载，在国内使用 `cibuildwheel` 构建时， 由于种种原因，
资源下载速度非常慢，导致构建体验不太友好。 因此有了 `cibuildwheel-cn`, 加速国内构建体验。
功能和`cibuildwheel`保持一致。

### 使用

**不能和`cibuildwheel`同时安装**

```bash
pip install cibuildwheel-cn
```

同`cibuildwheel`使用方法一样，参考 [cibuildwheel文档](https://cibuildwheel.readthedocs.io/en/v2.16.2/),

### 变更列表

- [build-platforms.toml](cibuildwheel/resources/build-platforms.toml) macos python configurations
- [docker images](bin/update_docker.py)
- [update virtualenv](bin/update_virtualenv.py)
- [pinned docker images](cibuildwheel/resources/pinned_docker_images.cfg)
- [virtualenv](cibuildwheel/resources/virtualenv.toml)

[cibuildwheel LICENSE](CIBUILDWHEEL_LICENSE)
