import random

from faker import Faker

fake = Faker()


def generate_code(document_type):
    if document_type == 'CNPJ':
        return f'{random.randint(10, 99):02}.{random.randint(100, 999):03}.{random.randint(100, 999):03}/{random.randint(1000, 9999):04}-{random.randint(10, 99):02}'
    elif document_type == 'CPF':
        return f'{random.randint(100, 999):03}.{random.randint(100, 999):03}.{random.randint(100, 999):03}-{random.randint(10, 99):02}'
    else:
        return None


def generate_producer_data():
    document_type = random.choice(['CPF', 'CNPJ'])
    code = generate_code(document_type)
    if document_type == 'CPF':
        cpf_number = code
        cnpj_number = ''
    else:
        cpf_number = ''
        cnpj_number = code

    return {
        'producer_name': fake.company(),
        'producer_document_type': document_type,
        'producer_cpf_number': cpf_number,
        'producer_cnpj_number': cnpj_number,
    }
