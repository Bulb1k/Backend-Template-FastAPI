import logging
from dataclasses import dataclass, asdict
from pathlib import Path
from typing import Dict, Any

from libcloud.storage.drivers.local import LocalStorageDriver
from pydantic.types import SecretType
from sqlalchemy_file import FileField, ImageField
from sqlalchemy_file.file import File
from sqlalchemy_file.storage import StorageManager

from app.core.config import settings

logger = logging.getLogger(__name__)

@dataclass
class Storages:

    @classmethod
    def to_list(cls):
        instance = cls()
        return list(asdict(instance).values())


class StorageService:
    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.settings = settings
            self.storage_root = Path(self.settings.STORAGE_DIR)
            self.storage_root.mkdir(parents=True, exist_ok=True)
            self._storages = set()

            self.driver = LocalStorageDriver(str(self.storage_root))

            self._register_storages()

            StorageService._initialized = True
            logger.info(f"StorageService initialized with root: {self.storage_root}")

    def _register_storages(self):

        for storage_name in Storages.to_list():
            self._ensure_storage(storage_name)

    def _ensure_storage(self, storage_name: str) -> None:

        try:
            if storage_name in self._storages:
                logger.debug(f"Storage '{storage_name}' already registered")
                return

            storage_path = self.storage_root / storage_name
            storage_path.mkdir(parents=True, exist_ok=True)

            try:
                container = self.driver.get_container(storage_name)
                logger.debug(f"Container '{storage_name}' already exists")
            except Exception:
                container = self.driver.create_container(storage_name)
                logger.info(f"Created new container: {storage_name}")

            StorageManager.add_storage(storage_name, container)
            self._storages.add(storage_name)
            logger.info(f"Storage '{storage_name}' registered successfully")

        except Exception as e:
            logger.error(f"Failed to ensure storage '{storage_name}': {e}")
            raise

    @classmethod
    def file_field(
            cls,
            table_name: str,
            subdir: str = "file",
            multiple: bool = False,
            **kwargs
    ) -> FileField:

        instance = cls()
        storage_name = f"{table_name}_{subdir}"
        instance._ensure_storage(storage_name)

        return FileField(
            upload_storage=storage_name,
            multiple=multiple,
            **kwargs
        )

    @classmethod
    def image_field(
            cls,
            table_name: str,
            subdir: str = "image",
            thumbnail_size: tuple = None,
            **kwargs
    ) -> ImageField:

        instance = cls()
        storage_name = f"{table_name}_{subdir}"
        instance._ensure_storage(storage_name)

        field_kwargs = {
            "upload_storage": storage_name,
            **kwargs
        }

        if thumbnail_size:
            field_kwargs["thumbnail_size"] = thumbnail_size

        return ImageField(**field_kwargs)

    @classmethod
    def get_file_url(cls, file_obj: File, base_url: str = None) -> str | None:

        if not file_obj:
            return None

        instance = cls()

        if base_url is None:
            base_url = instance.settings.BASE_URL or "http://localhost:8000"

        base_url = base_url.rstrip('/')

        return f"{base_url}/static/{file_obj.path}"

    @classmethod
    def get_file_path(cls, file_obj: File) -> Path | None:

        if not file_obj:
            return None

        instance = cls()
        return instance.storage_root / file_obj.path

    @classmethod
    def delete_file(cls, file_obj: File) -> bool:

        if not file_obj:
            return False

        try:
            file_path = cls.get_file_path(file_obj)
            if file_path and file_path.exists():
                file_path.unlink()
                logger.info(f"File deleted: {file_path}")
                return True
            return False
        except Exception as e:
            logger.error(f"Failed to delete file {file_obj.path}: {e}")
            return False

    @classmethod
    def get_storage_info(cls) -> Dict[str, Any]:

        instance = cls()

        info = {
            "storage_root": str(instance.storage_root),
            "registered_storages": [],
            "total_size": 0
        }

        try:
            for storage_name in StorageManager._storages.keys():
                storage_path = instance.storage_root / storage_name
                if storage_path.exists():
                    size = sum(f.stat().st_size for f in storage_path.rglob('*') if f.is_file())
                    file_count = len(list(storage_path.rglob('*')))

                    info["registered_storages"].append({
                        "name": storage_name,
                        "path": str(storage_path),
                        "size_bytes": size,
                        "file_count": file_count
                    })
                    info["total_size"] += size

        except Exception as e:
            logger.error(f"Failed to get storage info: {e}")

        return info

    @classmethod
    def cleanup_orphaned_files(cls) -> Dict[str, int]:

        logger.warning("cleanup_orphaned_files not implemented - requires database integration")
        return {"deleted_files": 0, "freed_bytes": 0}


def initialize_storage() -> StorageService:
    return StorageService()
