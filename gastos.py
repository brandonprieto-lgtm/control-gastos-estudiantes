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
    print("\n--- REGISTRAR INGRESO ---")
    descripcion = pedir_texto("Descripción (ej: Mesada, Trabajo): ")
    valor = pedir_valor("Valor del ingreso: ")
    movimiento = {
        "tipo": "ingreso",
        "categoria": None,
        "descripcion": descripcion,
        "valor": valor,
        "fecha": fecha_hoy(),
    }
    movimientos.append(movimiento)
    print(f"  ✔ Ingreso registrado: {descripcion} por {formato_pesos(valor)}")


def ver_historial():
    """TICKET 2: mostrar todos los movimientos en una tabla
    (número, fecha, tipo, categoría, descripción, valor)."""
    print("\n--- HISTORIAL DE MOVIMIENTOS ---")
    if not movimientos:
        print("  No hay movimientos.")
        return
    print(f"{'N°':<4}{'Fecha':<12}{'Tipo':<9}{'Categoría':<17}{'Descripción':<20}{'Valor':>12}")
    print("-" * 74)
    for numero, m in enumerate(movimientos, start=1):
        categoria = m["categoria"] if m["categoria"] else "-"
        print(f"{numero:<4}{m['fecha']:<12}{m['tipo']:<9}{categoria:<17}"
              f"{m['descripcion'][:19]:<20}{formato_pesos(m['valor']):>12}")
    print("-" * 74)
    ingresos, gastos, saldo = calcular_totales()
    print(f"  Total ingresos: {formato_pesos(ingresos)}")
    print(f"  Total gastos:   {formato_pesos(gastos)}")
    print(f"  Saldo actual:   {formato_pesos(saldo)}")


def definir_presupuesto():
    """TICKET 3 (parte A): pedir el presupuesto mensual y guardarlo en la variable global."""
    global presupuesto
    print("\n--- DEFINIR PRESUPUESTO MENSUAL ---")
    if presupuesto > 0:
        print(f"  Presupuesto actual: {formato_pesos(presupuesto)}")
    presupuesto = pedir_valor("Nuevo presupuesto mensual para gastos: ")
    print(f"  ✔ Presupuesto definido en {formato_pesos(presupuesto)}")
    verificar_presupuesto()


def verificar_presupuesto():
    """TICKET 3 (parte B): si hay presupuesto y los gastos pasan del 80 % o del 100 %,
    mostrar una alerta. El menú la llama sola después de cada gasto.
    Mientras no esté hecha, no hace nada (para no llenar la pantalla de avisos)."""
    if presupuesto <= 0:
        return
    _, total_gastos, _ = calcular_totales()
    porcentaje = total_gastos / presupuesto * 100
    if porcentaje >= 100:
        exceso = total_gastos - presupuesto
        print(f"  🚨 ALERTA: superó el presupuesto ({porcentaje:.0f} %). "
              f"Se pasó por {formato_pesos(exceso)}.")
    elif porcentaje >= 80:
        restante = presupuesto - total_gastos
        print(f"  ⚠ Cuidado: ya usó el {porcentaje:.0f} % del presupuesto. "
              f"Le quedan {formato_pesos(restante)}.")


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
    _, total_gastos, _ = calcular_totales()
    if total_gastos == 0:
        print("\nNo hay gastos registrados aún.")
        return

    gastos_por_categoria = {cat: 0 for cat in CATEGORIAS}
    for movimiento in movimientos:
        if (movimiento["tipo"] == "gasto"
                and movimiento["categoria"] in gastos_por_categoria):
            gastos_por_categoria[movimiento["categoria"]] += movimiento["valor"]

    print("\n--- RESUMEN DE GASTOS POR CATEGORÍA ---")
    for categoria, valor in gastos_por_categoria.items():
        porcentaje = valor / total_gastos * 100
        print(f"  {categoria}: {formato_pesos(valor)} ({porcentaje:.1f}%)")

    categoria_max = max(gastos_por_categoria, key=gastos_por_categoria.get)
    print(
        f"\nLa categoría en la que más gastas es: {categoria_max} "
        f"con {formato_pesos(gastos_por_categoria[categoria_max])}."
    )


def gasto_diario_disponible():
    """Calcula cuánto dinero puede gastar el estudiante por día hasta fin de mes."""
    _, _, saldo = calcular_totales()
    
    if saldo <= 0:
        print("  ⚠ No tienes saldo disponible para calcular un gasto diario.")
        return

    hoy = datetime.now()
    dias_del_mes = calendar.monthrange(hoy.year, hoy.month)[1]
    dias_restantes = dias_del_mes - hoy.day + 1 

    presupuesto_diario = saldo / dias_restantes
    
    print(f"\n  Tienes un saldo de {formato_pesos(saldo)} para los próximos {dias_restantes} días.")
    print(f" Puedes gastar aproximadamente {formato_pesos(presupuesto_diario)} diarios.")


def buscar_por_categoria():
    """Muestra un menú de categorías, filtra y suma los gastos de la categoría elegida."""
    print("\n--- CATEGORÍAS DISPONIBLES ---")
    for i, cat in enumerate(CATEGORIAS, 1):
        print(f"  {i}. {cat}")
    
    try:
        opcion = int(input("Elija el número de la categoría: "))
    except ValueError:
        print("  ⚠ Por favor, ingrese un número válido.")
        return

    if opcion < 1 or opcion > len(CATEGORIAS):
        print("  ⚠ Opción no válida.")
        return
        
    categoria_elegida = CATEGORIAS[opcion - 1]
    
    # Filtrar solo los gastos que coincidan con la categoría
    gastos_filtrados = [m for m in movimientos if m["tipo"] == "gasto" and m["categoria"] == categoria_elegida]
    
    print(f"\n--- GASTOS EN: {categoria_elegida.upper()} ---")
    if not gastos_filtrados:
        print("  No hay gastos registrados en esta categoría.")
        return
        
    total_categoria = 0
    # Imprimir historial y sumar
    for m in gastos_filtrados:
        print(f"  - {m['fecha']}: {m['descripcion']} -> {formato_pesos(m['valor'])}")
        total_categoria += m["valor"]
        
    print(f"\n  Total gastado en {categoria_elegida}: {formato_pesos(total_categoria)}")


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
