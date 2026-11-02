# -*- coding: utf-8 -*-
"""
Proyecto ACA - Programación Avanzada
Control de gastos personales para estudiantes

Problemática:
    El dinero del mes se acaba y el estudiante no sabe en qué se le fue,
    porque no anota los gastos pequeños del día a día.

Solución:
    Programa en Python que registra ingresos y gastos por categoría,
    muestra el saldo, un resumen de en qué se gasta más y alertas de presupuesto.

CÓMO TRABAJAMOS ESTE ARCHIVO
    - La BASE COMPARTIDA (datos y funciones de apoyo) ya está lista: NO la cambien
      sin avisar al grupo, porque todos la usan.
    - Cada integrante completa SOLO las funciones de sus tickets.
    - Mientras una función no esté hecha, muestra "pendiente" y el programa sigue
      funcionando. Así siempre se puede ejecutar y probar.
"""

import calendar
from datetime import datetime

# =============================================================================
# BASE COMPARTIDA (lista desde el inicio)
# =============================================================================

CATEGORIAS = ["Transporte", "Comida", "Fotocopias", "Entretenimiento", "Otros"]

# Cada movimiento es un diccionario con esta forma:
# {"tipo": "ingreso" o "gasto", "categoria": "Comida" (solo gastos, en ingresos None),
#  "descripcion": "Almuerzo", "valor": 12000, "fecha": "30/10/2026"}
movimientos = []

# Presupuesto mensual para gastos (0 = sin definir). Lo usa el Ticket 3.
presupuesto = 0


def formato_pesos(valor):
    """Convierte un número a pesos colombianos. Ej: 12500 -> $12.500"""
    signo = "-" if valor < 0 else ""
    return signo + "$" + f"{abs(valor):,.0f}".replace(",", ".")


def pedir_valor(mensaje):
    """Pide un valor en pesos mayor que cero. Repite hasta que sea válido."""
    while True:
        texto = input(mensaje).strip().replace(".", "").replace("$", "")
        try:
            valor = int(texto)
            if valor > 0:
                return valor
            print("  ⚠ El valor debe ser mayor que cero.")
        except ValueError:
            print("  ⚠ Escriba solo números, sin letras. Ej: 15000")


def pedir_texto(mensaje):
    """Pide un texto que no esté vacío."""
    while True:
        texto = input(mensaje).strip()
        if texto:
            return texto
        print("  ⚠ Este campo no puede quedar vacío.")


def fecha_hoy():
    return datetime.now().strftime("%d/%m/%Y")


def calcular_totales():
    """Devuelve (total_ingresos, total_gastos, saldo)."""
    ingresos = sum(m["valor"] for m in movimientos if m["tipo"] == "ingreso")
    gastos = sum(m["valor"] for m in movimientos if m["tipo"] == "gasto")
    return ingresos, gastos, ingresos - gastos


def pendiente(ticket, integrante):
    """Muestra un mensaje indicando que la función aún no está programada."""
    print(f"  ⏳ Función pendiente (Ticket {ticket} - {integrante}).")


# =============================================================================
# INTEGRANTE 1 — Tickets 1, 2 y 3
# =============================================================================

def registrar_ingreso():
    """TICKET 1: pedir descripción y valor, y guardar un movimiento tipo 'ingreso'."""
    pendiente(1, "Integrante 1")


def ver_historial():
    """TICKET 2: mostrar todos los movimientos en una tabla
    (número, fecha, tipo, categoría, descripción, valor)."""
    pendiente(2, "Integrante 1")


def definir_presupuesto():
    """TICKET 3 (parte A): pedir el presupuesto mensual y guardarlo en la variable global."""
    pendiente(3, "Integrante 1")


def verificar_presupuesto():
    """TICKET 3 (parte B): si hay presupuesto y los gastos pasan del 80 % o del 100 %,
    mostrar una alerta. El menú la llama sola después de cada gasto.
    Mientras no esté hecha, no hace nada (para no llenar la pantalla de avisos)."""
    pass


# =============================================================================
# INTEGRANTE 2 — Tickets 4, 5 y 6
# =============================================================================

def registrar_gasto():
    """TICKET 4: mostrar las categorías numeradas, elegir una, pedir descripción
    y valor, y guardar un movimiento tipo 'gasto'. Avisar si el saldo queda negativo."""
    print("\n--- REGISTRAR GASTO ---")
    print("  Categorías disponibles:")
    for i, cat in enumerate(CATEGORIAS, start=1):
        print(f"    {i}. {cat}")

    while True:
        eleccion = input("  Elija una categoría (número): ").strip()
        if eleccion.isdigit() and 1 <= int(eleccion) <= len(CATEGORIAS):
            categoria = CATEGORIAS[int(eleccion) - 1]
            break
        print("  ⚠ Opción no válida. Elija un número de la lista.")

    descripcion = pedir_texto("  Descripción del gasto: ")
    valor = pedir_valor("  Valor del gasto: ")

    movimientos.append({
        "tipo": "gasto",
        "categoria": categoria,
        "descripcion": descripcion,
        "valor": valor,
        "fecha": fecha_hoy(),
    })
    print(f"  ✓ Gasto registrado: {descripcion} ({categoria}) por {formato_pesos(valor)}.")

    _, _, saldo = calcular_totales()
    if saldo < 0:
        print(f"  🚨 ¡Cuidado! Su saldo quedó negativo: {formato_pesos(saldo)}.")


def ver_saldo():
    """TICKET 5: mostrar total de ingresos, total de gastos y saldo disponible."""
    print("\n--- SALDO DISPONIBLE ---")
    ingresos, gastos, saldo = calcular_totales()
    print(f"  Total ingresos    : {formato_pesos(ingresos):>15}")
    print(f"  Total gastos      : {formato_pesos(gastos):>15}")
    print(f"  Saldo disponible  : {formato_pesos(saldo):>15}")

    if presupuesto > 0:
        restante = presupuesto - gastos
        print(f"  Presupuesto mensual: {formato_pesos(presupuesto):>14}")
        print(f"  Restante del presupuesto: {formato_pesos(restante):>11}")


def eliminar_ultimo():
    """TICKET 6: mostrar el último movimiento, pedir confirmación (s/n) y borrarlo."""
    print("\n--- ELIMINAR ÚLTIMO MOVIMIENTO ---")
    if not movimientos:
        print("  No hay movimientos para eliminar.")
        return

    m = movimientos[-1]
    categoria = m["categoria"] if m["categoria"] else "-"
    print(f"  Último movimiento:")
    print(f"    Fecha      : {m['fecha']}")
    print(f"    Tipo       : {m['tipo']}")
    print(f"    Categoría  : {categoria}")
    print(f"    Descripción: {m['descripcion']}")
    print(f"    Valor      : {formato_pesos(m['valor'])}")

    respuesta = input("  ¿Eliminar este movimiento? (s/n): ").strip().lower()
    if respuesta == "s":
        movimientos.pop()
        print("  ✓ Movimiento eliminado.")
    else:
        print("  Operación cancelada.")



# =============================================================================
# INTEGRANTE 3 — Tickets 7, 8 y 9
# =============================================================================

def ver_resumen():
    """TICKET 7: total gastado por categoría con su porcentaje,
    y decir en qué categoría se gasta más."""
 _, total_gastos, _= calcular_totales()
if total_gastos == 0:
    print ("no hay gastos registrados aún")
    return 


def gasto_diario_disponible():
    """TICKET 8: con el saldo actual y los días que faltan para terminar el mes,
    calcular cuánto se puede gastar por día."""
    pendiente(8, "Integrante 3")


def buscar_por_categoria():
    """TICKET 9: elegir una categoría y mostrar solo los gastos de esa categoría
    con su total."""
    pendiente(9, "Integrante 3")


# =============================================================================
# MENÚ PRINCIPAL (base compartida, ya listo)
# =============================================================================

def menu():
    opciones = {
        "1": ("Registrar ingreso", registrar_ingreso),
        "2": ("Registrar gasto", registrar_gasto),
        "3": ("Ver saldo", ver_saldo),
        "4": ("Resumen por categoría", ver_resumen),
        "5": ("Historial de movimientos", ver_historial),
        "6": ("Buscar gastos por categoría", buscar_por_categoria),
        "7": ("¿Cuánto puedo gastar por día?", gasto_diario_disponible),
        "8": ("Definir presupuesto mensual", definir_presupuesto),
        "9": ("Eliminar último movimiento", eliminar_ultimo),
    }
    print("\n" + "=" * 50)
    print("   CONTROL DE GASTOS PARA ESTUDIANTES")
    print("=" * 50)
    while True:
        print("\nMENÚ PRINCIPAL")
        for clave, (texto, _) in opciones.items():
            print(f"  {clave}. {texto}")
        print("  0. Salir")
        eleccion = input("Elija una opción: ").strip()
        if eleccion == "0":
            print("\n¡Hasta pronto! Recuerde anotar todos sus gastos.")
            break
        elif eleccion in opciones:
            opciones[eleccion][1]()
            if eleccion == "2":
                verificar_presupuesto()
        else:
            print("  ⚠ Opción no válida.")


if __name__ == "__main__":
    menu()
