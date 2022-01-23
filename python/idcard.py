from faker import Faker
fake = Faker("zh_cn")
for _ in range(10):
    print(f'{fake.ssn()}, {fake.name()}, {fake.phone_number()}')