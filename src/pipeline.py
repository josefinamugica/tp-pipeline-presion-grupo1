
import re
from src.modelo import Paciente

PATRON_CODIGO = re.compile(r"PAC-\d{3}")

def convertir_numero(valor):
    if valor is None:
        return None

    if isinstance(valor, str) and valor.strip() == "":
        return None

    return float(valor)

RANGOS = {
    "edad": (18, 100),
    "imc": (10, 60),
    "presion_sistolica": (60, 250)
}

GRUPOS_VALIDOS = {"A", "B"}


def validar_registro(registro):
    motivos = []

    codigo = registro.get("codigo")
    if not isinstance(codigo, str) or not PATRON_CODIGO.fullmatch(codigo):
        motivos.append("código con formato inválido")

    for campo, (minimo, maximo) in RANGOS.items():
        try:
            valor = convertir_numero(registro.get(campo))

            if valor is None:
                motivos.append(f"{campo} faltante")
            elif not minimo <= valor <= maximo:
                motivos.append(f"{campo} fuera de rango")

        except (ValueError, TypeError):
            motivos.append(f"{campo} no numérico")

    if registro.get("grupo") not in GRUPOS_VALIDOS:
        motivos.append("grupo inválido")

    return motivos

def limpiar(registros):
    validos = []
    rechazos = []
    codigos_aceptados = set()

    for numero_fila, registro in enumerate(registros, start=1):
        motivos = validar_registro(registro)
        codigo = registro.get("codigo")

        if not motivos and codigo in codigos_aceptados:
            motivos.append("código duplicado")

        if motivos:
            rechazos.append({
                "fila": numero_fila,
                "codigo": codigo,
                "motivo": "; ".join(motivos)
            })
        else:
            paciente = Paciente(
                codigo,
                convertir_numero(registro["edad"]),
                convertir_numero(registro["imc"]),
                convertir_numero(registro["presion_sistolica"]),
                registro["grupo"]
            )

            validos.append(paciente)
            codigos_aceptados.add(codigo)

    return validos, rechazos
