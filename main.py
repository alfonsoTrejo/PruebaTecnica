import PyPDF2
import re
def deteccionLatina(texto):
    # Patrones de expresión regular para extraer
    siniestro_pattern = r"SINIESTRO (\d+)"
    nombre_asegurado_pattern = r"NOMBRE ASEGURADO ([A-ZÁÉÍÓÚÑ\s]+)EDAD"
    nombre_doctor_pattern = r"MÉDICO TRATANTE ([A-Z\s]+)\n"
    folio_pattern = r"FOLIO (\d+)"
    monto_pattern = r"\$([0-9]+(?:\.[0-9]+)?)"
    patron_concepto = r"([A-ZÁÉÍÓÚÑ]+\s+[0-9]+\s+)\$(?P<monto>(?:[1-9]\d*|0)(?:\.\d+)?)"


    # Buscar coincidencias de los patrones en el texto
    siniestro_match = re.search(siniestro_pattern, texto)
    nombre_asegurado_match = re.search(nombre_asegurado_pattern, texto)
    nombre_doctor_match = re.search(nombre_doctor_pattern, texto)
    folio_match = re.search(folio_pattern, texto)
    monto_match = re.findall(monto_pattern, texto)
    concepto_match = re.findall(patron_concepto, texto)
    # Extraer el número de siniestro y el nombre del asegurado si se encuentran
    numero_siniestro = siniestro_match.group(1) if siniestro_match else None
    nombre_asegurado = nombre_asegurado_match.group(1) if nombre_asegurado_match else None
    nombre_doctor = nombre_doctor_match.group(1) if nombre_doctor_match else None
    folio = folio_match.group(1) if folio_match else None
    suma_montos = sum(float(monto.replace(',', '')) for monto in monto_match)
    conceptos_con_monto_mayor_a_cero = [concepto for concepto, monto in concepto_match if float(monto) > 0]

    cantidad_conceptos = len(conceptos_con_monto_mayor_a_cero)


    # Imprimir los resultados
    print("Número de Siniestro:", numero_siniestro)
    print("Nombre del Asegurado:", nombre_asegurado)
    print("Nombre del Doctor:", nombre_doctor)
    print("Folio:", folio)
    print("Montos:", cantidad_conceptos)
    print("Monto Total:", suma_montos)

def deteccionMonterrey(texto):
    siniestro_pattern =  r"Siniestro: (\d+)\.?\d*"
    nombre_asegurado_pattern = r"Nombre del [Pp]aciente: ([A-Za-z\s]+?)(?=[F\n\t\b])"
    nombre_doctor_pattern =  r"Médico [Tt]ratante: ([A-ZÁÉÍÓÚÑ\s]+)\b"
    folio_pattern = r"Folio:\s*([A-Za-z\d]+)"
    monto_pattern =  r"\s+([\w\s]+)\s+\$([\d,]+\.\d{2})\s+([\w\s]+)"

    siniestro_match = re.search(siniestro_pattern, texto)
    nombre_asegurado_match =re.search(nombre_asegurado_pattern,texto)
    nombre_doctor_match = re.search(nombre_doctor_pattern,texto)
    monton_match = re.findall(monto_pattern,texto)
    folio_match = re.search(folio_pattern,texto)

    numero_siniestro = siniestro_match.group(1) if siniestro_match else None
    nombre_asegurado = nombre_asegurado_match.group(1) if nombre_asegurado_match else None
    nombre_doctor = nombre_doctor_match.group(1) if nombre_doctor_match else None
    folio = folio_match.group(1) if folio_match else None
    montos = len(monton_match)
    suma_montos = sum(float(monto.replace(',', '')) for (_, monto, _) in monton_match)

    print("Número de Siniestro:", numero_siniestro)
    print("Número del paciente:", nombre_asegurado)
    print("Número del Doctor:", nombre_doctor.strip())
    print("Folio:", folio)
    print("Montos: ", montos)
    print("Monto Total: ", suma_montos)
    
    

def identificarPDF(text):
    if text.startswith("Carta de Autorización"):
        return "Seguros Monterrey"
    elif text.startswith("LA LATINOAMERICANA, SEGUROS,  SA - HOJA DE  PROGRAMACIÓN"):
        return "La Latinoamérica"
    else:
        return "Atlas"


if(__name__=="__main__"):
    for pdf_path in pdf_paths:
        reader = PyPDF2.PdfReader(pdf_path)
        texto = reader.pages[0].extract_text()
        tipo = identificarPDF(texto)
        if(tipo == "Seguros Monterrey" ):
            deteccionMonterrey(texto)
        elif (tipo == "La Latinoamérica"):
            deteccionLatina(texto)
        print("")
        