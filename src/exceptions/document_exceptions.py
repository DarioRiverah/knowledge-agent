class UnsupportedDocumentError(Exception):
    """
    Se lanza cuando se intenta cargar
    un formato no soportado.
    """

    pass


class DocumentAlreadyExistsError(Exception):
    """
    Se lanza cuando un documento ya existe
    en la base de conocimiento.
    """

    pass