# tests/test_app.py
import pytest
from app.app import app


@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_index_get(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.data


@pytest.mark.parametrize(
    "operacion, num1, num2, esperado",
    [
        pytest.param("sumar", "2", "3", b"Resultado: 5.0", id="sumar"),
        pytest.param("restar", "5", "3", b"Resultado: 2.0", id="restar"),
        pytest.param("multiplicar", "2", "3", b"Resultado: 6.0", id="multiplicar"),
        pytest.param("dividir", "6", "3", b"Resultado: 2.0", id="dividir"),
        pytest.param("potencia", "2", "3", b"Resultado: 8.0", id="potencia"),
        pytest.param("modulo", "7", "3", b"Resultado: 1.0", id="modulo"),
    ],
)
def test_index_post_operaciones(client, operacion, num1, num2, esperado):
    response = client.post(
        "/", data={"num1": num1, "num2": num2, "operacion": operacion}
    )
    assert response.status_code == 200
    assert esperado in response.data


def test_index_post_dividir_by_zero(client):
    response = client.post("/", data={"num1": "6", "num2": "0", "operacion": "dividir"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_modulo_by_zero(client):
    response = client.post("/", data={"num1": "5", "num2": "0", "operacion": "modulo"})
    assert response.status_code == 200
    assert b"Error: No se puede dividir por cero" in response.data


def test_index_post_potencia_overflow(client):
    response = client.post(
        "/", data={"num1": "10", "num2": "1000", "operacion": "potencia"}
    )
    assert response.status_code == 200
    assert b"Error: El resultado es demasiado grande" in response.data


def test_index_post_potencia_no_real(client):
    response = client.post(
        "/", data={"num1": "-8", "num2": "0.5", "operacion": "potencia"}
    )
    assert response.status_code == 200
    assert "Error: El resultado no es un número real".encode() in response.data


def test_index_post_invalid_operation(client):
    response = client.post("/", data={"num1": "6", "num2": "3", "operacion": "invalid"})
    assert response.status_code == 200
    assert b"Operaci\xc3\xb3n no v\xc3\xa1lida" in response.data


def test_index_post_invalid_numbers(client):
    response = client.post("/", data={"num1": "a", "num2": "b", "operacion": "sumar"})
    assert response.status_code == 200
    assert b"Error: Introduce n\xc3\xbameros v\xc3\xa1lidos" in response.data


def test_index_post_valid_first_invalid_second_number(client):
    response = client.post("/", data={"num1": "2", "num2": "abc", "operacion": "sumar"})
    assert response.status_code == 200
    assert b"Error: Introduce n\xc3\xbameros v\xc3\xa1lidos" in response.data


def test_health(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok", "version": "local"}
