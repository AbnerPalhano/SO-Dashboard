from pathlib import Path
import os
import ctypes
from dataclasses import dataclass
import sys
import Model.macros as macros

# /proc/partitions
# /proc/diskstats
# /proc/ioports
# /proc/iomem
# /sys/block
# inodes - files metadata


# definição da estrutura de dados que statx retorna dos arquivos,
# contendo informações sobre o arquivo
class statx_timestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64),  # Seconds since the Epoch (UNIX time)
        ("tv_nsec", ctypes.c_uint32),  # Nanoseconds since tv_sec
    ]


class statx(ctypes.Structure):
    _fields_ = [
        ("stx_mask", ctypes.c_uint32),  # Mask of bits indicating filled fields
        ("stx_blksize", ctypes.c_uint32),  # Block size for filesystem I/O
        ("stx_attributes", ctypes.c_uint64),  # Extra file attribute indicators
        ("stx_nlink", ctypes.c_uint32),  # Number of hard links
        ("stx_uid", ctypes.c_uint32),  # User ID of owner
        ("stx_gid", ctypes.c_uint32),  # Group ID of owner
        ("stx_mode", ctypes.c_uint16),  # File type and mode
        ("__spare0", ctypes.c_uint16),
        ("stx_ino", ctypes.c_uint64),  # Inode number
        ("stx_size", ctypes.c_uint64),  # Total size in bytes
        ("stx_blocks", ctypes.c_uint64),  # Number of 512B blocks allocated
        (
            "stx_attributes_mask",
            ctypes.c_uint64,
        ),  # Mask to show what's supported in stx_attributes
        # timestamps
        ("stx_atime", statx_timestamp),  # Last access
        ("stx_btime", statx_timestamp),  # Creation
        ("stx_ctime", statx_timestamp),  # Last status change
        ("stx_mtime", statx_timestamp),  # Last data modification
        # If this file represents a device,
        # then the next two fields contain the ID of the device
        ("stx_rdev_major", ctypes.c_uint32),  # Major ID for special device
        ("stx_rdev_minor", ctypes.c_uint32),  # Minor ID for special device
        # The next two fields contain the ID of the device
        # containing the filesystem where the file resides
        ("stx_dev_major", ctypes.c_uint32),  # Major ID
        ("stx_dev_minor", ctypes.c_uint32),  # Minor ID
        ("stx_mnt_id", ctypes.c_uint64),  # ID of mount point
        # Direct I/O alignment restrictions
        (
            "stx_dio_mem_align",
            ctypes.c_uint32,
        ),  # Memory buffer alignment for direct I/O
        (
            "stx_dio_offset_align",
            ctypes.c_uint32,
        ),  # File offset alignment for direct I/O
        ("stx_subvol", ctypes.c_uint64),  # Subvolume identifier
        ("__spare3", ctypes.c_uint64),
    ]


def main():
    try:
        sys.settrace
        libc = ctypes.CDLL("libc.so.6")
        mask = (
            macros.STATX_TYPE
            | macros.STATX_MODE
            | macros.STATX_NLINK
            | macros.STATX_UID
            | macros.STATX_GID
            | macros.STATX_ATIME
            | macros.STATX_MTIME
            | macros.STATX_CTIME
            | macros.STATX_INO
            | macros.STATX_SIZE
            | macros.STATX_BLOCKS
            | macros.STATX_BASIC_STATS
            | macros.STATX_BTIME
            | macros.STATX_MNT_ID
            | macros.STATX_DIOALIGN
        )
        statxbuf = statx()
        filename = "/proc"  # os.getcwd()  # + "/diskInfo.py"
        statx_syscall = 332
        result = libc.syscall(
            statx_syscall, -100, filename, 0, macros.mask, ctypes.byref(statxbuf)
        )
        if result == -1:
            print(f"erro")
            quit(1)
        print(f"'{os.path.basename(filename)}' File/Folder Information:")
        print(f"Device major: {statxbuf.stx_dev_major}")
        print(f"Device minor: {statxbuf.stx_dev_minor}")
        print(f"Inode: {statxbuf.stx_ino}")
        print(f"Mode: {oct(statxbuf.stx_mode)}")
        print(f"Number of hard links: {statxbuf.stx_nlink}")
        print(f"UID: {statxbuf.stx_uid}")
        print(f"GID: {statxbuf.stx_gid}")
        print(f"Size: {statxbuf.stx_size} bytes")
        print(f"Block size: {statxbuf.stx_blksize}")
        print(f"Number of blocks: {statxbuf.stx_blocks}")
        print(f"Last access time: {statxbuf.stx_atime.tv_sec}")
        print(f"Creation time: {statxbuf.stx_btime.tv_sec}")
        print(f"Last modification time: {statxbuf.stx_mtime.tv_sec}")
        print(f"Last status change time: {statxbuf.stx_ctime.tv_sec}")

        return statxbuf
    except MemoryError as e:
        print(f"Error: {e}")
        quit(1)


if __name__ == "__main__":
    main()
