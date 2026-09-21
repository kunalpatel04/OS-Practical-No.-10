import random

MAX_REQUESTS = 100
TOTAL_CYLINDERS = 200
TOTAL_BLOCKS = 16
BLOCK_SIZE = 32
MAX_FILENAME = 32

class DirectoryEntry:
    def __init__(self, filename="", start_block=0, length=0, is_used=False):
        self.filename = filename
        self.start_block = start_block
        self.length = length
        self.is_used = is_used

class SimpleFileSystem:
    def __init__(self):
        self.disk = ["" for _ in range(TOTAL_BLOCKS)]
        self.bit_map = [0] * TOTAL_BLOCKS
        self.directory = [DirectoryEntry() for _ in range(TOTAL_BLOCKS)]

def fcfs(req, n, head):
    current = head
    total_movement = 0
    seq = [current]

    for i in range(n):
        total_movement += abs(req[i] - current)
        current = req[i]
        seq.append(current)

    print(f"{'FCFS':<10} | {total_movement:<18} | {seq}")

def sstf(req, n, head):
    current = head
    total_movement = 0
    visited = [False] * n
    seq = [current]

    for _ in range(n):
        min_dist = 10000
        nearest_idx = -1

        for j in range(n):
            if not visited[j]:
                dist = abs(req[j] - current)
                if dist < min_dist:
                    min_dist = dist
                    nearest_idx = j

        visited[nearest_idx] = True
        total_movement += min_dist
        current = req[nearest_idx]
        seq.append(current)

    print(f"{'SSTF':<10} | {total_movement:<18} | {seq}")

def c_scan(req, n, head):
    current = head
    total_movement = 0
    seq = [current]

    left = sorted([x for x in req if x < current])
    right = sorted([x for x in req if x >= current])

    for r in right:
        total_movement += abs(r - current)
        current = r
        seq.append(current)

    if left:
        total_movement += abs((TOTAL_CYLINDERS - 1) - current)
        current = TOTAL_CYLINDERS - 1
        seq.append(current)

        total_movement += (TOTAL_CYLINDERS - 1)
        current = 0
        seq.append(current)

        for l in left:
            total_movement += abs(l - current)
            current = l
            seq.append(current)

    print(f"{'C-SCAN':<10} | {total_movement:<18} | {seq}")

def c_look(req, n, head):
    current = head
    total_movement = 0
    seq = [current]

    left = sorted([x for x in req if x < current])
    right = sorted([x for x in req if x >= current])

    for r in right:
        total_movement += abs(r - current)
        current = r
        seq.append(current)

    if left:
        total_movement += abs(left[0] - current)
        current = left[0]
        seq.append(current)

        for l in left[1:]:
            total_movement += abs(l - current)
            current = l
            seq.append(current)

    print(f"{'C-LOOK':<10} | {total_movement:<18} | {seq}")

def rss(req, n, head):
    current = head
    total_movement = 0
    pending = req.copy()
    random.shuffle(pending)
    seq = [current]

    for p in pending:
        total_movement += abs(p - current)
        current = p
        seq.append(current)

    print(f"{'RSS':<10} | {total_movement:<18} | {seq}")

def find_free_blocks(fs, count):
    consecutive = 0
    start_index = -1

    for i in range(TOTAL_BLOCKS):
        if not fs.bit_map[i]:
            if consecutive == 0:
                start_index = i
            consecutive += 1
            if consecutive == count:
                return start_index
        else:
            consecutive = 0
            start_index = -1
    return -1

def create_file(fs, filename, data):
    for entry in fs.directory:
        if entry.is_used and entry.filename == filename:
            print(f"[FS Error] File '{filename}' already exists.")
            return False

    num_blocks = (len(data) + BLOCK_SIZE - 1) // BLOCK_SIZE
    if num_blocks == 0:
        num_blocks = 1

    start_block = find_free_blocks(fs, num_blocks)
    if start_block == -1:
        print(f"[FS Error] Not enough contiguous free blocks for '{filename}'.")
        return False

    for i in range(num_blocks):
        block_idx = start_block + i
        fs.bit_map[block_idx] = 1
        fs.disk[block_idx] = data[i * BLOCK_SIZE : (i + 1) * BLOCK_SIZE]

    for entry in fs.directory:
        if not entry.is_used:
            entry.filename = filename
            entry.start_block = start_block
            entry.length = num_blocks
            entry.is_used = True
            break

    print(f"[FS Success] File '{filename}' created at Block {start_block} (Blocks used: {num_blocks}).")
    return True

def read_file(fs, filename):
    for entry in fs.directory:
        if entry.is_used and entry.filename == filename:
            content = "".join(fs.disk[entry.start_block : entry.start_block + entry.length])
            print(f"Reading '{filename}':\n -> \"{content}\"\n")
            return
    print(f"[FS Error] File '{filename}' not found.")

def delete_file(fs, filename):
    for entry in fs.directory:
        if entry.is_used and entry.filename == filename:
            for i in range(entry.length):
                block_idx = entry.start_block + i
                fs.bit_map[block_idx] = 0
                fs.disk[block_idx] = ""
            entry.is_used = False
            print(f"[FS Success] File '{filename}' deleted successfully.")
            return True
    print(f"[FS Error] File '{filename}' not found.")
    return False

def display_status(fs):
    print("\n--- Directory Status ---")
    empty = True
    for entry in fs.directory:
        if entry.is_used:
            print(f"File: {entry.filename:<12} | Start Block: {entry.start_block:<3} | Length: {entry.length} Block(s)")
            empty = False
    if empty:
        print("Directory is empty.")
    print("------------------------\n")

if __name__ == "__main__":
    print("Aim: Disk Scheduling and Simple File System Design")
    print("Name: Kunal Patel | Roll No: S-101\n")

    print("==========================================")
    print("      PART 1: DISK SCHEDULING SIMULATION  ")
    print("==========================================")

    req_queue = [98, 183, 37, 122, 14, 124, 65, 67]
    initial_head = 53

    print(f"Request Queue: {req_queue}")
    print(f"Initial Head Position: {initial_head}\n")

    print(f"{'Algorithm':<10} | {'Total Movement':<18} | Head Sequence")
    print("-" * 75)

    fcfs(req_queue, len(req_queue), initial_head)
    sstf(req_queue, len(req_queue), initial_head)
    c_scan(req_queue, len(req_queue), initial_head)
    c_look(req_queue, len(req_queue), initial_head)
    rss(req_queue, len(req_queue), initial_head)

    print("\n==========================================")
    print("      PART 2: SIMPLE FILE SYSTEM SIMULATOR ")
    print("==========================================")

    fs = SimpleFileSystem()

    create_file(fs, "document.txt", "Operating Systems - Disk Scheduling and File System.")
    create_file(fs, "code.c", 'printf("Hello World");')
    display_status(fs)

    read_file(fs, "document.txt")
    read_file(fs, "code.c")

    delete_file(fs, "document.txt")
    display_status(fs)

    read_file(fs, "document.txt")
