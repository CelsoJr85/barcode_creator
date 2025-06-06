"""
Teste.py - Interface para testar o gerador de código de barras
Interface simples com input para receber dados como string
"""

import os
import sys
from barcode_creator import (
    definir_pasta_padrao,
    gerar_codigo_barras,
    gerar_codigo_limpo,
    visualizar_codigo,
    codigo_barras_rapido,
    obter_pasta_padrao,
    listar_arquivos_gerados
)


def exibir_menu():
    """Exibe o menu principal"""
    print("\n" + "=" * 60)
    print("🔧 TESTADOR DE CÓDIGO DE BARRAS")
    print("=" * 60)
    print("1️⃣  Gerar código limpo (PNG + HTML + Base64)")
    print("2️⃣  Gerar código rápido (PNG simples)")
    print("3️⃣  Gerar código completo (todas as opções)")
    print("4️⃣  Visualizar código (PNG para exibição)")
    print("📁 5️⃣  Configurar pasta padrão")
    print("📋 6️⃣  Listar códigos gerados")
    print("ℹ️  7️⃣  Mostrar pasta atual")
    print("❌ 0️⃣  Sair")
    print("=" * 60)


def obter_dados_usuario():
    """Obtém dados do usuário via input"""
    print("\n📝 Digite os dados para o código de barras:")
    print("💡 Pode ser números, letras, símbolos - tudo como string")
    print("📋 Exemplos: '123456789', 'PRODUTO-ABC', 'Hello World 2025'")

    while True:
        dados = input("\n➤ Dados: ").strip()

        if not dados:
            print("❌ Por favor, digite algum dado!")
            continue

        # Confirmar dados
        print(f"\n✅ Dados recebidos: '{dados}'")
        confirma = input("📋 Confirmar? (s/n): ").strip().lower()

        if confirma in ['s', 'sim', 'y', 'yes', '']:
            return dados
        elif confirma in ['n', 'nao', 'não', 'no']:
            print("🔄 Digite novamente...")
            continue
        else:
            print("❓ Resposta inválida. Considerando como 'sim'...")
            return dados


def obter_pasta_usuario():
    """Obtém pasta do usuário"""
    print("\n📁 Digite o caminho da pasta (ou Enter para usar padrão):")
    print("💡 Exemplo: './meus_barcodes' ou 'C:/Códigos'")

    pasta = input("➤ Pasta: ").strip()

    if not pasta:
        return './codigos_barras'

    return pasta


def testar_codigo_limpo():
    """Testa a função gerar_codigo_limpo"""
    print("\n🎯 TESTE: Gerar Código Limpo")
    print("-" * 40)

    dados = obter_dados_usuario()

    try:
        print(f"\n🔄 Gerando código limpo para: '{dados}'")
        resultados = gerar_codigo_limpo(dados)

        print("\n✅ SUCESSO! Arquivos gerados:")
        print(f"📱 PNG: {resultados['png']}")
        print(f"🌐 HTML: {resultados['html']}")
        print(f"💻 Base64: Código HTML pronto para embed")

        # Verificar se arquivos existem
        if os.path.exists(resultados['png']):
            print(f"✅ Arquivo PNG criado: {os.path.getsize(resultados['png'])} bytes")
        if os.path.exists(resultados['html']):
            print(f"✅ Arquivo HTML criado: {os.path.getsize(resultados['html'])} bytes")

        print(f"\n💡 DICA: Para ver o código, abra: {resultados['html']}")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def testar_codigo_rapido():
    """Testa a função codigo_barras_rapido"""
    print("\n⚡ TESTE: Gerar Código Rápido")
    print("-" * 40)

    dados = obter_dados_usuario()

    try:
        print(f"\n🔄 Gerando código rápido para: '{dados}'")
        arquivo = codigo_barras_rapido(dados)

        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"\n✅ SUCESSO! PNG gerado: {arquivo}")
            print(f"📊 Tamanho: {tamanho} bytes")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def testar_codigo_completo():
    """Testa a função gerar_codigo_barras com opções"""
    print("\n🔧 TESTE: Gerar Código Completo")
    print("-" * 40)

    dados = obter_dados_usuario()

    # Opções avançadas
    print("\n⚙️ Opções avançadas:")
    print("1. Tipo: auto, code128, code39, ean13, ean8, upc")
    tipo = input("➤ Tipo de código (Enter=auto): ").strip() or 'auto'

    print("2. Formato: png, svg")
    formato = input("➤ Formato (Enter=png): ").strip() or 'png'

    nome = input("➤ Nome do arquivo (Enter=automático): ").strip() or None

    try:
        print(f"\n🔄 Gerando código completo...")
        print(f"📊 Dados: '{dados}' | Tipo: {tipo} | Formato: {formato}")

        arquivo = gerar_codigo_barras(
            dados=dados,
            tipo_codigo=tipo,
            formato_saida=formato,
            nome_arquivo=nome
        )

        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"\n✅ SUCESSO! Arquivo gerado: {arquivo}")
            print(f"📊 Tamanho: {tamanho} bytes")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def testar_visualizar_codigo():
    """Testa a função visualizar_codigo"""
    print("\n👁️ TESTE: Visualizar Código")
    print("-" * 40)

    dados = obter_dados_usuario()

    try:
        print(f"\n🔄 Gerando código para visualização: '{dados}'")
        arquivo = visualizar_codigo(dados)

        if os.path.exists(arquivo):
            tamanho = os.path.getsize(arquivo)
            print(f"\n✅ SUCESSO! PNG limpo gerado: {arquivo}")
            print(f"📊 Tamanho: {tamanho} bytes")
            print("💡 Este PNG é otimizado para exibição limpa (sem código SVG)")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def configurar_pasta():
    """Configura pasta padrão"""
    print("\n📁 CONFIGURAR PASTA PADRÃO")
    print("-" * 40)

    print(f"📂 Pasta atual: {obter_pasta_padrao()}")

    nova_pasta = obter_pasta_usuario()

    try:
        definir_pasta_padrao(nova_pasta)
        print(f"✅ Pasta padrão atualizada: {obter_pasta_padrao()}")
    except Exception as e:
        print(f"❌ ERRO ao configurar pasta: {e}")


def listar_codigos():
    """Lista códigos gerados"""
    print("\n📋 CÓDIGOS GERADOS")
    print("-" * 40)

    try:
        arquivos = listar_arquivos_gerados()

        if not arquivos:
            print("📭 Nenhum código de barras encontrado na pasta atual")
            print(f"📂 Pasta: {obter_pasta_padrao()}")
            return

        print(f"📂 Pasta: {obter_pasta_padrao()}")
        print(f"📊 Total: {len(arquivos)} arquivo(s)")
        print("\n📋 Arquivos encontrados:")

        for i, arquivo in enumerate(arquivos, 1):
            nome = os.path.basename(arquivo)
            if os.path.exists(arquivo):
                tamanho = os.path.getsize(arquivo)
                print(f"{i:2}. {nome} ({tamanho} bytes)")
            else:
                print(f"{i:2}. {nome} (arquivo não encontrado)")

    except Exception as e:
        print(f"❌ ERRO ao listar: {e}")


def mostrar_info():
    """Mostra informações do sistema"""
    print("\n ℹ️ INFORMAÇÕES DO SISTEMA")
    print("-" * 40)
    print(f"📂 Pasta padrão: {obter_pasta_padrao()}")
    print(f"📁 Pasta existe: {'✅ Sim' if os.path.exists(obter_pasta_padrao()) else '❌ Não'}")

    try:
        total_arquivos = len(listar_arquivos_gerados())
        print(f"📊 Total de códigos: {total_arquivos}")
    except:
        print("📊 Total de códigos: Erro ao contar")


def main():
    """Função principal do teste"""
    print("🚀 Iniciando testador de código de barras...")

    # Configurar pasta inicial se necessário
    if not os.path.exists(obter_pasta_padrao()):
        print(f"📁 Criando pasta padrão: {obter_pasta_padrao()}")
        os.makedirs(obter_pasta_padrao(), exist_ok=True)

    while True:
        try:
            exibir_menu()
            opcao = input("\n➤ Escolha uma opção: ").strip()

            if opcao == '1':
                testar_codigo_limpo()
            elif opcao == '2':
                testar_codigo_rapido()
            elif opcao == '3':
                testar_codigo_completo()
            elif opcao == '4':
                testar_visualizar_codigo()
            elif opcao == '5':
                configurar_pasta()
            elif opcao == '6':
                listar_codigos()
            elif opcao == '7':
                mostrar_info()
            elif opcao == '0':
                print("\n👋 Encerrando testador...")
                print("✅ Obrigado por usar o gerador de código de barras!")
                break
            else:
                print(f"❌ Opção inválida: '{opcao}'")
                print("💡 Escolha um número de 0 a 7")

            # Pausa para ver resultado
            if opcao != '0':
                input("\n⏯️  Pressione Enter para continuar...")

        except KeyboardInterrupt:
            print("\n\n❌ Interrompido pelo usuário (Ctrl+C)")
            print("👋 Encerrando...")
            break
        except Exception as e:
            print(f"\n❌ ERRO INESPERADO: {e}")
            input("\n⏯️  Pressione Enter para continuar...")


if __name__ == "__main__":
    main()
