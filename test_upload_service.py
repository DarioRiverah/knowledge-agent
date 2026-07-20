from src.services.upload_service import UploadService


def main():

    service = UploadService()

    chunks = service.upload(
        "data/uploads/politica_prueba.txt"
    )

    print(
        f"Chunks agregados: {chunks}"
    )


if __name__ == "__main__":
    main()