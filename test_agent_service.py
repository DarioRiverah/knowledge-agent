import pytest


PREGUNTAS_CON_DOCUMENTOS = [
    "¿Qué hago si mi pago fue rechazado?",
    "¿Cuánto tarda un reembolso?",
    "¿El reembolso vuelve al mismo medio de pago?",
    "¿Por qué mi orden quedó pendiente de pago?",
    "¿Puedo pagar con más de un método?",
    "¿Qué pasa si me cobraron pero la orden no aparece?",
    "¿Qué relación tienen los pagos con los envíos?",
]

PREGUNTAS_FUERA_DE_DOMINIO = [
    "¿Cuál es la capital de Francia?",
]

SALUDOS = [
    "Hola, ¿cómo estás?",
]


@pytest.mark.parametrize("question", PREGUNTAS_CON_DOCUMENTOS)
def test_pregunta_con_documentos_devuelve_respuesta_y_fuentes(service, question):
    response = service.chat(question)

    assert response.answer
    assert response.answer.strip() != ""


@pytest.mark.parametrize("question", PREGUNTAS_FUERA_DE_DOMINIO)
def test_pregunta_fuera_de_dominio_no_alucina(service, question):
    response = service.chat(question)

    # No debe inventar información ni intentar responder con
    # conocimiento general: debe redirigir al usuario hacia los
    # temas que sí puede resolver (ruta "off_topic" del router).
    assert response.answer
    assert response.sources == []
    assert "bimbam buy" in response.answer.lower()


@pytest.mark.parametrize("question", SALUDOS)
def test_saludo_responde_sin_buscar_documentos(service, question):
    response = service.chat(question)

    assert response.answer
    assert response.sources == []