from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from barcode import EAN13
from barcode.writer import ImageWriter
import os

def generate_barcode(code, output_path):
    """Gera o código de barras e salva como imagem."""
    try:
        # Remover a extensão, pois o `save` adiciona automaticamente
        barcode = EAN13(code, writer=ImageWriter())
        barcode.save(output_path.replace(".png", ""))
        print(f"Código de barras salvo em: {output_path}")
    except Exception as e:
        print(f"Erro ao gerar o código de barras: {e}")

def generate_multiple_labels(background_pdf, num_labels, output_pdf):
    """Adiciona múltiplos rótulos com códigos de barras ao PDF."""
    # Caminhos para arquivos temporários
    barcode_image = "barcode.png"  # Nome base do código de barras
    barcode_pdf = "barcode_overlay.pdf"  # Arquivo PDF temporário para o código de barras

    # Verificar arquivo de fundo
    if not os.path.exists(background_pdf):
        raise FileNotFoundError(f"Arquivo de fundo não encontrado: {background_pdf}")

    # Dimensões e posição do código de barras no PDF
    barcode_x = 300  # Posição X no PDF
    barcode_y = 200  # Posição Y no PDF
    barcode_width = 100  # Largura do código de barras
    barcode_height = 50  # Altura do código de barras

    # Carregar o PDF de entrada
    original_pdf = PdfReader(background_pdf)
    writer = PdfWriter()

    # Gerar múltiplas páginas
    for i in range(num_labels):
        # Gerar o código de barras com sequência
        barcode_code = f"78985222{i:04d}"  # Sequência ajustada
        generate_barcode(barcode_code, barcode_image)

        # Criar um PDF temporário com o código de barras
        c = canvas.Canvas(barcode_pdf, pagesize=letter)
        c.drawImage(barcode_image, barcode_x, barcode_y, width=barcode_width, height=barcode_height)
        c.save()

        # Verificar se o arquivo PDF foi criado
        if not os.path.exists(barcode_pdf):
            raise FileNotFoundError(f"Arquivo PDF temporário não encontrado: {barcode_pdf}")

        # Adicionar o conteúdo do rótulo ao PDF de saída
        overlay_pdf = PdfReader(barcode_pdf)
        for page in original_pdf.pages:
            page.merge_page(overlay_pdf.pages[0])
            writer.add_page(page)

    # Salvar o resultado final
    with open(output_pdf, "wb") as output_file:
        writer.write(output_file)

    # Remover arquivos temporários
    if os.path.exists(barcode_image):
        os.remove(barcode_image)
    if os.path.exists(barcode_pdf):
        os.remove(barcode_pdf)

    print(f"Rótulos gerados em: {output_pdf}")

# Exemplo de uso
background_pdf = "meu_rotulo.pdf"  # Arquivo PDF de fundo
num_labels = 50                    # Número de rótulos desejados
output_pdf = "rotulo_final.pdf"    # Nome do PDF final gerado

generate_multiple_labels(background_pdf, num_labels, output_pdf)
