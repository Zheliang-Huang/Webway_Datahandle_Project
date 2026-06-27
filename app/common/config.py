from pathlib import Path
from typing import Any, Dict, List
import yaml

BASE_DIR = Path(__file__).resolve().parent.parent


class ConfigError(Exception):
    """配置文件错误"""
    pass


class Appconfig:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)

        if not self.config_path.exists():
            raise ConfigError(f"配置文件不存在：{self.config_path}")

        self.raw = self._load_yaml()
        self.project = self.raw.get("project", {})
        self.paths = self.raw.get("paths", {})
        self.ocr = self.raw.get("ocr", {})
        self.image = self.raw.get("image", {})
        self.quality = self.raw.get("quality", {})
        self.steps = self.raw.get("steps", {})

        self._validate()
        self._normalize_paths()
        self._ensure_dirs()

    def _load_yaml(self):
        try:
            with open(self.config_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f)
        except Exception as e:
            raise ConfigError(f"读取配置文件失败：{e}")

        if not isinstance(data, dict):
            raise ConfigError("配置文件格式错误：yaml 顶层必须是字典结构")

        return data

    def _validate(self):
        """校验必要配置项"""
        required_sections = ["project", "paths", "ocr", "image", "steps"]

        for section in required_sections:
            if section not in self.raw:
                raise ConfigError(f"缺少配置段：{section}")

        required_paths = [
            "input_dir",
            "work_dir",
            "output_dir",
            "error_dir",
            "report_dir",
            "log_dir",
            "state_file",
        ]

        for key in required_paths:
            if key not in self.paths:
                raise ConfigError(f"paths 缺少必要配置：{key}")

        required_ocr = ["url", "threads", "timeout", "retry"]

        for key in required_ocr:
            if key not in self.ocr:
                raise ConfigError(f"ocr 缺少必要配置：{key}")

        if "allow_ext" not in self.image:
            raise ConfigError("image 缺少必要配置：allow_ext")

    def _normalize_paths(self):
        """统一处理路径"""

        for key, value in self.paths.items():

            p = Path(value)

            if not p.is_absolute():
                p = BASE_DIR / p

            self.paths[key] = p.resolve()

    def _ensure_dirs(self):
        """自动创建必要目录"""
        dir_keys = [
            "work_dir",
            "output_dir",
            "error_dir",
            "report_dir",
            "log_dir",
        ]

        for key in dir_keys:
            self.paths[key].mkdir(parents=True, exist_ok=True)

        state_file: Path = self.paths["state_file"]
        state_file.parent.mkdir(parents=True, exist_ok=True)

    @property
    def project_name(self) -> str:
        return self.project.get("name", "")

    @property
    def batch_name(self) -> str:
        return self.project.get("batch_name", "")

    @property
    def input_dir(self) -> Path:
        return self.paths["input_dir"]

    @property
    def log_dir(self) -> Path:
        return self.paths["log_dir"]
