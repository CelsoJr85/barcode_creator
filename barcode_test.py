"""
Test.py - Interface para testar o gerador de código de barras
Interface simples com input para receber dados como string
"""

import os
import sys
from barcode_creator import (
    set_default_folder,
    generate_barcode,
    generate_clean_barcode,
    visualize_barcode,
    quick_barcode,
    get_default_folder,
    list_generated_files
)


def display_menu():
    """Exibe o menu principal"""
    print("\n" + "=" * 60)
    print("🔧 TESTADOR DE CÓDIGO DE BARRAS")
    print("=" * 60)
    print("1️⃣  Gerar código limpo (PNG + HTML + Base64)")
    print("2️⃣  Gerar código rápido (PNG simples)")
    print("3️⃣  Gerar código completo (todas as opções)")
    print("4️⃣  Visualizar código (PNG para exibição)")
    print("5️⃣  Configurar pasta padrão")
    print("6️⃣  Listar códigos gerados")
    print("7️⃣  Mostrar pasta atual")
    print("0️⃣  Sair")
    print("=" * 60)


def get_user_data():
    """Obtém dados do usuário via input"""
    print("\n📝 Digite os dados para o código de barras:")
    print("💡 Pode ser números, letras, símbolos - tudo como string")
    print("📋 Exemplos: '123456789', 'PRODUTO-ABC', 'Hello World 2025'")

    while True:
        data = input("\n➤ Dados: ").strip()

        if not data:
            print("❌ Por favor, digite algum dado!")
            continue

        # Confirmar dados
        print(f"\n✅ Dados recebidos: '{data}'")
        confirm = input("📋 Confirmar? (s/n): ").strip().lower()

        if confirm in ['s', 'sim', 'y', 'yes', '']:
            return data
        elif confirm in ['n', 'nao', 'não', 'no']:
            print("🔄 Digite novamente...")
            continue
        else:
            print("❓ Resposta inválida. Considerando como 'sim'...")
            return data


def get_user_folder():
    """Obtém pasta do usuário"""
    print("\n📁 Digite o caminho da pasta (ou Enter para usar padrão):")
    print("💡 Exemplo: './meus_barcodes' ou 'C:/Códigos'")

    folder = input("➤ Pasta: ").strip()

    if not folder:
        return './codigos_barras'

    return folder


def test_clean_barcode():
    """Testa a função generate_clean_barcode"""
    print("\n🎯 TESTE: Gerar Código Limpo")
    print("-" * 40)

    data = get_user_data()

    try:
        print(f"\n🔄 Gerando código limpo para: '{data}'")
        results = generate_clean_barcode(data)

        print("\n✅ SUCESSO! Arquivos gerados:")
        print(f"📱 PNG: {results['png']}")
        print(f"🌐 HTML: {results['html']}")
        print(f"💻 Base64: Código HTML pronto para embed")

        # Verificar se arquivos existem
        if os.path.exists(results['png']):
            print(f"✅ Arquivo PNG criado: {os.path.getsize(results['png'])} bytes")
        if os.path.exists(results['html']):
            print(f"✅ Arquivo HTML criado: {os.path.getsize(results['html'])} bytes")

        print(f"\n💡 DICA: Para ver o código, abra: {results['html']}")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def test_quick_barcode():
    """Testa a função quick_barcode"""
    print("\n⚡ TESTE: Gerar Código Rápido")
    print("-" * 40)

    data = get_user_data()

    try:
        print(f"\n🔄 Gerando código rápido para: '{data}'")
        file = quick_barcode(data)

        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"\n✅ SUCESSO! PNG gerado: {file}")
            print(f"📊 Tamanho: {size} bytes")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def test_complete_barcode():
    """Testa a função generate_barcode com opções"""
    print("\n🔧 TESTE: Gerar Código Completo")
    print("-" * 40)

    data = get_user_data()

    # Opções avançadas
    print("\n⚙️ Opções avançadas:")
    print("1. Tipo: auto, code128, code39, ean13, ean8, upc")
    barcode_type = input("➤ Tipo de código (Enter=auto): ").strip() or 'auto'

    print("2. Formato: png, svg")
    output_format = input("➤ Formato (Enter=png): ").strip() or 'png'

    filename = input("➤ Nome do arquivo (Enter=automático): ").strip() or None

    try:
        print(f"\n🔄 Gerando código completo...")
        print(f"📊 Dados: '{data}' | Tipo: {barcode_type} | Formato: {output_format}")

        file = generate_barcode(
            data=data,
            output_format=output_format,
        )

        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"\n✅ SUCESSO! Arquivo gerado: {file}")
            print(f"📊 Tamanho: {size} bytes")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def test_visualize_barcode():
    """Testa a função visualize_barcode"""
    print("\n👁️ TESTE: Visualizar Código")
    print("-" * 40)

    data = get_user_data()

    try:
        print(f"\n🔄 Gerando código para visualização: '{data}'")
        file = visualize_barcode(data)

        if os.path.exists(file):
            size = os.path.getsize(file)
            print(f"\n✅ SUCESSO! PNG limpo gerado: {file}")
            print(f"📊 Tamanho: {size} bytes")
            print("💡 Este PNG é otimizado para exibição limpa (sem código SVG)")
        else:
            print("❌ Arquivo não foi criado")

    except Exception as e:
        print(f"❌ ERRO: {e}")


def configure_folder():
    """Configura pasta padrão"""
    print("\n📁 CONFIGURAR PASTA PADRÃO")
    print("-" * 40)

    print(f"📂 Pasta atual: {get_default_folder()}")

    new_folder = get_user_folder()

    try:
        set_default_folder(new_folder)
        print(f"✅ Pasta padrão atualizada: {get_default_folder()}")
    except Exception as e:
        print(f"❌ ERRO ao configurar pasta: {e}")


def list_barcodes():
    """Lista códigos gerados"""
    print("\n📋 CÓDIGOS GERADOS")
    print("-" * 40)

    try:
        files = list_generated_files()

        if not files:
            print("📭 Nenhum código de barras encontrado na pasta atual")
            print(f"📂 Pasta: {get_default_folder()}")
            return

        print(f"📂 Pasta: {get_default_folder()}")
        print(f"📊 Total: {len(files)} arquivo(s)")
        print("\n📋 Arquivos encontrados:")

        for i, file in enumerate(files, 1):
            name = os.path.basename(file)
            if os.path.exists(file):
                size = os.path.getsize(file)
                print(f"{i:2}. {name} ({size} bytes)")
            else:
                print(f"{i:2}. {name} (arquivo não encontrado)")

    except Exception as e:
        print(f"❌ ERRO ao listar: {e}")


def show_info():
    """Mostra informações do sistema"""
    print("\n ℹ️ INFORMAÇÕES DO SISTEMA")
    print("-" * 40)
    print(f"📂 Pasta padrão: {get_default_folder()}")
    print(f"📁 Pasta existe: {'✅ Sim' if os.path.exists(get_default_folder()) else '❌ Não'}")

    try:
        total_files = len(list_generated_files())
        print(f"📊 Total de códigos: {total_files}")
    except:
        print("📊 Total de códigos: Erro ao contar")


def main():
    """Função principal do teste"""
    print("🚀 Iniciando testador de código de barras...")

    # Configurar pasta inicial se necessário
    if not os.path.exists(get_default_folder()):
        print(f"📁 Criando pasta padrão: {get_default_folder()}")
        os.makedirs(get_default_folder(), exist_ok=True)

    while True:
        try:
            display_menu()
            option = input("\n➤ Escolha uma opção: ").strip()

            if option == '1':
                test_clean_barcode()
            elif option == '2':
                test_quick_barcode()
            elif option == '3':
                test_complete_barcode()
            elif option == '4':
                test_visualize_barcode()
            elif option == '5':
                configure_folder()
            elif option == '6':
                list_barcodes()
            elif option == '7':
                show_info()
            elif option == '0':
                print("\n👋 Encerrando testador...")
                print("✅ Obrigado por usar o gerador de código de barras!")
                break
            else:
                print(f"❌ Opção inválida: '{option}'")
                print("💡 Escolha um número de 0 a 7")

            # Pausa para ver resultado
            if option != '0':
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