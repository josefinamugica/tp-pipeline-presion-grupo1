
import csv


def generar_reporte(pacientes):
    reporte = []

    grupos = sorted(set(p.grupo for p in pacientes))

    for grupo in grupos:
        pacientes_grupo = [
            p for p in pacientes if p.grupo == grupo
        ]

        cantidad = len(pacientes_grupo)

        presion_media = round(
            sum(p.presion for p in pacientes_grupo) / cantidad, 2
        )

        proporcion = round(
            sum(p.es_hipertenso() for p in pacientes_grupo) / cantidad, 3
        )

        reporte.append({
            "grupo": grupo,
            "cantidad": cantidad,
            "presion_media": presion_media,
            "proporcion_hipertensos": proporcion
        })

    return reporte


def guardar_csv(filas, ruta):
    with open(ruta, "w", newline="", encoding="utf-8") as archivo:
        escritor = csv.DictWriter(
            archivo, fieldnames=list(filas[0].keys())
        )
        escritor.writeheader()
        escritor.writerows(filas)


from pathlib import Path
from src.fuentes import FuenteCSV
from src.pipeline import limpiar

CARPETA_SALIDA = Path("outputs")


def main(ruta_entrada):
    registros = FuenteCSV().cargar(ruta_entrada)
    validos, rechazos = limpiar(registros)
    reporte = generar_reporte(validos)

    print(f"Leídos: {len(registros)} | válidos: {len(validos)} | rechazados: {len(rechazos)}")

    for fila in reporte:
        print(fila)

    CARPETA_SALIDA.mkdir(exist_ok=True)

    guardar_csv(reporte, CARPETA_SALIDA / "reporte.csv")

    if rechazos:
        guardar_csv(rechazos, CARPETA_SALIDA / "rechazos.csv")


if __name__ == "__main__":
    main("data/mediciones.csv")