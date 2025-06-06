"""
Gerador de Código de Barras - Função Principal
Biblioteca reutilizável para gerar códigos de barras com exibição limpa
"""

from barcode import Code128, Code39, EAN13, EAN8, UPCA
from barcode.writer import ImageWriter, SVGWriter
import os
from typing import Optional, Literal, Union
import re
import base64
from io import BytesIO

# Variável global para pasta padrão
_DEFAULT_FOLDER = './codigos_barras'


def set_default_folder(folder: str) -> None:
    """
    Define a pasta padrão para salvar códigos de barras

    Args:
        folder (str): Caminho da pasta que será usada como padrão
    """
    global _DEFAULT_FOLDER
    _DEFAULT_FOLDER = os.path.abspath(folder)
    os.makedirs(_DEFAULT_FOLDER, exist_ok=True)
    print(f"📁 Pasta padrão definida: {_DEFAULT_FOLDER}")


def generate_barcode(
        data: str,
        code_type: Literal['auto', 'code128', 'code39', 'ean13', 'ean8', 'upc'] = 'auto',
        output_format: Literal['png', 'svg'] = 'png',
        file_name: Optional[str] = None,
        destination_folder: Optional[str] = None,
        customization_options: Optional[dict] = None
) -> str:
    """
    Gera código de barras completo com todas as opções

    Args:
        data (str): Texto ou números para gerar o código de barras
        code_type (str): Tipo do código de barras
        output_format (str): 'png' ou 'svg'
        file_name (str, optional): Nome personalizado do arquivo
        destination_folder (str, optional): Pasta específica (usa padrão se None)
        customization_options (dict, optional): Opções para customizar aparência

    Returns:
        str: Caminho completo do arquivo gerado
    """

    # Usar pasta padrão se não especificada
    folder = destination_folder if destination_folder is not None else _DEFAULT_FOLDER
    os.makedirs(folder, exist_ok=True)

    # Detectar tipo automaticamente se necessário
    if code_type == 'auto':
        code_type = _detect_code_type(data)

    # Validar e preparar dados
    processed_data = _validate_and_process_data(data, code_type)

    # Selecionar classe do código de barras
    code_classes = {
        'code128': Code128,
        'code39': Code39,
        'ean13': EAN13,
        'ean8': EAN8,
        'upc': UPCA
    }

    if code_type not in code_classes:
        raise ValueError(f"Tipo de código não suportado: {code_type}")

    # Configurar writer
    writer = ImageWriter() if output_format == 'png' else SVGWriter()

    # Aplicar opções de customização
    if customization_options:
        for option, value in customization_options.items():
            if hasattr(writer, option):
                setattr(writer, option, value)

    try:
        # Gerar código de barras
        barcode = code_classes[code_type](processed_data, writer=writer)

        # Definir nome do arquivo
        if not file_name:
            file_name = f"barcode_{processed_data[:10]}_{code_type}"

        # Remover caracteres inválidos do nome do arquivo
        file_name = re.sub(r'[<>:"/\\|?*]', '_', file_name)

        # Caminho completo
        file_path = os.path.join(folder, file_name)

        # Salvar arquivo
        barcode.save(file_path)

        # Retornar caminho completo com extensão
        extension = '.png' if output_format == 'png' else '.svg'
        complete_path = file_path + extension

        return complete_path

    except Exception as e:
        raise Exception(f"Erro ao gerar código de barras: {str(e)}")


def generate_clean_barcode(
        data: str,
        destination_folder: Optional[str] = None
) -> dict:
    """
    Gera código de barras otimizado para exibição limpa

    Args:
        data (str): Texto ou números para o código
        destination_folder (str, optional): Pasta específica (usa padrão se None)

    Returns:
        dict: Dicionário com arquivos e códigos gerados
            - 'png': Caminho do arquivo PNG (sempre limpo)
            - 'base64': Código HTML com imagem em base64
            - 'html': Arquivo HTML completo para visualização
    """

    # Usar pasta padrão se não especificada
    folder = destination_folder if destination_folder is not None else _DEFAULT_FOLDER
    os.makedirs(folder, exist_ok=True)

    results = {}

    # Detectar melhor tipo de código
    code_type = _detect_code_type(data)
    processed_data = _validate_and_process_data(data, code_type)

    # 1. PNG - Sempre limpo e confiável
    png_writer = ImageWriter()
    png_barcode = Code128(processed_data, writer=png_writer)
    png_path = os.path.join(folder, f"barcode_{processed_data[:10]}")
    png_barcode.save(png_path)
    results['png'] = png_path + '.png'

    # 2. Base64 - Para embed direto no HTML
    buffer = BytesIO()
    png_barcode.write(buffer)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    results[
        'base64'] = f'<img src="data:image/png;base64,{img_base64}" alt="Barcode" style="max-width:100%;height:auto;">'

    # 3. HTML completo - Para visualização perfeita
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Código de Barras - {data}</title>
    <style>
        body {{ margin: 0; padding: 20px; background: #f5f5f5; font-family: Arial, sans-serif; }}
        .container {{ max-width: 800px; margin: 0 auto; background: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .barcode {{ text-align: center; margin: 20px 0; }}
        .barcode img {{ max-width: 100%; height: auto; border: 1px solid #ddd; padding: 10px; }}
        .info {{ text-align: center; color: #666; font-size: 14px; margin-top: 15px; }}
        .code {{ font-family: monospace; font-size: 18px; font-weight: bold; color: #333; }}
    </style>
</head>
<body>
    <div class="container">
        <h2 style="text-align: center; color: #333;">Código de Barras</h2>
        <div class="barcode">
            <img src="{os.path.basename(results['png'])}" alt="Código de Barras">
        </div>
        <div class="info">
            <div class="code">{data}</div>
            <p>Código gerado automaticamente</p>
        </div>
    </div>
</body>
</html>"""

    html_file = os.path.join(folder, f"barcode_{processed_data[:10]}.html")
    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)
    results['html'] = html_file

    return results


def visualize_barcode(data: str, destination_folder: Optional[str] = None) -> str:
    """
    Função simplificada - Gera e retorna PNG limpo para visualização

    Args:
        data (str): Texto ou números
        destination_folder (str, optional): Pasta específica (usa padrão se None)

    Returns:
        str: Caminho do arquivo PNG (melhor para exibição limpa)
    """
    result = generate_clean_barcode(data, destination_folder)
    return result['png']


def quick_barcode(data: str, destination_folder: Optional[str] = None) -> str:
    """
    Versão simplificada para gerar código de barras rapidamente

    Args:
        data (str): Texto ou números
        destination_folder (str, optional): Pasta específica (usa padrão se None)

    Returns:
        str: Caminho do arquivo PNG gerado
    """
    return generate_barcode(data, output_format='png', destination_folder=destination_folder)


# FUNÇÕES AUXILIARES INTERNAS

def _detect_code_type(data: str) -> str:
    """Detecta automaticamente o melhor tipo de código de barras"""

    clean_data = data.replace(' ', '')

    if clean_data.isdigit():
        if len(clean_data) == 13:
            return 'ean13'
        elif len(clean_data) == 8:
            return 'ean8'
        elif len(clean_data) == 12:
            return 'upc'
        else:
            return 'code128'

    elif not clean_data.isupper() or any(c in clean_data for c in ['@', '#', '$', '%']):
        return 'code128'

    else:
        return 'code39'


def _validate_and_process_data(data: str, code_type: str) -> str:
    """Valida e processa os dados conforme o tipo de código"""

    processed_data = data.strip()

    if code_type == 'ean13':
        numbers = re.sub(r'[^0-9]', '', processed_data)
        if len(numbers) < 12:
            numbers = numbers.zfill(12)
        elif len(numbers) > 12:
            numbers = numbers[:12]
        processed_data = numbers

    elif code_type == 'ean8':
        numbers = re.sub(r'[^0-9]', '', processed_data)
        if len(numbers) < 7:
            numbers = numbers.zfill(7)
        elif len(numbers) > 7:
            numbers = numbers[:7]
        processed_data = numbers

    elif code_type == 'upc':
        numbers = re.sub(r'[^0-9]', '', processed_data)
        if len(numbers) < 11:
            numbers = numbers.zfill(11)
        elif len(numbers) > 11:
            numbers = numbers[:11]
        processed_data = numbers

    elif code_type == 'code39':
        processed_data = processed_data.upper()
        valid_characters = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%')
        if not all(c in valid_characters for c in processed_data):
            raise ValueError("Code39 não suporta alguns caracteres do texto fornecido")

    return processed_data


def get_default_folder() -> str:
    """
    Retorna a pasta padrão atual

    Returns:
        str: Caminho da pasta padrão
    """
    return _DEFAULT_FOLDER


def list_generated_files(folder: Optional[str] = None) -> list:
    """
    Lista todos os códigos de barras gerados em uma pasta

    Args:
        folder (str, optional): Pasta para listar (usa padrão se None)

    Returns:
        list: Lista de arquivos de código de barras encontrados
    """
    search_folder = folder if folder is not None else _DEFAULT_FOLDER

    if not os.path.exists(search_folder):
        return []

    files = []
    for file in os.listdir(search_folder):
        if file.startswith('barcode_') and (
                file.endswith('.png') or file.endswith('.svg') or file.endswith('.html')):
            files.append(os.path.join(search_folder, file))

    return sorted(files)