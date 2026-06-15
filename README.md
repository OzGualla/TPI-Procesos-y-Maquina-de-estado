## FerroLux — Chatbot de Presupuestación
Trabajo Práctico Integrador — Organización Empresarial  
Tecnicatura Universitaria en Programación (UTN)

## Descripción
Simulación de un chatbot de consola que automatiza el proceso de presupuestación del área de Ventas de FerroLux, una empresa del rubro metalúrgico.
El bot permite al cliente consultar productos, obtener un presupuesto en tiempo real (con descuentos aplicados automáticamente) y registrar su pedido, que luego es derivado al área de Ventas para su autorización y posterior envío a producción.

## Estructura del proyecto

```text
TPI-Procesos-y-Maquina-de-estado/
│
├── solicitar_presupuesto.py      # Script principal del chatbot
├── productos.csv                 # Base de datos del catálogo de productos
├── pedidos_registrados.csv       # Registro de pedidos generados (se crea automáticamente)
│
├── docs/
│   ├── TPI_Informe_Empresa_Ferrolux.pdf
│   ├── FerroLux_Diccionario_de_Datos.pdf
│   ├── FerroLux_Manual_de_Usuario.pdf
│   ├── Maquina_de_estado.pdf
│   ├── Consultas_IA.pdf
│   ├── as-is.bpmn                # Diagrama BPMN del proceso AS-IS
│   └── to-be.bpmn                # Diagrama BPMN del proceso TO-BE
│
├── README.md
└── .gitignore
```

## Requisitos
Python 3.10 o superior (se utiliza "match/case" , disponible desde 3.10)
Módulos: "csv", "os" (ambos incluidos en la biblioteca estándar, no requieren instalación adicional)

## Cómo ejecutar
Clonar o descargar el repositorio:

https://github.com/OzGualla/TPI-Procesos-y-Maquina-de-estado

Verificar que "productos.csv" y "pedidos_registrados.csv" esté en el mismo directorio que el script.
Ejecutar el chatbot:
	
python solicitar_presupuesto.py


## Flujo del chatbot

```text
Cliente selecciona producto
        |
Sistema verifica stock
        |
    ¿Hay stock?
   /           \
  Sí            No -> Ofrece reiniciar o finalizar
   |
Sistema calcula presupuesto (con descuento si aplica)
        |
¿Cliente confirma el pedido?
   /           \
  Sí            No -> Finaliza
   |
Pedido registrado en CSV con estado "pendiente"
        |
Ventas revisa y autoriza/rechaza
        |
    ¿Autorizado?
   /           \
  Sí            No -> Finaliza
   |
Se genera orden de preparación
        |
Pedido derivado a producción -> Finaliza
```

## Reglas de negocio
-Se aplica un descuento del 15% cuando el producto tiene 'descuento = "si"'.
-No se puede pedir una cantidad mayor al stock disponible.
-El campo producto solo acepta letras (sin números ni caracteres especiales).
-La cantidad debe ser un número entero positivo.
-Todo pedido se registra con estado "pendiente".
-El pedido solo avanza a producción si Ventas lo autoriza explícitamente.

```text
## Integrantes
Gualla Mariano
Furfaro Ivan

## Entidad
Carrera: Tecnicatura de programacion a distancia
Cátedra: Organización Empresarial — UTN  
Docente titular: Prof. Gabriela Martínez
Docentes adjuntos: Prof. Carolina Bruno, Prof. Mario Raúl López, Prof. Andrea Ramos
```
