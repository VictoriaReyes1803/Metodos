import re
import math
def procesar_funcion(funcion):
    """
    Convierte la función ingresada por el usuario a una forma válida en Python.
    Reemplaza operadores y funciones matemáticas escritas de manera incorrecta.
    """
    if not funcion:
        return None

    funcion = funcion.replace("^", "**")
    funcion = funcion.replace("−", "-")
    funcion = re.sub(r'(\d)([a-zA-Z])', r'\1*\2', funcion)

    reemplazos = {
        "ln(": "log(",  
        "tgh(": "tanh(", 
        "exp(": "E**(",  
        "e**": "E**",
        "cos(": "cos(", 
        "sen(": "sin(",  
        "sin(": "sin(",  
        "tan(": "tan(",  
        "arcotangente(": "atan(",
        "acos(": "acos(", 
        "asin(": "asin(",  
        "atan(": "atan(",
        "y'":"yp",
    }
    
    for viejo, nuevo in reemplazos.items():
        funcion = funcion.replace(viejo, nuevo)

    if "=" in funcion:
        partes = funcion.split("=")
        izquierda = partes[0].strip()
        derecha = partes[1].strip()
        funcion = f"({izquierda}) - ({derecha})"

    return funcion
