import os
import zipfile
import subprocess
import shutil
from mhg_dl.logger import log

def pack_zip(download_dir: str, ext: str) -> None:
    for entry in os.scandir(download_dir):
        if not entry.is_dir():
            continue
        type_dir = entry.path
        for chapter_entry in os.scandir(type_dir):
            if not chapter_entry.is_dir():
                continue
            chapter_dir = chapter_entry.path
            archive_path = chapter_dir + f".{ext}"
            log.info(f"Packing {chapter_entry.name} -> {os.path.basename(archive_path)}")
            with zipfile.ZipFile(archive_path, "w", zipfile.ZIP_DEFLATED) as zf:
                for file in sorted(os.listdir(chapter_dir)):
                    file_path = os.path.join(chapter_dir, file)
                    if os.path.isfile(file_path):
                        zf.write(file_path, arcname=file)
            shutil.rmtree(chapter_dir)


def pack_rar(download_dir: str, ext: str) -> None:
    rar_bin = _find_rar_bin()
    if rar_bin is None:
        log.error("RAR not found. Please install RAR!")
        return

    for entry in os.scandir(download_dir):
        if not entry.is_dir():
            continue
        type_dir = entry.path
        for chapter_entry in os.scandir(type_dir):
            if not chapter_entry.is_dir():
                continue
            chapter_dir = chapter_entry.path
            archive_path = chapter_dir + f".{ext}"
            log.info(f"Packing {chapter_entry.name} -> {os.path.basename(archive_path)}")
            cmd = [rar_bin, "a", "-ep", archive_path, os.path.join(chapter_dir, "*")]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode != 0:
                log.error(f"rar failed for {chapter_entry.name}: {result.stderr.strip()}")
            else:
                shutil.rmtree(chapter_dir)


def _find_rar_bin() -> str | None:
    rar = shutil.which("rar")
    if rar:
        return rar
    return None
