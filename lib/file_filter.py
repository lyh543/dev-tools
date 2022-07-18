from typing import Callable, List

TEXT_FILE_EXTENSIONS = [
    "py",
    "html",
    "css",
    "js",
    "json",
    "md",
    "ts",
    "tsx",
    "txt",
    "bat",
    "sh",
    "ps1",
]
IMAGE_FILE_EXTENSIONS = ["jpg", "jpeg", "png"]
VIDEO_FILE_EXTENSIONS = [
    "mp4",
    "avi",
    "mkv",
    "mov",
    "m4v",
    "webm",
    "wmv",
    "flv",
    "vob",
    "ogv",
    "ogg",
    "mpg",
    "mpeg",
    "m2v",
    "m4p",
    "m4v",
    "mp4v",
    "svi",
    "3gp",
    "3g2",
    "mxf",
    "roq",
    "nsv",
    "f4v",
    "f4p",
    "f4a",
    "f4b",
]
COMMON_IGNORED_DIRECTORIES = [
    "node_modules",
    ".git",
    ".idea",
    ".vscode",
    "build",
    "dist",
    "__pycache__",
]

# filter(filename, filepath) -> file matches if returns True
FileFilter = Callable[[str, str], bool]


def no_filter(filename: str, filepath: str) -> bool:
    return True


def filename_allow_filter(allowlist: List[str]) -> FileFilter:
    def _filter(filename: str, filepath: str) -> bool:
        return filename in allowlist

    return _filter


def filename_block_filter(blocklist: List[str]) -> FileFilter:
    def _filter(filename: str, filepath: str) -> bool:
        return filename.lower() not in blocklist

    return _filter


def extension_allow_filter(allowlist: List[str]) -> FileFilter:
    def _filter(filename: str, filepath: str) -> bool:
        return filename.split(".")[-1].lower() in allowlist

    return _filter


def extension_block_filter(blocklist: List[str]) -> FileFilter:
    def _filter(filename: str, filepath: str) -> bool:
        return filename.split(".")[-1] not in blocklist

    return _filter
