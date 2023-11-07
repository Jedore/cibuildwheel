#!/usr/bin/env python3
from __future__ import annotations

import configparser
from dataclasses import dataclass
from pathlib import Path

import requests
from packaging.version import Version

DIR = Path(__file__).parent.resolve()
RESOURCES = DIR.parent / "cibuildwheel/resources"


@dataclass(frozen=True)
class Image:
    manylinux_version: str
    platform: str
    image_name: str
    tag: str | None  # Set this to pin the image


class PyPAImage(Image):
    def __init__(self, manylinux_version: str, platform: str, tag: str | None):
        platform_no_pypy = platform[5:] if platform.startswith("pypy_") else platform
        image_name = f"quay.io/pypa/{manylinux_version}_{platform_no_pypy}"
        super().__init__(manylinux_version, platform, image_name, tag)


images = [
    # manylinux1 images
    Image("manylinux1", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux1_x86_64", None),
    Image("manylinux1", "i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux1_i686", None),
    # manylinux2010 images
    Image("manylinux2010", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2010_x86_64", None),
    Image("manylinux2010", "i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux2010_i686", None),
    Image("manylinux2010", "pypy_x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2010_x86_64", None),
    Image("manylinux2010", "pypy_i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux2010_i686", None),
    # manylinux2014 images
    Image("manylinux2014", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_x86_64", None),
    Image("manylinux2014", "i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_i686", None),
    Image("manylinux2014", "aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_aarch64", None),
    Image("manylinux2014", "ppc64le", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_ppc64le", None),
    Image("manylinux2014", "s390x", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_s390x", None),
    Image("manylinux2014", "pypy_x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_x86_64", None),
    Image("manylinux2014", "pypy_i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_i686", None),
    Image("manylinux2014", "pypy_aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux2014_aarch64", None),
    # manylinux_2_24 images
    Image("manylinux_2_24", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_x86_64", None),
    Image("manylinux_2_24", "i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_i686", None),
    Image("manylinux_2_24", "aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_aarch64", None),
    Image("manylinux_2_24", "ppc64le", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_ppc64le", None),
    Image("manylinux_2_24", "s390x", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_s390x", None),
    Image("manylinux_2_24", "pypy_x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_x86_64", None),
    Image("manylinux_2_24", "pypy_i686", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_i686", None),
    Image("manylinux_2_24", "pypy_aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_24_aarch64", None),
    # manylinux_2_28 images
    Image("manylinux_2_28", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_x86_64", None),
    Image("manylinux_2_28", "aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_aarch64", None),
    Image("manylinux_2_28", "ppc64le", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_ppc64le", None),
    Image("manylinux_2_28", "s390x", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_s390x", None),
    Image("manylinux_2_28", "pypy_x86_64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_x86_64", None),
    Image("manylinux_2_28", "pypy_aarch64", "quay.mirrors.ustc.edu.cn/pypa/manylinux_2_28_aarch64", None),
    # manylinux_2_31 images
    Image("manylinux_2_31", "armv7l", "ghcr.io/mayeut/manylinux_2_31", None),
    # manylinux_2_34 images
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/x86_64", None),
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/aarch64", None),
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/ppc64le", None),
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/s390x", None),
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/pypy_x86_64", None),
    PyPAImage("manylinux_2_34", "quay.mirrors.ustc.edu.cn/pypa/pypy_aarch64", None),
    # musllinux_1_1 images
    Image("musllinux_1_1", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_1_x86_64", None),
    Image("musllinux_1_1", "i686", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_1_i686", None),
    Image("musllinux_1_1", "aarch64", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_1_aarch64", None),
    Image("musllinux_1_1", "ppc64le", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_1_ppc64le", None),
    Image("musllinux_1_1", "s390x", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_1_s390x", None),
    # musllinux_1_2 images
    Image("musllinux_1_2", "x86_64", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_2_x86_64", None),
    Image("musllinux_1_2", "i686", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_2_i686", None),
    Image("musllinux_1_2", "aarch64", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_2_aarch64", None),
    Image("musllinux_1_2", "ppc64le", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_2_ppc64le", None),
    Image("musllinux_1_2", "s390x", "quay.mirrors.ustc.edu.cn/pypa/musllinux_1_2_s390x", None),
]

config = configparser.ConfigParser()

for image in images:
    # get the tag name whose digest matches 'latest'
    if image.tag is not None:
        # image has been pinned, do not update
        tag_name = image.tag
    elif image.image_name.startswith("quay.io/"):
        _, _, repository_name = image.image_name.partition("/")
        response = requests.get(
            f"https://quay.io/api/v1/repository/{repository_name}?includeTags=true"
        )
        response.raise_for_status()
        repo_info = response.json()
        tags_dict = repo_info["tags"]

        latest_tag = tags_dict.pop("latest")
        # find the tag whose manifest matches 'latest'
        tag_name = next(
            name
            for (name, info) in tags_dict.items()
            if info["manifest_digest"] == latest_tag["manifest_digest"]
        )
    elif image.image_name.startswith("quay.mirrors.ustc.edu.cn/"):
        _, _, repository_name = image.image_name.partition("/")
        response = requests.get(
            f"https://quay.mirrors.ustc.edu.cn//api/v1/repository/{repository_name}?includeTags=true"
        )
        response.raise_for_status()
        repo_info = response.json()
        tags_dict = repo_info["tags"]

        latest_tag = tags_dict.pop("latest")
        # find the tag whose manifest matches 'latest'
        tag_name = next(
            name
            for (name, info) in tags_dict.items()
            if info["manifest_digest"] == latest_tag["manifest_digest"]
        )
    elif image.image_name.startswith("ghcr.io/"):
        repository = image.image_name[8:]
        response = requests.get(
            "https://ghcr.io/token", params={"scope": f"repository:{repository}:pull"}
        )
        response.raise_for_status()
        token = response.json()["token"]
        response = requests.get(
            f"https://ghcr.io/v2/{repository}/tags/list",
            headers={"Authorization": f"Bearer {token}"},
        )
        response.raise_for_status()
        ghcr_tags = [(Version(tag), tag) for tag in response.json()["tags"] if tag != "latest"]
        ghcr_tags.sort(reverse=True)
        tag_name = ghcr_tags[0][1]
    else:
        response = requests.get(f"https://hub.docker.com/v2/repositories/{image.image_name}/tags")
        response.raise_for_status()
        tags = response.json()["results"]

        latest_tag = next(tag for tag in tags if tag["name"] == "latest")
        # i don't know what it would mean to have multiple images per tag
        assert len(latest_tag["images"]) == 1
        digest = latest_tag["images"][0]["digest"]

        pinned_tag = next(
            tag for tag in tags if tag != latest_tag and tag["images"][0]["digest"] == digest
        )
        tag_name = pinned_tag["name"]

    if not config.has_section(image.platform):
        config[image.platform] = {}

    config[image.platform][image.manylinux_version] = f"{image.image_name}:{tag_name}"

with open(RESOURCES / "pinned_docker_images.cfg", "w") as f:
    config.write(f)
