import PyPDF2
import re
def deteccionLatina(texto):
    # Patrones de expresión regular para extraer
    siniestro_pattern = r"siniestro (\d+)"
    nombre_asegurado_pattern = r"nombre asegurado ([a-záéíóúñ\s]+)edad"
    nombre_doctor_pattern = r"médico tratante ([a-z\s]+)\n"
    folio_pattern = r"folio (\d+)"
    monto_pattern = r"\$([0-9]+(?:\.[0-9]+)?)"
    patron_concepto = r"([a-záéíóúñ]+\s+[0-9]+\s+)\$(?P<monto>(?:[1-9]\d*|0)(?:\.\d+)?)"


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
    siniestro_pattern =  r"siniestro: (\d+)\.?\d*"
    nombre_asegurado_pattern = r"nombre del [Pp]aciente: ([A-Za-z\s]+?)(?=[f\n\t\b])"
    nombre_doctor_pattern =  r"médico [Tt]ratante: ([a-záéíóúñ\s]+)\b"
    folio_pattern = r"folio:\s*([A-Za-z\d]+)"
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
    
def deteccionAtlas(texto):
    siniestro_pattern = r"siniestro\s*([^\s\n]+)"
    folio_pattern = r"folio\s*([^\s\n]+)"
    nombre_paciente_patter = r"asegurado afectado\n*([^\n]+)"
    doctor_patter = r"médico tratante\n*([^\n]+)"
    monto_patter =  r"\$[ ]*([1-9][0-9,]+(?:\.[0-9]+)?)"

    siniestro_match = re.search(siniestro_pattern, texto)
    folio_match = re.search(folio_pattern, texto)
    nombre_paciente_match = re.search(nombre_paciente_patter,texto)
    doctor_match = re.search(doctor_patter,texto)
    monto_match = re.findall(monto_patter,texto)

    numero_siniestro = siniestro_match.group(1) if siniestro_match else None
    folio = folio_match.group(1) if folio_match else None
    nombre_paciente = nombre_paciente_match.group(1) if nombre_paciente_match else None
    doctor = doctor_match.group(1) if doctor_match else None

    suma_montos = 0
    if monto_match:
        for monto in monto_match:
            monto = monto.replace(",", "")
            suma_montos += float(monto)

    print("siniestro:", numero_siniestro)
    print("Folio:", folio)
    print("Nombre paciente:", nombre_paciente)
    print("Nombre Doctor:", doctor)
    print("Montos:", len(monto_match))
    print("Monto total:", suma_montos)


def identificarPDF(text):
    atlas_patter = r"seguros atlas"
    latina_patter = r"la latinoamericana"
    monterrey_patter = r"carta de autorizaciónno."

    atlas_match = re.search(atlas_patter,text)
    latina_match = re.search(latina_patter,text)
    monterrey_match = re.search(monterrey_patter,text)
    
    if atlas_match:
        return "atlas"
    elif latina_match:
        return "La Latinoamérica"
    elif monterrey_match:
        return "monterrey"


if(__name__=="__main__"):
    for pdf_path in pdf_paths:
        reader = PyPDF2.PdfReader(pdf_path)
        texto = reader.pages[0].extract_text().lower()
        tipo = identificarPDF(texto)
        print(pdf_path)
        #print(texto)
        if(tipo == "monterrey" ):
            deteccionMonterrey(texto)
        elif (tipo == "La Latinoamérica"):
            deteccionLatina(texto)
        elif (tipo == "atlas"):
            deteccionAtlas(texto)
        print("")
        