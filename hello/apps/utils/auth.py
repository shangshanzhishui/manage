import time
import hashlib




def create_token(email):
    ctime = int(time.time())
    localTime = time.localtime(ctime)
    ctime = time.strftime("%Y%m%d%H%M", localTime)
    key = "xiaomi"
    need_data = key + str(ctime) + email
    h1 = hashlib.md5()
    h1.update(need_data.encode("utf-8"))
    token = h1.hexdigest()
    return token