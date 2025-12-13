import pytest
from uuid import UUID, uuid4
from datetime import datetime
from unittest.mock import Mock, patch
import requests


# Модели для тестирования
class Material:
    def __init__(self, id: UUID, title: str, filename: str):
        self.id = id
        self.title = title
        self.filename = filename
        self.uploaded_at = datetime.now()

    @classmethod
    def model_validate(cls, data):
        """Метод для валидации данных, аналогичный Pydantic"""
        return cls(
            id=UUID(data["id"]),
            title=data["title"],
            filename=data["filename"]
        )


# Фикстуры для тестовых данных
@pytest.fixture(scope='session')
def first_material_data() -> tuple[UUID, str, str]:
    return uuid4(), "Алгебра 7 класс", "algebra7.pdf"


@pytest.fixture(scope='session')
def second_material_data() -> tuple[UUID, str, str]:
    return uuid4(), "Геометрия 9 класс", "geometry9.pdf"


@pytest.fixture
def mock_requests():
    """Фикстура для мокирования requests"""
    with patch('requests.get') as mock_get, \
         patch('requests.post') as mock_post, \
         patch('requests.delete') as mock_delete:
        yield mock_get, mock_post, mock_delete


@pytest.fixture
def base_url():
    """Базовый URL для API"""
    return "http://localhost:8000/api"


class TestMaterialsService:
    """Тесты для сервиса учебных материалов"""

    def test_get_materials_empty(self, mock_requests, base_url):
        """Тест на пустоту списка материалов при старте работы"""
        # Дано
        mock_get, _, _ = mock_requests
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = []
        
        # Когда
        response = requests.get(f"{base_url}/materials")
        
        # Тогда
        assert response.status_code == 200
        assert response.json() == []
        mock_get.assert_called_once_with(f"{base_url}/materials")

    def test_create_material_success(self, mock_requests, base_url, first_material_data):
        """Тест - Загрузка нового учебного материала (PDF)"""
        # Дано
        material_id, title, filename = first_material_data
        mock_get, mock_post, _ = mock_requests
        
        expected_response = {
            "id": str(material_id),
            "title": title,
            "filename": filename,
            "uploaded_at": datetime.now().isoformat()
        }
        
        mock_post.return_value.status_code = 201
        mock_post.return_value.json.return_value = expected_response
        
        # Когда
        response = requests.post(
            f"{base_url}/materials",
            json={
                "id": str(material_id),
                "title": title,
                "filename": filename
            }
        )
        
        
        
        # Тогда
        material = Material.model_validate(response.json())
        
        assert response.status_code == 201
        assert material.id == material_id
        assert material.title == title
        assert material.filename == filename
        mock_post.assert_called_once_with(
            f"{base_url}/materials",
            json={
                "id": str(material_id),
                "title": title,
                "filename": filename
            }
        )

    def test_get_material_success(self, mock_requests, base_url, first_material_data):
        """Тест - получение информации о загруженном материале"""
        # Дано
        material_id, title, filename = first_material_data
        mock_get, _, _ = mock_requests
        
        expected_response = {
            "id": str(material_id),
            "title": title,
            "filename": filename,
            "uploaded_at": datetime.now().isoformat()
        }
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_response
        
        # Когда
        response = requests.get(f"{base_url}/materials/{material_id}")
        
        # Тогда
        material = Material.model_validate(response.json())
        
        assert response.status_code == 200
        assert material.id == material_id
        assert material.title == title
        assert material.filename == filename
        mock_get.assert_called_once_with(f"{base_url}/materials/{material_id}")

    def test_download_material_success(self, mock_requests, base_url, first_material_data):
        """Тест на скачивание PDF-файла"""
        # Дано
        material_id, _, _ = first_material_data
        mock_get, _, _ = mock_requests
        
        # Создаем mock PDF контент
        mock_pdf_content = b"%PDF-1.4 fake pdf content for testing"
        
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.headers = {"Content-Type": "application/pdf"}
        mock_response.content = mock_pdf_content
        mock_get.return_value = mock_response
        
        # Когда
        response = requests.get(f"{base_url}/materials/{material_id}/download")
        
        # Тогда
        assert response.status_code == 200
        assert response.headers["Content-Type"] == "application/pdf"
        assert len(response.content) > 10  # PDF не может быть пустым
        assert response.content == mock_pdf_content
        mock_get.assert_called_once_with(f"{base_url}/materials/{material_id}/download")

    def test_delete_material_success(self, mock_requests, base_url, first_material_data):
        """Тест на удаление материалов"""
        # Дано
        material_id, _, _ = first_material_data
        _, _, mock_delete = mock_requests
        
        mock_delete.return_value.status_code = 204
        
        # Когда
        response = requests.delete(f"{base_url}/materials/{material_id}")
        
        # Тогда
        assert response.status_code == 204
        mock_delete.assert_called_once_with(f"{base_url}/materials/{material_id}")

    def test_get_material_not_found(self, mock_requests, base_url):
        """Тест на получение несуществующего материала"""
        # Дано
        material_id = uuid4()
        mock_get, _, _ = mock_requests
        
        mock_get.return_value.status_code = 404
        mock_get.return_value.json.return_value = {"detail": "Material not found"}
        
        # Когда
        response = requests.get(f"{base_url}/materials/{material_id}")
        
        # Тогда
        assert response.status_code == 404
        mock_get.assert_called_once_with(f"{base_url}/materials/{material_id}")

    def test_create_material_validation_error(self, mock_requests, base_url):
        """Тест на ошибку валидации при создании материала"""
        # Дано
        mock_get, mock_post, _ = mock_requests
        
        invalid_data = {
            "id": "invalid-uuid",  # Невалидный UUID
            "title": "",  # Пустой заголовок
            "filename": "test.pdf"
        }
        
        mock_post.return_value.status_code = 422
        mock_post.return_value.json.return_value = {
            "detail": "Validation error"
        }
        
        # Когда
        response = requests.post(f"{base_url}/materials", json=invalid_data)
        
        # Тогда
        assert response.status_code == 422
        mock_post.assert_called_once_with(f"{base_url}/materials", json=invalid_data)

    def test_get_materials_with_data(self, mock_requests, base_url, first_material_data, second_material_data):
        """Тест на получение списка материалов с данными"""
        # Дано
        material_id1, title1, filename1 = first_material_data
        material_id2, title2, filename2 = second_material_data
        mock_get, _, _ = mock_requests
        
        expected_response = [
            {
                "id": str(material_id1),
                "title": title1,
                "filename": filename1,
                "uploaded_at": datetime.now().isoformat()
            },
            {
                "id": str(material_id2),
                "title": title2,
                "filename": filename2,
                "uploaded_at": datetime.now().isoformat()
            }
        ]
        
        mock_get.return_value.status_code = 200
        mock_get.return_value.json.return_value = expected_response
        
        # Когда
        response = requests.get(f"{base_url}/materials")
        
        # Тогда
        assert response.status_code == 200
        materials = response.json()
        assert len(materials) == 2
        assert materials[0]["title"] == title1
        assert materials[1]["title"] == title2
        mock_get.assert_called_once_with(f"{base_url}/materials")