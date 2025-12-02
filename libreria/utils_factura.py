import os
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from django.conf import settings
from django.contrib.staticfiles import finders


def generar_factura_pdf(transaccion):
    from .models import Transaccion  # Evita import circular

    nombre_archivo = f"factura_{transaccion.id}.pdf"
    ruta_completa = os.path.join(settings.MEDIA_ROOT, nombre_archivo)

    c = canvas.Canvas(ruta_completa, pagesize=letter)
    width, height = letter

    # -----------------------------
    #   MARCA DE AGUA / LOGO
    # -----------------------------
    logo_path = finders.find("imagen/logo.png")  # Ajústalo si tu logo está en otra carpeta

    if logo_path:
        c.saveState()
        c.setFillColor(colors.Color(1, 1, 1, alpha=0.3))
        c.setStrokeColor(colors.Color(1, 1, 1, alpha=0.3))
        c.drawImage(
            logo_path,
            x=(width - 300) / 2,
            y=(height - 300) / 2,
            width=300,
            height=300,
            mask="auto"
        )
        c.restoreState()

    # -----------------------------
    #          ENCABEZADO
    # -----------------------------
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(width / 2, height - 50, "LACTEOS HEDYBED")

    c.setFont("Helvetica", 14)
    c.drawCentredString(width / 2, height - 75, "FACTURA DE VENTA")

    # -----------------------------
    #     INFO FACTURA
    # -----------------------------
    c.setFont("Helvetica", 10)
    c.drawString(40, height - 120, f"Factura N°: {transaccion.id}")
    c.drawString(40, height - 135, f"Fecha: {transaccion.fecha}")

    # -----------------------------
    #     INFO CLIENTE
    # -----------------------------
    if transaccion.cliente:
        c.drawString(40, height - 170, f"Cliente: {transaccion.cliente.nombre}")
        c.drawString(40, height - 185, f"Documento: {transaccion.cliente.documento}")
    else:
        c.drawString(40, height - 170, "Cliente: No registrado")

    # -----------------------------
    #   TABLA DE PRODUCTOS
    # -----------------------------
    y = height - 230

    c.setFont("Helvetica-Bold", 11)
    c.drawString(40, y, "Producto")
    c.drawString(250, y, "Cantidad")
    c.drawString(320, y, "Precio")
    c.drawString(400, y, "Subtotal")

    c.line(40, y - 5, width - 40, y - 5)
    y -= 25

    c.setFont("Helvetica", 10)

    items = transaccion.obtener_items()

    for item in items:
        c.drawString(40, y, item["nombre"])
        c.drawString(250, y, str(item["cantidad"]))
        c.drawString(320, y, f"${item['precio']:,.0f}")
        c.drawString(400, y, f"${item['subtotal']:,.0f}")
        y -= 20

    # -----------------------------
    #           TOTAL
    # -----------------------------
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y - 20, f"TOTAL A PAGAR: ${transaccion.monto_total:,.0f}")

    c.save()
    return nombre_archivo
