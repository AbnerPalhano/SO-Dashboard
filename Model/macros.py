import ctypes

########## -------- CONSTANTES E MACROS -------- ##########
# Macros pegos de stat.h do kernel linux:
# https://github.com/torvalds/linux/blob/14d7c92f8df9c0964ae6f8b813c1b3ac38120825/include/uapi/linux/stat.h#L152
# alguns comentarios foram pegos da documentação de statx:
# https://manpages.debian.org/unstable/manpages-dev/statx.2.en.html
STATX_TYPE = 0x00000001  # want stx_mode & S_IFMT
STATX_MODE = 0x00000002  # want stx_mode & ~S_IFMT
STATX_NLINK = 0x00000004  # want stx_nlink
STATX_UID = 0x00000008  # want stx_uid
STATX_GID = 0x00000010  # want stx_gid
STATX_ATIME = 0x00000020  # want stx_atime
STATX_MTIME = 0x00000040  # want stx_mtime
STATX_CTIME = 0x00000080  # want stx_ctime
STATX_INO = 0x00000100  # want stx_ino
STATX_SIZE = 0x00000200  # want stx_size
STATX_BLOCKS = 0x00000400  # want stx_blocks
STATX_BASIC_STATS = 0x000007FF  # [all of the above]
STATX_BTIME = 0x00000800  # want stx_btime
STATX_MNT_ID = 0x00001000  # want stx_mnt_id
STATX_DIOALIGN = 0x00002000  # want stx_dio_align and stx_dio_offset_align
STATX_MNT_ID_UNIQUE = 0x00004000  # want extended stx_mnt_id
STATX_SUBVOL = 0x00008000  # want stx_subvol
STAT__RESERVED = 0x80000000  # reserved for future struct statx expansion

S_IFMT = 0o170000  # Bit mask for the file type bit field
S_IFSOCK = 0o140000  # Socket
S_IFLNK = 0o120000  # Symbolic link
S_IFREG = 0o100000  # Regular file
S_IFBLK = 0o060000  # Block device
S_IFDIR = 0o040000  # Directory
S_IFCHR = 0o020000  # Character device
S_IFIFO = 0o010000  # FIFO

S_ISUID = 0o004000  # Set-user-ID bit
S_ISGID = 0o002000  # Set-group-ID bit
S_ISVTX = 0o001000  # Sticky bit


def S_ISLNK(m):
    return (m & S_IFMT) == S_IFLNK


def S_ISREG(m):
    return (m & S_IFMT) == S_IFREG


def S_ISDIR(m):
    return (m & S_IFMT) == S_IFDIR


def S_ISCHR(m):
    return (m & S_IFMT) == S_IFCHR


def S_ISBLK(m):
    return (m & S_IFMT) == S_IFBLK


def S_ISFIFO(m):
    return (m & S_IFMT) == S_IFIFO


def S_ISSOCK(m):
    return (m & S_IFMT) == S_IFSOCK


# Permissions
S_IRWXU = 0o700  # Mask for file owner permissions (read, write, execute)
S_IRUSR = 0o400  # Owner has read permission
S_IWUSR = 0o200  # Owner has write permission
S_IXUSR = 0o100  # Owner has execute permission

S_IRWXG = 0o070  # Mask for group permissions (read, write, execute)
S_IRGRP = 0o040  # Group has read permission
S_IWGRP = 0o020  # Group has write permission
S_IXGRP = 0o010  # Group has execute permission

S_IRWXO = 0o007  # Mask for others permissions (read, write, execute)
S_IROTH = 0o004  # Others have read permission
S_IWOTH = 0o002  # Others have write permission
S_IXOTH = 0o001  # Others have execute permission


STATX_ATTR_COMPRESSED = 0x00000004  # File is compressed by the filesystem
STATX_ATTR_IMMUTABLE = 0x00000010  # File is marked immutable
STATX_ATTR_APPEND = 0x00000020  # File is append-only
STATX_ATTR_NODUMP = 0x00000040  # File is not to be dumped
STATX_ATTR_ENCRYPTED = 0x00000800  # File requires key to decrypt in filesystem
STATX_ATTR_AUTOMOUNT = 0x00001000  # Directory: Automount trigger
STATX_ATTR_MOUNT_ROOT = 0x00002000  # Root of a mount
STATX_ATTR_VERITY = 0x00100000  # Verity protected file
STATX_ATTR_DAX = 0x00200000  # File is currently in DAX state
###########################################################

mask = (
    STATX_TYPE
    | STATX_MODE
    | STATX_NLINK
    | STATX_UID
    | STATX_GID
    | STATX_ATIME
    | STATX_MTIME
    | STATX_CTIME
    | STATX_INO
    | STATX_SIZE
    | STATX_BLOCKS
    | STATX_BASIC_STATS
    | STATX_BTIME
    | STATX_MNT_ID
    | STATX_DIOALIGN
)


# definição da estrutura de dados que statx retorna dos arquivos,
# contendo informações sobre o arquivo
class statx_timestamp(ctypes.Structure):
    _fields_ = [
        ("tv_sec", ctypes.c_int64),  # Seconds since the Epoch (UNIX time)
        ("tv_nsec", ctypes.c_uint32),  # Nanoseconds since tv_sec
        ("__reserved", ctypes.c_int32),  # Reserved for future expansion
    ]


# struct de statx
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
        ("__spare3", ctypes.c_uint64 * 11),
    ]
