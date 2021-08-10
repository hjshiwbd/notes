from faker import Faker
fake = Faker("zh_cn")
for _ in range(10):
    print(fake.ssn())