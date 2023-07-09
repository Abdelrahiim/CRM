import nanoid
import secrets ,os

def get_nano_id():
    return nanoid.generate(size = 12)

# ---------------------------------------------------------------
def unique_filename(path):
    
    def _func(instance, filename):
        ext = filename.split('.')[-1]
        new_file_name = f"{secrets.token_hex(10)}.{ext}"
        return os.path.join(path, new_file_name)
    
    return _func