# 🔥 FOGUINHO - TikTok Streak Bot

Bot automatizado para manter seus streaks (foguinhos) do TikTok sempre acesos! 

## 📋 Funcionalidades

- ✅ Envia mensagens automáticas para manter streaks ativos
- 💖 Mensagens personalizadas para pessoas especiais
- ⚙️ Configurações flexíveis via JSON
- 🎨 Interface colorida no terminal
- 📸 Screenshot automático do resultado
- 🔒 Usa seus próprios cookies de autenticação

## 🚀 Instalação

### Pré-requisitos

- Python 3.8 ou superior
- Google Chrome instalado

### Passo a passo

1. Clone o repositório:
```bash
git clone https://github.com/eoshai/bot-foguinho-tiktok.git
cd bot-foguinho-tiktok
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 📝 Configuração

### 0. Configurar Arquivos Necessários

Primeiro, copie os arquivos de exemplo e renomeie-os:

```bash
cp cookies.example.json cookies.json
cp fogos.example.json fogos.json
cp config.example.json config.json
```

Ou no Windows:
```cmd
copy cookies.example.json cookies.json
copy fogos.example.json fogos.json
copy config.example.json config.json
```

### 1. Exportar Cookies do TikTok

Para que o bot funcione, você precisa exportar seus cookies de autenticação do TikTok:

1. Instale uma extensão de cookies no Chrome:
   - [EditThisCookie](https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg)
   - [Cookie-Editor](https://chrome.google.com/webstore/detail/cookie-editor/hlkenndednhfkekhgcdicdfddnkalmdm)

2. Acesse o TikTok e faça login

3. Clique na extensão e exporte os cookies em formato JSON

4. Cole o JSON exportado no arquivo `cookies.json` na raiz do projeto

### 2. Configurar Lista de Pessoas

Crie o arquivo `fogos.json` com os nomes das pessoas para quem quer enviar mensagens:

```json
[
  "usuario1",
  "usuario2",
  "usuario3"
]
```

**⚠️ IMPORTANTE:** Os nomes devem ser **exatamente** como aparecem no TikTok, incluindo emojis se houver!

### 3. Personalizar Configurações (Opcional)

Edite o arquivo `config.json` para personalizar o comportamento:

```json
{
  "mensagem_padrao": "🔥 Acende nosso foguinho aee - 🤖",
  "pessoas_especiais": {
    "usuario1": "💖",
    "usuario2": "E aí mano! 🔥"
  },
  "delay_entre_mensagens": 2.0,
  "usar_headless": false,
  "tempo_espera_load": 15,
  "screenshot_final": true
}
```

#### Opções de Configuração:

- **mensagem_padrao**: Mensagem padrão enviada para todos
- **pessoas_especiais**: Dicionário com mensagens personalizadas para pessoas específicas
- **delay_entre_mensagens**: Tempo (em segundos) entre cada mensagem enviada
- **usar_headless**: Se `true`, roda sem abrir janela do navegador
- **tempo_espera_load**: Tempo de espera para carregar a página
- **screenshot_final**: Se `true`, tira screenshot ao final

## 🎯 Uso

Execute o script:

```bash
python main.py
```

O bot irá:
1. Abrir o TikTok com suas credenciais
2. Acessar suas mensagens diretas
3. Procurar pelas pessoas da lista `fogos.json`
4. Enviar as mensagens configuradas
5. Salvar um screenshot do resultado

## 📁 Estrutura de Arquivos

```
foguinho-tiktok/
│
├── main.py                 # Script principal
├── config.json             # Configurações personalizáveis
├── fogos.json              # Lista de pessoas para enviar
├── cookies.json            # Seus cookies do TikTok (não commitar!)
├── requirements.txt        # Dependências Python
├── .gitignore             # Arquivos ignorados pelo Git
└── README.md              # Este arquivo
```

## ⚠️ Avisos Importantes

- **Cookies Privados**: NUNCA compartilhe seu `cookies.json`! Este arquivo contém suas credenciais de acesso.
- **Uso Responsável**: Use o bot de forma responsável e respeite os termos de serviço do TikTok.
- **Rate Limiting**: O TikTok pode detectar atividade automatizada. Use delays adequados.
- **Manutenção**: Você precisará atualizar os cookies periodicamente quando expirarem.

## 🔒 Segurança

O arquivo `cookies.json` está no `.gitignore` para evitar que você acidentalmente exponha suas credenciais. **NUNCA** faça commit deste arquivo!

## 🐛 Solução de Problemas

### "Não foi possível encontrar os contatos"
- Verifique se está logado corretamente
- Aumente o `tempo_espera_load` no config.json
- Tente rodar com `usar_headless: false` para ver o que está acontecendo

### "Erro ao add cookie"
- Certifique-se de que exportou os cookies corretamente
- Verifique se os cookies não expiraram
- Tente exportar novamente fazendo logout e login no TikTok

### Bot não envia mensagens
- Verifique se os nomes em `fogos.json` estão exatamente como no TikTok
- Aumente o delay entre mensagens
- Verifique se tem conversas ativas com essas pessoas

## 📜 Licença

MIT License - veja o arquivo LICENSE para detalhes

## 👨‍💻 Desenvolvedor

Desenvolvido por **Shai**

---

**⭐ Se este projeto te ajudou, deixe uma estrela no GitHub!**
