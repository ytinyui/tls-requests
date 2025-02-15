import ctypes
import glob
import os
import platform
import re
import sys
from dataclasses import dataclass, field, fields
from pathlib import Path
from platform import machine
from typing import List, Optional

import requests
from tqdm import tqdm

__all__ = ["TLSLibrary"]

BIN_DIR = os.path.join(Path(__file__).resolve(strict=True).parent.parent / "bin")
GITHUB_API_URL = "https://api.github.com/repos/bogdanfinn/tls-client/releases"
PLATFORM = sys.platform
IS_UBUNTU = False
ARCH_MAPPING = {
    "amd64": "amd64",
    "x86_64": "amd64",
    "x86": "386",
    "i686": "386",
    "i386": "386",
    "arm64": "arm64",
    "aarch64": "arm64",
    "armv5l": "arm-5",
    "armv6l": "arm-6",
    "armv7l": "arm-7",
    "ppc64le": "ppc64le",
    "riscv64": "riscv64",
    "s390x": "s390x",
}

FILE_EXT = ".unk"
MACHINE = ARCH_MAPPING.get(machine()) or machine()
if PLATFORM == "linux":
    FILE_EXT = "so"
    try:
        platform_data = platform.freedesktop_os_release()
        if "ID" in platform_data:
            curr_system = platform_data["ID"]
        else:
            curr_system = platform_data.get("id")

        if "ubuntu" in str(curr_system).lower():
            IS_UBUNTU = True

    except Exception as e:  # noqa
        pass

elif PLATFORM in ("win32", "cygwin"):
    PLATFORM = "windows"
    FILE_EXT = "dll"
elif PLATFORM == "darwin":
    FILE_EXT = "dylib"

PATTERN_RE = re.compile(r"%s-%s.*%s" % (PLATFORM, MACHINE, FILE_EXT), re.I)
PATTERN_UBUNTU_RE = re.compile(r"%s-%s.*%s" % ("ubuntu", MACHINE, FILE_EXT), re.I)

TLS_LIBRARY_PATH = os.getenv("TLS_LIBRARY_PATH")


@dataclass
class BaseRelease:

    @classmethod
    def model_fields_set(cls) -> set:
        return {model_field.name for model_field in fields(cls)}

    @classmethod
    def from_kwargs(cls, **kwargs):
        model_fields_set = cls.model_fields_set()
        return cls(**{k: v for k, v in kwargs.items() if k in model_fields_set})


@dataclass
class ReleaseAsset(BaseRelease):
    browser_download_url: str
    name: Optional[str] = None


@dataclass
class Release(BaseRelease):
    name: Optional[str] = None
    tag_name: Optional[str] = None
    assets: List[ReleaseAsset] = field(default_factory=list)

    @classmethod
    def from_kwargs(cls, **kwargs):
        model_fields_set = cls.model_fields_set()
        assets = kwargs.pop("assets", []) or []
        kwargs["assets"] = [
            ReleaseAsset.from_kwargs(**asset_kwargs) for asset_kwargs in assets
        ]
        return cls(**{k: v for k, v in kwargs.items() if k in model_fields_set})


class TLSLibrary:
    """TLS Library

    A utility class for managing the TLS library, including discovery, validation,
    downloading, and loading. This class facilitates interaction with system-specific
    binaries, ensuring compatibility with the platform and machine architecture.

    Class Attributes:
        _PATH (str): The current path to the loaded TLS library.

    Methods:
        fetch_api(version: Optional[str] = None, retries: int = 3) -> Generator[str, None, None]:
            Fetches library download URLs from the GitHub API for the specified version.

        is_valid(fp: str) -> bool:
            Validates a file path against platform-specific patterns.

        find() -> str:
            Finds the first valid library binary in the binary directory.

        find_all() -> list[str]:
            Lists all library binaries in the binary directory.

        download(version: Optional[str] = None) -> str:
            Downloads the library binary for the specified version.

        set_path(fp: str):
            Sets the path to the currently loaded library.

        load() -> ctypes.CDLL:
            Loads the library, either from an existing path or by discovering and downloading it.
    """

    _PATH: str = None
    _STATIC_API_DATA = {
        "name": "v1.7.10",
        "tag_name": "v1.7.10",
        "assets": [
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-darwin-amd64-1.7.10.dylib",
                "name": "tls-client-darwin-amd64-1.7.10.dylib",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-darwin-arm64-1.7.10.dylib",
                "name": "tls-client-darwin-arm64-1.7.10.dylib",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-linux-arm64-1.7.10.so",
                "name": "tls-client-linux-arm64-1.7.10.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-linux-armv7-1.7.10.so",
                "name": "tls-client-linux-armv7-1.7.10.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-linux-ubuntu-amd64-1.7.10.so",
                "name": "tls-client-linux-ubuntu-amd64-1.7.10.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-windows-32-1.7.10.dll",
                "name": "tls-client-windows-32-1.7.10.dll",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-windows-64-1.7.10.dll",
                "name": "tls-client-windows-64-1.7.10.dll",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-darwin-amd64.dylib",
                "name": "tls-client-xgo-1.7.10-darwin-amd64.dylib",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-darwin-arm64.dylib",
                "name": "tls-client-xgo-1.7.10-darwin-arm64.dylib",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-386.so",
                "name": "tls-client-xgo-1.7.10-linux-386.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-amd64.so",
                "name": "tls-client-xgo-1.7.10-linux-amd64.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-arm-5.so",
                "name": "tls-client-xgo-1.7.10-linux-arm-5.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-arm-6.so",
                "name": "tls-client-xgo-1.7.10-linux-arm-6.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-arm-7.so",
                "name": "tls-client-xgo-1.7.10-linux-arm-7.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-arm64.so",
                "name": "tls-client-xgo-1.7.10-linux-arm64.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-ppc64le.so",
                "name": "tls-client-xgo-1.7.10-linux-ppc64le.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-riscv64.so",
                "name": "tls-client-xgo-1.7.10-linux-riscv64.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-linux-s390x.so",
                "name": "tls-client-xgo-1.7.10-linux-s390x.so",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-windows-386.dll",
                "name": "tls-client-xgo-1.7.10-windows-386.dll",
            },
            {
                "browser_download_url": "https://github.com/bogdanfinn/tls-client/releases/download/v1.7.10/tls-client-xgo-1.7.10-windows-amd64.dll",
                "name": "tls-client-xgo-1.7.10-windows-amd64.dll",
            },
        ],
    }

    @classmethod
    def fetch_api(cls, version: str = None, retries: int = 3):
        def _find_release(data, version_: str = None):
            releases = [
                Release.from_kwargs(**kwargs) for kwargs in data
            ]

            if version_ is not None:
                version_ = (
                    "v%s" % version_
                    if not str(version_).startswith("v")
                    else str(version_)
                )
                releases = [
                    release
                    for release in releases
                    if re.search(version_, release.name, re.I)
                ]

            for release in releases:
                for asset in release.assets:
                    if IS_UBUNTU and PATTERN_UBUNTU_RE.search(
                        asset.browser_download_url
                    ):
                        ubuntu_urls.append(asset.browser_download_url)
                    if PATTERN_RE.search(asset.browser_download_url):
                        asset_urls.append(asset.browser_download_url)

        asset_urls, ubuntu_urls = [], []
        for _ in range(retries):
            try:
                response = requests.get(GITHUB_API_URL)
                if response.ok:
                    _find_release(response.json())
                    break

            except Exception as ex:
                print("Unable to fetch GitHub API: %s" % ex)

        if not asset_urls and not ubuntu_urls:
            _find_release([cls._STATIC_API_DATA])

        for url in ubuntu_urls:
            yield url

        for url in asset_urls:
            yield url

    @classmethod
    def find(cls) -> str:
        for fp in cls.find_all():
            if PATTERN_RE.search(fp):
                return fp

    @classmethod
    def find_all(cls) -> List[str]:
        return [
            src
            for src in glob.glob(os.path.join(BIN_DIR, r"*"))
            if src.lower().endswith(("so", "dll", "dylib"))
        ]

    @classmethod
    def download(cls, version: str = None) -> str:
        try:
            print(
                "System Info - Platform: %s, Machine: %s, File Ext : %s."
                % (
                    PLATFORM,
                    "%s (Ubuntu)" % MACHINE if IS_UBUNTU else MACHINE,
                    FILE_EXT,
                )
            )
            download_url = None
            for download_url in cls.fetch_api(version):
                if download_url:
                    break

            print("Library Download URL: %s" % download_url)
            if download_url:
                destination = os.path.join(BIN_DIR, download_url.split("/")[-1])
                with requests.get(download_url, stream=True) as response:
                    response.raise_for_status()
                    os.makedirs(BIN_DIR, exist_ok=True)
                    total_size = int(response.headers.get("content-length", 0))
                    chunk_size = 1024
                    with open(
                        os.path.join(BIN_DIR, download_url.split("/")[-1]), "wb"
                    ) as file, tqdm(
                        desc=destination,
                        total=total_size,
                        unit="iB",
                        unit_scale=True,
                        unit_divisor=chunk_size,
                    ) as progress_bar:
                        for chunk in response.iter_content(chunk_size):
                            size = file.write(chunk)
                            progress_bar.update(size)

                return destination

        except requests.exceptions.HTTPError as ex:
            print("Unable to download file: %s" % ex)

    @classmethod
    def set_path(cls, fp: str):
        cls._PATH = fp

    @classmethod
    def load(cls):
        """Load libraries"""

        def _load_libraries(fp_):
            try:
                lib = ctypes.cdll.LoadLibrary(fp_)
                cls.set_path(fp_)
                return lib
            except Exception as ex:
                print("Unable to load TLS Library, details: %s" % ex)
                try:
                    os.remove(fp_)
                except FileNotFoundError:
                    pass

        if cls._PATH is not None:
            library = _load_libraries(cls._PATH)
            if library:
                return library

        if TLS_LIBRARY_PATH:
            library = _load_libraries(TLS_LIBRARY_PATH)
            if library:
                return library

        for fp in cls.find_all():
            if IS_UBUNTU and PATTERN_UBUNTU_RE.search(fp):
                library = _load_libraries(fp)
                if library:
                    return library
            if PATTERN_RE.search(fp):
                library = _load_libraries(fp)
                if library:
                    return library

        download_fp = cls.download()
        if download_fp:
            library = _load_libraries(download_fp)
            if library:
                return library

        raise OSError("Your system does not support TLS Library.")
