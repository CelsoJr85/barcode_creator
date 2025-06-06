# 📊 Gerador de Código de Barras Python

Uma biblioteca Python completa e fácil de usar para gerar códigos de barras de alta qualidade, com suporte a múltiplos formatos e exibição otimizada.

## ✨ Características

- 🎯 **Detecção Automática**: Identifica o melhor tipo de código automaticamente
- 📱 **Múltiplos Formatos**: PNG, SVG, HTML e Base64
- 🔧 **Exibição Limpa**: Gera códigos otimizados para visualização sem código SVG
- 📁 **Pasta Configurável**: Sistema de pasta padrão personalizável
- 🛠️ **Interface de Teste**: Aplicação completa para testar todas as funcionalidades
- ✅ **Validado**: Testado com Google Lens e leitores reais

## 🚀 Instalação

```bash
# Clone o repositório
git clone https://github.com/CelsoJr85/barcode_creator
cd barcode-creator

# Crie um ambiente virtual (recomendado)
python -m venv venv

# Ative o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instale as dependências
pip install -r requirements.txt

# OU instale manualmente
pip install python-barcode[images]
```

## 📋 Tipos de Código Suportados

| Tipo | Descrição | Uso Recomendado |
|------|-----------|-----------------|
| **CODE128** | Números, letras e símbolos | Uso geral, mais versátil |
| **CODE39** | Números, letras maiúsculas | Etiquetas industriais |
| **EAN13** | 13 dígitos | Produtos comerciais |
| **EAN8** | 8 dígitos | Produtos pequenos |
| **UPC** | 12 dígitos | Produtos americanos |
| **AUTO** | Detecta automaticamente | Recomendado para iniciantes |

## 🎯 Uso Rápido

### Exemplo Básico

```python
from barcode_creator import visualizar_codigo

# Gera PNG limpo para exibição (pasta padrão)
arquivo = visualizar_codigo("123456789")
print(f"Código gerado: {arquivo}")

# Gera na sua pasta preferida
arquivo = visualizar_codigo("123456789", pasta_destino='C:/MeusProjetos/Barcodes')
```

### Exemplo Completo

```python
from barcode_creator import gerar_codigo_limpo, definir_pasta_padrao

# Configurar pasta padrão para sua preferência
definir_pasta_padrao('C:/Users/SeuNome/Documents/MeusBarcodes')

# Gerar código com múltiplos formatos
resultado = gerar_codigo_limpo("PRODUTO-ABC123")

print(f"PNG: {resultado['png']}")
print(f"HTML: {resultado['html']}")  
print(f"Base64: {resultado['base64']}")
```

## 🔧 Funções Principais

### `visualizar_codigo(dados, pasta_destino=None)`
**Recomendada para exibição** - Gera PNG limpo otimizado.

```python
# Uso básico (pasta padrão)
png_file = visualizar_codigo("Hello World")

# Com pasta específica do usuário
png_file = visualizar_codigo("123456", "C:/Users/SeuNome/Desktop")
png_file = visualizar_codigo("123456", "/home/usuario/meus_barcodes")  # Linux
png_file = visualizar_codigo("123456", "./minha_pasta")                # Relativo
```

### `gerar_codigo_limpo(dados, pasta_destino=None)`
**Melhor para projetos web** - Gera PNG + HTML + Base64.

```python
resultado = gerar_codigo_limpo("PRODUTO-2025")
# resultado['png'] -> arquivo PNG
# resultado['html'] -> página HTML estilizada  
# resultado['base64'] -> código para embed HTML
```

### `gerar_codigo_barras(dados, tipo_codigo='auto', formato_saida='png', ...)`
**Função completa** com todas as opções avançadas.

```python
arquivo = gerar_codigo_barras(
    dados="Custom Code",
    tipo_codigo='code128',
    formato_saida='svg',
    nome_arquivo='meu_codigo',
    opcoes_customizacao={'module_height': 20}
)
```

### `codigo_barras_rapido(dados, pasta_destino=None)`
**Para uso simples** - Gera PNG rapidamente.

```python
arquivo = codigo_barras_rapido("987654321")
```

## 🛠️ Interface de Teste

Execute o testador interativo para experimentar todas as funcionalidades:

```bash
python teste.py
```

### Menu do Testador

- **1️⃣ Código Limpo** - PNG + HTML + Base64 (recomendado)
- **2️⃣ Código Rápido** - PNG simples  
- **3️⃣ Código Completo** - Todas as opções avançadas
- **4️⃣ Visualizar Código** - PNG otimizado para exibição
- **5️⃣ Configurar Pasta** - Define pasta padrão
- **6️⃣ Listar Códigos** - Mostra arquivos gerados
- **7️⃣ Mostrar Info** - Informações do sistema

## 📁 Configuração de Pasta

### Método 1: Configurar Pasta Padrão (Recomendado)

```python
from barcode_generator import definir_pasta_padrao, obter_pasta_padrao

# Definir pasta padrão (persiste para todas as chamadas)
definir_pasta_padrao('./meus_codigos')
# ou Windows: definir_pasta_padrao('C:/MeusProjetos/Barcodes')
# ou Linux/Mac: definir_pasta_padrao('/home/usuario/barcodes')

# Verificar pasta atual
print(f"Pasta padrão: {obter_pasta_padrao()}")

# Todas as funções usarão esta pasta automaticamente
codigo = visualizar_codigo("123456")  # Salva na pasta padrão
```

### Método 2: Especificar Pasta Para Cada Função

```python
# Windows - Exemplos de caminhos
arquivo = visualizar_codigo("123456", pasta_destino='C:/Users/SeuNome/Documents/Barcodes')
arquivo = visualizar_codigo("123456", pasta_destino='D:/Projetos/CodigoBarras')

# Linux/Mac - Exemplos de caminhos  
arquivo = visualizar_codigo("123456", pasta_destino='/home/usuario/barcodes')
arquivo = visualizar_codigo("123456", pasta_destino='~/Desktop/codigos')

# Caminho relativo (funciona em qualquer sistema)
arquivo = visualizar_codigo("123456", pasta_destino='./minha_pasta')
arquivo = visualizar_codigo("123456", pasta_destino='../barcodes')
```

### Método 3: Editar Pasta Padrão no Código

**Para definir sua pasta favorita permanentemente:**

1. Abra o arquivo `barcode_creator.py`
2. Localize a linha: `_PASTA_PADRAO = './codigos_barras'`
3. Altere para sua pasta preferida:

```python
# Exemplos de alteração:
_PASTA_PADRAO = 'C:/MeusProjetos/Barcodes'        # Windows
_PASTA_PADRAO = '/home/usuario/barcodes'          # Linux  
_PASTA_PADRAO = '/Users/usuario/Desktop/barcodes' # Mac
_PASTA_PADRAO = './meus_codigos'                  # Relativo
```

4. Salve o arquivo - agora esta será a pasta padrão sempre!

## 🌐 Exibição em HTML

### Usando Base64 (Embed)

```html
<!-- Código gerado pela função gerar_codigo_limpo() -->
<img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAA..." alt="Barcode">
```

### Usando Arquivo PNG

```html
<img src="barcode_123456789.png" alt="Código de Barras" style="max-width: 100%;">
```

### Usando HTML Completo

A função `gerar_codigo_limpo()` cria um arquivo HTML estilizado pronto para uso:

```html
<!DOCTYPE html>
<html>
<head>
    <title>Código de Barras</title>
    <!-- CSS incluso automaticamente -->
</head>
<body>
    <div class="container">
        <h2>Código de Barras</h2>
        <div class="barcode">
            <img src="barcode.png" alt="Código de Barras">
        </div>
        <div class="info">
            <div class="code">123456789</div>
        </div>
    </div>
</body>
</html>
```

## 📊 Exemplos de Entrada

| Entrada | Tipo Detectado | Resultado |
|---------|---------------|-----------|
| `"123456789012"` | EAN13 | Código de produto |
| `"12345678"` | EAN8 | Produto pequeno |
| `"PRODUTO-ABC"` | CODE39 | Código alfanumérico |
| `"Hello World!"` | CODE128 | Texto com símbolos |
| `"987654321098"` | UPC | Produto americano |

## ✅ Validação e Compatibilidade

✅ **Testado com Google Lens** - Leitura perfeita  
✅ **Compatível com scanners profissionais**  
✅ **Padrões da indústria** - EAN, UPC, Code128, Code39  
✅ **Qualidade de produção** - Pronto para uso comercial  

## 💡 Dicas de Configuração

### Para Windows
```python
# Exemplos comuns de pastas no Windows
definir_pasta_padrao('C:/Users/SeuNome/Documents/Barcodes')
definir_pasta_padrao('D:/Projetos/CodigoBarras') 
definir_pasta_padrao('C:/Temp/Barcodes')
```

### Para Linux/Mac
```python
# Exemplos comuns de pastas no Linux/Mac
definir_pasta_padrao('/home/usuario/barcodes')
definir_pasta_padrao('~/Desktop/codigos')
definir_pasta_padrao('/tmp/barcodes')
```

### Caminhos Relativos (Funcionam em qualquer sistema)
```python
definir_pasta_padrao('./meus_codigos')      # Pasta na mesma localização
definir_pasta_padrao('../barcodes')         # Pasta no diretório pai
definir_pasta_padrao('output/barcodes')     # Subpasta
```

### ⚠️ Importante
- As pastas são criadas automaticamente se não existirem
- Use `/` em vez de `\` nos caminhos (funciona em Windows, Linux e Mac)
- Para caminhos com espaços no Windows: `'C:/Program Files/Meu App/Barcodes'`

- Python 3.7+
- python-barcode[images]
- PIL/Pillow (incluso no python-barcode[images])

## 📝 Estrutura do Projeto

```
projeto/
├── barcode_creator.py        # Biblioteca principal
├── teste.py                 # Interface de teste
├── requirements.txt         # Dependências do projeto
├── .gitignore              # Exclusões do Git
├── README.md               # Este arquivo
└── codigos_barras/         # Pasta padrão (criada automaticamente)
    ├── barcode_*.png       # Arquivos PNG gerados
    ├── barcode_*.html      # Arquivos HTML gerados
    └── barcode_*.svg       # Arquivos SVG gerados
```

## 🎨 Customização Avançada

```python
# Opções de customização para aparência
opcoes = {
    'module_width': 0.3,      # Largura das barras
    'module_height': 20,      # Altura das barras  
    'quiet_zone': 5,          # Zona de silêncio
    'font_size': 12,          # Tamanho da fonte
    'text_distance': 5        # Distância do texto
}

arquivo = gerar_codigo_barras(
    "Custom Code",
    opcoes_customizacao=opcoes
)
```

## 🐛 Tratamento de Erros

```python
try:
    arquivo = visualizar_codigo("dados-inválidos-para-ean13")
except ValueError as e:
    print(f"Erro de validação: {e}")
except Exception as e:
    print(f"Erro geral: {e}")
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie sua feature branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -am 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

- **Problemas**: Abra uma issue no GitHub
- **Dúvidas**: Use as discussions do repositório
- **Email**: [seu-email@exemplo.com]

## 🚀 Próximas Funcionalidades

- [ ] Suporte a QR Code
- [ ] Batch processing (múltiplos códigos)
- [ ] Integração com bases de dados
- [ ] API REST
- [ ] Interface gráfica (GUI)

---

**⭐ Se este projeto foi útil, deixe uma estrela no GitHub!**
