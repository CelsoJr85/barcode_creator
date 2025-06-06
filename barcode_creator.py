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
_PASTA_PADRAO = './codigos_barras'


def definir_pasta_padrao(pasta: str) -> None:
    """
    Define a pasta padrão para salvar códigos de barras

    Args:
        pasta (str): Caminho da pasta que será usada como padrão
    """
    global _PASTA_PADRAO
    _PASTA_PADRAO = os.path.abspath(pasta)
    os.makedirs(_PASTA_PADRAO, exist_ok=True)
    print(f"📁 Pasta padrão definida: {_PASTA_PADRAO}")


def gerar_codigo_barras(
        dados: str,
        tipo_codigo: Literal['auto', 'code128', 'code39', 'ean13', 'ean8', 'upc'] = 'auto',
        formato_saida: Literal['png', 'svg'] = 'png',
        nome_arquivo: Optional[str] = None,
        pasta_destino: Optional[str] = None,
        opcoes_customizacao: Optional[dict] = None
) -> str:
    """
    Gera código de barras completo com todas as opções

    Args:
        dados (str): Texto ou números para gerar o código de barras
        tipo_codigo (str): Tipo do código de barras
        formato_saida (str): 'png' ou 'svg'
        nome_arquivo (str, optional): Nome personalizado do arquivo
        pasta_destino (str, optional): Pasta específica (usa padrão se None)
        opcoes_customizacao (dict, optional): Opções para customizar aparência

    Returns:
        str: Caminho completo do arquivo gerado
    """

    # Usar pasta padrão se não especificada
    pasta = pasta_destino if pasta_destino is not None else _PASTA_PADRAO
    os.makedirs(pasta, exist_ok=True)

    # Detectar tipo automaticamente se necessário
    if tipo_codigo == 'auto':
        tipo_codigo = _detectar_tipo_codigo(dados)

    # Validar e preparar dados
    dados_processados = _validar_e_processar_dados(dados, tipo_codigo)

    # Selecionar classe do código de barras
    classes_codigo = {
        'code128': Code128,
        'code39': Code39,
        'ean13': EAN13,
        'ean8': EAN8,
        'upc': UPCA
    }

    if tipo_codigo not in classes_codigo:
        raise ValueError(f"Tipo de código não suportado: {tipo_codigo}")

    # Configurar writer
    writer = ImageWriter() if formato_saida == 'png' else SVGWriter()

    # Aplicar opções de customização
    if opcoes_customizacao:
        for opcao, valor in opcoes_customizacao.items():
            if hasattr(writer, opcao):
                setattr(writer, opcao, valor)

    try:
        # Gerar código de barras
        codigo_barras = classes_codigo[tipo_codigo](dados_processados, writer=writer)

        # Definir nome do arquivo
        if not nome_arquivo:
            nome_arquivo = f"barcode_{dados_processados[:10]}_{tipo_codigo}"

        # Remover caracteres inválidos do nome do arquivo
        nome_arquivo = re.sub(r'[<>:"/\\|?*]', '_', nome_arquivo)

        # Caminho completo
        caminho_arquivo = os.path.join(pasta, nome_arquivo)

        # Salvar arquivo
        codigo_barras.save(caminho_arquivo)

        # Retornar caminho completo com extensão
        extensao = '.png' if formato_saida == 'png' else '.svg'
        caminho_completo = caminho_arquivo + extensao

        return caminho_completo

    except Exception as e:
        raise Exception(f"Erro ao gerar código de barras: {str(e)}")


def gerar_codigo_limpo(
        dados: str,
        pasta_destino: Optional[str] = None
) -> dict:
    """
    Gera código de barras otimizado para exibição limpa

    Args:
        dados (str): Texto ou números para o código
        pasta_destino (str, optional): Pasta específica (usa padrão se None)

    Returns:
        dict: Dicionário com arquivos e códigos gerados
            - 'png': Caminho do arquivo PNG (sempre limpo)
            - 'base64': Código HTML com imagem em base64
            - 'html': Arquivo HTML completo para visualização
    """

    # Usar pasta padrão se não especificada
    pasta = pasta_destino if pasta_destino is not None else _PASTA_PADRAO
    os.makedirs(pasta, exist_ok=True)

    resultados = {}

    # Detectar melhor tipo de código
    tipo_codigo = _detectar_tipo_codigo(dados)
    dados_processados = _validar_e_processar_dados(dados, tipo_codigo)

    # 1. PNG - Sempre limpo e confiável
    writer_png = ImageWriter()
    codigo_png = Code128(dados_processados, writer=writer_png)
    caminho_png = os.path.join(pasta, f"barcode_{dados_processados[:10]}")
    codigo_png.save(caminho_png)
    resultados['png'] = caminho_png + '.png'

    # 2. Base64 - Para embed direto no HTML
    buffer = BytesIO()
    codigo_png.write(buffer)
    buffer.seek(0)
    img_base64 = base64.b64encode(buffer.read()).decode()
    resultados[
        'base64'] = f'<img src="data:image/png;base64,{img_base64}" alt="Barcode" style="max-width:100%;height:auto;">'

    # 3. HTML completo - Para visualização perfeita
    html_content = f"""<!DOCTYPE html>
<html>
<head>
    <title>Código de Barras - {dados}</title>
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
            <img src="{os.path.basename(resultados['png'])}" alt="Código de Barras">
        </div>
        <div class="info">
            <div class="code">{dados}</div>
            <p>Código gerado automaticamente</p>
        </div>
    </div>
</body>
</html>"""

    arquivo_html = os.path.join(pasta, f"barcode_{dados_processados[:10]}.html")
    with open(arquivo_html, 'w', encoding='utf-8') as f:
        f.write(html_content)
    resultados['html'] = arquivo_html

    return resultados


def visualizar_codigo(dados: str, pasta_destino: Optional[str] = None) -> str:
    """
    Função simplificada - Gera e retorna PNG limpo para visualização

    Args:
        dados (str): Texto ou números
        pasta_destino (str, optional): Pasta específica (usa padrão se None)

    Returns:
        str: Caminho do arquivo PNG (melhor para exibição limpa)
    """
    resultado = gerar_codigo_limpo(dados, pasta_destino)
    return resultado['png']


def codigo_barras_rapido(dados: str, pasta_destino: Optional[str] = None) -> str:
    """
    Versão simplificada para gerar código de barras rapidamente

    Args:
        dados (str): Texto ou números
        pasta_destino (str, optional): Pasta específica (usa padrão se None)

    Returns:
        str: Caminho do arquivo PNG gerado
    """
    return gerar_codigo_barras(dados, formato_saida='png', pasta_destino=pasta_destino)


# FUNÇÕES AUXILIARES INTERNAS

def _detectar_tipo_codigo(dados: str) -> str:
    """Detecta automaticamente o melhor tipo de código de barras"""

    dados_limpos = dados.replace(' ', '')

    if dados_limpos.isdigit():
        if len(dados_limpos) == 13:
            return 'ean13'
        elif len(dados_limpos) == 8:
            return 'ean8'
        elif len(dados_limpos) == 12:
            return 'upc'
        else:
            return 'code128'

    elif not dados_limpos.isupper() or any(c in dados_limpos for c in ['@', '#', '$', '%']):
        return 'code128'

    else:
        return 'code39'


def _validar_e_processar_dados(dados: str, tipo_codigo: str) -> str:
    """Valida e processa os dados conforme o tipo de código"""

    dados_processados = dados.strip()

    if tipo_codigo == 'ean13':
        numeros = re.sub(r'[^0-9]', '', dados_processados)
        if len(numeros) < 12:
            numeros = numeros.zfill(12)
        elif len(numeros) > 12:
            numeros = numeros[:12]
        dados_processados = numeros

    elif tipo_codigo == 'ean8':
        numeros = re.sub(r'[^0-9]', '', dados_processados)
        if len(numeros) < 7:
            numeros = numeros.zfill(7)
        elif len(numeros) > 7:
            numeros = numeros[:7]
        dados_processados = numeros

    elif tipo_codigo == 'upc':
        numeros = re.sub(r'[^0-9]', '', dados_processados)
        if len(numeros) < 11:
            numeros = numeros.zfill(11)
        elif len(numeros) > 11:
            numeros = numeros[:11]
        dados_processados = numeros

    elif tipo_codigo == 'code39':
        dados_processados = dados_processados.upper()
        caracteres_validos = set('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ-. $/+%')
        if not all(c in caracteres_validos for c in dados_processados):
            raise ValueError("Code39 não suporta alguns caracteres do texto fornecido")

    return dados_processados


def obter_pasta_padrao() -> str:
    """
    Retorna a pasta padrão atual

    Returns:
        str: Caminho da pasta padrão
    """
    return _PASTA_PADRAO


def listar_arquivos_gerados(pasta: Optional[str] = None) -> list:
    """
    Lista todos os códigos de barras gerados em uma pasta

    Args:
        pasta (str, optional): Pasta para listar (usa padrão se None)

    Returns:
        list: Lista de arquivos de código de barras encontrados
    """
    pasta_busca = pasta if pasta is not None else _PASTA_PADRAO

    if not os.path.exists(pasta_busca):
        return []

    arquivos = []
    for arquivo in os.listdir(pasta_busca):
        if arquivo.startswith('barcode_') and (
                arquivo.endswith('.png') or arquivo.endswith('.svg') or arquivo.endswith('.html')):
            arquivos.append(os.path.join(pasta_busca, arquivo))

    return sorted(arquivos)