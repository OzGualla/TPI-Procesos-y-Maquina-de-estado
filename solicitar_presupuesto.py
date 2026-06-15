
import csv
import os

# ========================
# Declaración de funciones
# ========================

def mostrar_productos():
    """
    Retorna:
    filas (list): Lista de diccionarios con los datos de cada producto.
    """
    try:

        with open("productos.csv", "r", newline = "", encoding = "utf-8") as archivo:
            # Construir el lector
            # Y lee el archivo como un diccionario clave:valor
            lector = csv.DictReader(archivo)
            # Convertir todo el contenido del lector en una lista
            filas = list(lector)

            return filas
    
    except FileNotFoundError:
        print("Error: El archivo no existe")

    except Exception as e:
        print("Ha ocurrido un error inesperado: ",type(e).__name__)


def menu():
    """ Muestra el menú iterativo
    y los nombres de los productos
    """

    print("""
=============================
=== Bienvenido a FerroLux ===
=============================

=== Chatbot ===
Nuestros productos:
""")
    
    for fila in mostrar_productos():

        print(f"  - {fila['producto'].capitalize()}")


def elegir_producto():
    """
    Permite al usuario elegir un producto de la lista
    verifica si existe
    Retorna:
    fila de producto seleccionado
    """

    while True:
        
        producto = input("\nSeleccione un articulo de la lista: ")

        if not producto.isalpha():

            print("Error: Solo se aceptan letras")

            continue

        # Utiliza el return de la función mostrar_productor()
        for fila in mostrar_productos():

            # Igualar caracteres para comparación
            if producto.lower() == fila['producto'].lower():

                return fila
            
        print("El articulo no se encuentra en el catalogo")


def pedir_cantidad(fila):
    """
    Pide cantidad del producto al usuario
    retorna Nona si es menor al stock actual de ese producto
    retorna el valor de cantidad si es valido
    """

    while True:

        cantidad = input("Seleccione cantidad: ")

        # Validación de entrada
        if not cantidad.isdigit():

            print("Ingrese un número válido")

            continue

        cantidad = int(cantidad)

        # Si el stock actual es menor a la cantidad requerida
        # devuelve None
        if int(fila['stock']) < cantidad:

            print("Stock insuficiente")

            return None
        
        return cantidad


def calcular_presupuesto(fila, cantidad):
    """
    Calcula el presupuesto en base a el precio del articulo
    la cantidad seleccionada por el usuario
    y si aplica descuento
    """

    presupuesto = int(fila['precio']) * cantidad

    # Verifica si el articulo tiene descuento
    if fila['descuento'] == 'si':

        presupuesto -= (presupuesto * 15) / 100

    return presupuesto


def registrar_pedido(fila, cantidad, presupuesto):
    """
    Lee el archivo, cuenta la cantidad de filas y retorna su valor como numero de id
    Agrega la fila al archivo pedidos_registrados.csv
    """

    columnas = ["id_pedido", "producto", "cantidad", "presupuesto", "estado"]

    archivo_path = "pedidos_registrados.csv"

    try:
        # Contar pedidos existentes para generar el próximo id
        try:

            with open(archivo_path, "r", newline="", encoding="utf-8") as archivo:

                filas_existentes = list(csv.DictReader(archivo))

                # contador de numero ID
                numero_pedido = len(filas_existentes) + 1

        except FileNotFoundError:
            
            # Si el archivo no existe, generara el numero del primer pedido
            numero_pedido = 1

        archivo_existe = os.path.isfile(archivo_path)

        # ===================================================================

        # Agregar la fila con sus datos asociados al archivo
        with open(archivo_path, "a", newline="", encoding="utf-8") as archivo:

            escritor = csv.DictWriter(archivo, fieldnames=columnas)

            # Si el archivo no existe, genera los encabezados
            if not archivo_existe:

                escritor.writeheader()

            escritor.writerow({"id_pedido": numero_pedido,"producto": fila['producto'],"cantidad": cantidad,"presupuesto": presupuesto,"estado": "pendiente"})

        print(f"Pedido #{numero_pedido} registrado correctamente.")

    except Exception as e:

        print("Ha ocurrido un error inesperado: ", type(e).__name__)


# =======================
#         Main
# =======================

def main():

    # Estado inicial
    estado = "ESPERANDO_SOLICITUD"

    # Se utilizan variables fuera del match.
    # Son variables compartidas entre estados
    fila = None
    cantidad = None
    presupuesto = None
    numero_pedido = 0

    while True:

        match estado:

            # Siempre empieza la ejecución por "ESPERANDO_SOLICITUD"
            case "ESPERANDO_SOLICITUD":

                menu()

                fila = elegir_producto()

                # En cada case, se reasigna el estado del bot
                estado = "VERIFICAR_OFERTA_Y_STOCK"


            case "VERIFICAR_OFERTA_Y_STOCK":

                cantidad = pedir_cantidad(fila)

                if cantidad is None:

                    estado = "SIN_STOCK"

                else:

                    estado = "GENERAR_Y_ENVIAR_PRESUPUESTO"


            case "SIN_STOCK":
                
                print("\n=== Chatbot ===")
                print("Stock insuficiente para la cantidad solicitada.")

                print("¿Iniciar nuevo presupuesto?\n"\
                    "1-Si\n"\
                    "2-No\n")
                # De no contar con stock, se le consulta al usuario si quiere seguir operando
                opcion = input("-> ")

                # Si (Vuelve a iniciar el ciclo)
                if opcion == "1":

                    estado = "ESPERANDO_SOLICITUD"

                # No (Finaliza la ejecución)
                elif opcion == "2":

                    estado = "FINALIZADO"

                else:
                    
                    print("=== Chatbot ===")
                    print("=== Opción invalida ===")


            case "GENERAR_Y_ENVIAR_PRESUPUESTO":

                presupuesto = calcular_presupuesto(fila, cantidad)

                print("\n=== Chatbot ===")
                print("\nSu Presupuesto:")

                # Muestra el presupuesto final al usuario
                print(f"Articulo: {fila['producto']} | Cantidad: {cantidad} | Total: ${presupuesto:.2f}\n")

                estado = "ESPERANDO_CONFIRMACION"


            case "ESPERANDO_CONFIRMACION":
                
                print("\n=== Chatbot ===")
                print("¿Desea realizar el pedido?\n"\
                    "1-Si\n"\
                    "2-No\n")
            
                opcion = input("-> ")

                # Si (El pedido se registra y se deriva para autorizar)
                if opcion == "1":

                    estado = "REGISTRAR_PEDIDO"

                # No (Finaliza la ejecución)
                elif opcion == "2":

                    estado = "FINALIZADO"

                else:

                    # no cambia el estado, vuelve a preguntar
                    print("=== Chatbot ===")
                    print("Opción inválida")


            case "REGISTRAR_PEDIDO":

                registrar_pedido(fila, cantidad, presupuesto)

                print("\n=== Chatbot ===")
                print("Pedido enviado a Ventas para autorización.")

                estado = "ESPERANDO_AUTORIZACION"


            case "ESPERANDO_AUTORIZACION":

                # Simula que ventas recibe el pedido
                print("\n===== ÁREA VENTAS =====")
                input("\n[VENTAS] Presione Enter para revisar el pedido...")

                estado = "AUTORIZAR_PEDIDO"


            case "AUTORIZAR_PEDIDO":

                print("\n[VENTAS] ¿Autorizar pedido?\n"\
                    "1-Si\n"\
                    "2-No\n")
            
                opcion = input("-> ")

                if opcion == "1":

                    estado = "RECIBIR_AUTORIZACION"

                else:
                    
                    print("\n=== Chatbot ===")
                    print("Pedido rechazado por Ventas.")

                    estado = "FINALIZADO"

            
            case "RECIBIR_AUTORIZACION":
                
                print("\n=== Chatbot ===")
                print("Autorización recibida desde Ventas.")

                estado = "GENERAR_ORDEN_DE_PREPARACION"


            case "GENERAR_ORDEN_DE_PREPARACION":
                
                print("\n=== Chatbot ===")
                print("\nOrden de preparación generada.")

                estado = "DERIVAR_A_PRODUCCION"


            case "DERIVAR_A_PRODUCCION":

                print("Pedido derivado al área de producción.")

                estado = "FINALIZADO"


            case "FINALIZADO":

                print("\n=== Proceso finalizado ===\n")

                break


if __name__ == "__main__":
    main()