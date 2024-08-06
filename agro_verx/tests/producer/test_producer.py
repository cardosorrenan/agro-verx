import pytest
from django.urls import reverse
from rest_framework import status

from agro_verx.producer.models import ProducerModel


@pytest.mark.django_db
class TestProducerViewset:
    def test_list_producers(self, api_client):
        url = reverse('producermodel-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_create_producer(self, api_client, producer_data):
        url = reverse('producermodel-list')
        response = api_client.post(url, producer_data)
        assert response.status_code == status.HTTP_201_CREATED
        assert ProducerModel.objects.count() == 11
        assert (
            ProducerModel.objects.last().producer_name
            == producer_data['producer_name']
        )

    def test_retrieve_producer(
        self, api_client, producer_data, create_producer
    ):
        producer = create_producer(**producer_data)
        url = reverse(
            'producermodel-detail', kwargs={'pk': producer.producer_id}
        )
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['producer_name'] == producer.producer_name

    def test_update_producer(self, api_client, producer_data, create_producer):
        producer = create_producer(**producer_data)
        url = reverse(
            'producermodel-detail', kwargs={'pk': producer.producer_id}
        )
        updated_data = {'producer_name': 'Change Name Producer'}
        response = api_client.patch(url, updated_data)
        assert response.status_code == status.HTTP_200_OK
        assert (
            ProducerModel.objects.get(
                producer_id=producer.producer_id
            ).producer_name
            == 'Change Name Producer'
        )

    def test_delete_producer(self, api_client, producer_data, create_producer):
        producer = create_producer(**producer_data)
        url = reverse(
            'producermodel-detail', kwargs={'pk': producer.producer_id}
        )
        response = api_client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert ProducerModel.objects.filter(is_deleted=True).count() == 0
        assert ProducerModel.all_objects.filter(is_deleted=True).count() == 1

    def test_restore_producer(
        self, api_client, producer_data, create_producer
    ):
        producer = create_producer(**producer_data)
        url = reverse(
            'producermodel-restore', kwargs={'pk': producer.producer_id}
        )
        response = api_client.patch(url)
        assert response.status_code == status.HTTP_200_OK
        assert ProducerModel.objects.filter(is_deleted=True).count() == 0

    def test_restore_non_existent_producer(self, api_client):
        url = reverse('producermodel-restore', kwargs={'pk': 999})
        response = api_client.patch(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_invalid_cpf_number(self, api_client):
        url = reverse('producermodel-list')
        invalid_data = {
            'producer_name': 'Invalid CPF Producer',
            'producer_document_type': 'CPF',
            'producer_cpf_number': '123.456.789-1',  # Invalid CPF
        }
        response = api_client.post(url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'producer_cpf_number' in response.data
        assert (
            str(response.data['producer_cpf_number'][0])
            == 'CPF must be exactly 14 characters long.'
        )

    def test_invalid_cnpj_number(self, producer_data, api_client):
        url = reverse('producermodel-list')
        invalid_data = {
            'producer_name': 'Invalid CNPJ Producer',
            'producer_document_type': 'CNPJ',
            'producer_cnpj_number': '12.345.678/901-34',  # Invalid CNPJ
        }
        response = api_client.post(url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'producer_cnpj_number' in response.data
        assert (
            str(response.data['producer_cnpj_number'][0])
            == 'CNPJ must be exactly 18 characters long.'
        )

    def test_mismatch_cpf_type_cnpj_number(self, api_client):
        url = reverse('producermodel-list')
        invalid_data = {
            'producer_name': 'Invalid CPF Producer',
            'producer_document_type': 'CPF',
            'producer_cnpj_number': '12.345.678/9012-34',
        }
        response = api_client.post(url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'producer_cpf_number' in response.data
        assert (
            str(response.data['producer_cpf_number'][0])
            == "CPF number mustn't be empty."
        )

    def test_mismatch_cnpj_type_cpf_number(self, producer_data, api_client):
        url = reverse('producermodel-list')
        invalid_data = {
            'producer_name': 'Invalid CNPJ Producer',
            'producer_document_type': 'CNPJ',
            'producer_cpf_number': '123.456.789-12',  # Invalid CNPJ
        }
        response = api_client.post(url, invalid_data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        assert 'producer_cnpj_number' in response.data
        assert (
            str(response.data['producer_cnpj_number'][0])
            == "CNPJ number mustn't be empty."
        )
