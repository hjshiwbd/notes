import hashlib

def md5sum(filename):
    file_object = open(filename, 'rb')
    file_content = file_object.read()
    file_object.close()
    file_md5 = hashlib.md5(file_content)
    return file_md5

# s = "yuzHi0518#"
# s = "Qwer1234!"
# s = "UAQNq4q1l79YpdumUhFq4AakqQUqiIg9"
# Qwer1234! ad6cdcad4e7622512dc122aaeacc6e6b
s="""
Qwer1234!
""".strip()
s2 = hashlib.md5(s.encode(encoding='UTF-8')).hexdigest()

print(s2)

# s3 = md5sum("D:\\git\\yuzhi\\lltt-app-parent\\lltt-app-pc\\target\\lltt_pc.jar")

# print(s3.hexdigest())

