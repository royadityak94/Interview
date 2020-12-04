def mmap_io_find_and_replace(filename):
    with open(filename, mode="r+", encoding="utf-8") as file_obj:
        with mmap.mmap(file_obj.fileno(), length=0, access=mmap.ACCESS_WRITE) as mmap_obj:
            orig_text = mmap_obj.read()
            new_text = orig_text.replace(b" the ", b" eht ")
            mmap_obj[:] = new_text
            mmap_obj.flush()
