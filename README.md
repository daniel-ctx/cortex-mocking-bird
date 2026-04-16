# Cortex Figma Agent

Agente Claude Code para criação autônoma de telas no Figma para todas as ofertas Cortex.

A partir de um prompt, PRD ou descrição, o agente lê o design system, consulta telas
existentes da oferta e gera 2–3 variações de tela com qualidade de produção diretamente
no Figma — sem abrir o Figma, sem arrastar componente, sem montar frame.

**Ofertas suportadas:** Geofusion · Growth · Brand · Reach · Outros

---

## Pré-requisitos

| Requisito | Versão mínima | Como obter |
|---|---|---|
| Claude Code | última | [claude.ai/download](https://claude.ai/download) ou `npm install -g @anthropic-ai/claude-code` |
| Node.js | 18+ | [nodejs.org](https://nodejs.org) (necessário para o MCP do Figma via `npx`) |
| Conta Figma com acesso ao time Cortex | — | Solicite ao admin do Figma da Cortex |

---

## Setup

### 1. Clonar o repositório

```bash
git clone https://github.com/daniel-ctx/cortex-figma-agent.git
cd cortex-figma-agent
```

### 2. Criar o `.env`

```bash
cp .env.example .env
```

Abra `.env` e preencha o `FIGMA_ACCESS_TOKEN`:

```
FIGMA_ACCESS_TOKEN=figd_seu_token_aqui
```

**Como gerar o token:**
1. Acesse figma.com → clique no seu avatar → **Settings → Security → Personal access tokens**
2. Clique em **Generate new token**, nome sugerido: `cortex-figma-agent`
3. Marque os escopos: `file_content:write` · `files:write` · `file_comments:write`
4. Clique em **Generate token** — aparece **apenas uma vez**, copie agora

### 3. Abrir no Claude Code

```bash
claude
```

O agente está pronto. Se algum requisito estiver faltando, ele avisará diretamente no chat.

---

## Validando o setup

Antes de usar em demandas reais, confirme que o agente consegue ler os arquivos de referência:

```
Leia o arquivo Claude System e liste os 5 componentes mais relevantes
para telas de dashboard.
```

**Resultado esperado:** lista de componentes reais do Claude System (ex: Table, Button, Tab Group, Input Text).

**Se retornar erro ou componentes genéricos:** verifique se `FIGMA_ACCESS_TOKEN` está correto no `.env`
e reinicie o Claude Code.

Mais testes em [`prompts-de-teste.md`](./prompts-de-teste.md).

---

## Como usar

Descreva a demanda em linguagem natural. Especifique a oferta se não estiver óbvio pelo contexto.

O agente vai:
1. Identificar a oferta e confirmar o entendimento
2. Ler os snapshots locais do design system (`design-system/`) — sem chamadas desnecessárias à API
3. Consultar telas existentes da oferta como referência
4. Propor 2–3 variações arquiteturalmente distintas
5. Criar os frames no arquivo de trabalho (especificado por você ou criado automaticamente)
6. Documentar o racional em sticky notes ao lado de cada variação
7. Atualizar o arquivo de projeto local em `projects/`

---

## Protótipo HTML

Use `/prototype` para gerar um HTML navegável a partir de qualquer design no Figma.

```
/prototype https://www.figma.com/design/...
```

O agente lê a estrutura do arquivo, mapeia os componentes para classes Tailwind usando os tokens
Cortex e gera um `index.html` self-contained — sem servidor, sem build, abre direto no browser.

**Output:**
```
prototypes/{oferta-kebab}-{descricao-kebab}-{dd-mm-aaaa}/
  index.html
```

**Abrir localmente:**
```bash
open prototypes/{pasta}/index.html
```

**Gerar URL local para compartilhar:**
```bash
npx serve prototypes/{pasta}
```

Os arquivos de referência do design system usados pelo protótipo ficam em `design-system/`:

| Arquivo | Papel |
|---|---|
| `html-bridge.json` | Mapeamento componente Figma → HTML+Tailwind |
| `cortex-components.css` | Classes semânticas (`.btn-primary`, `.input-text`, etc.) |
| `cortex-tailwind-config.js` | Tokens de cor, tipografia e espaçamento Cortex |

O bridge cresce a cada protótipo gerado — componentes novos são adicionados automaticamente.

### Exemplos de prompt por oferta

**Geofusion**
```
Crie 2 variações de tela para o fluxo de criação de alerta de mobilidade.
O usuário define: área geográfica, tipo de evento, threshold e canal de notificação.
```

**Growth**
```
Preciso de uma tela de resultados de prospecção. O usuário vê uma lista de leads
ranqueados com filtros por segmento, região e porte de empresa. Score visual por linha.
```

**Brand**
```
Crie uma tela de comparativo de pontos de mídia OOH. O usuário seleciona até 3 pontos
e vê lado a lado: audiência estimada, perfil demográfico e custo por impacto.
```

**Reach**
```
O dashboard principal do Reach precisa de revisão. Acesse o arquivo mais recente
do projeto e proponha 2 variações com melhor hierarquia de KPIs e filtros.
```

---

## Estrutura do repositório

```
cortex-figma-agent/
├── CLAUDE.md                    # Instruções persistentes do agente (não edite sem intenção)
├── OFFERINGS.md                 # Contexto sobre cada oferta Cortex
├── README.md                    # Este arquivo
├── prompts-de-teste.md          # Suite de testes para validar o setup
├── .mcp.json                    # Configuração do servidor MCP do Figma
├── .env.example                 # Template de variáveis de ambiente
├── .env                         # Suas credenciais (nunca commitar)
├── design-system/               # Snapshots locais do Claude System + tokens HTML
│   ├── components.json          # Componentes: chave, importMethod, variantProperties
│   ├── tokens.json              # Tokens de cor, tipografia e espaçamento
│   ├── icons.json               # Ícones disponíveis e hints de busca
│   ├── libraries.json           # Chaves e prioridade das bibliotecas
│   ├── figma-api-notes.md       # Gotchas da Plugin API (enums, import, fontes)
│   ├── html-bridge.json         # Mapeamento componente Figma → HTML+Tailwind
│   ├── cortex-components.css    # Classes semânticas para protótipos HTML
│   └── cortex-tailwind-config.js# Tokens Cortex para Tailwind CDN
├── prototypes/                  # Protótipos HTML gerados por /prototype
├── projects/                    # Tracking de projetos ativos
│   └── .active                  # Path do arquivo de projeto da sessão atual
└── .claude/
    ├── settings.json            # Permissões e hooks do Claude Code
    ├── load-project.py          # Hook SessionStart: verifica requisitos + carrega projeto
    ├── protect-figma-refs.py    # Hook PreToolUse: bloqueia escrita no design system
    └── skills/
        ├── update-design-system.md
        └── prototype.md         # Skill /prototype → HTML navegável
```

---

## Snapshots do design system

O agente lê os snapshots em `design-system/` antes de qualquer chamada à API do Figma.
Para atualizar com os dados mais recentes do Claude System:

```
/update-design-system
```

---

## Tracking de projetos

Cada demanda tem um arquivo `.md` em `projects/` com todo o histórico: arquivo Figma vinculado,
páginas criadas, elementos gerados com node IDs, decisões tomadas e log de sessões.

O hook `SessionStart` carrega esse contexto automaticamente — o agente retoma de onde parou
sem briefing manual.

---

## Regras importantes

- O agente **nunca edita** o arquivo Claude System — bloqueio técnico ativo
- O agente **nunca edita** os projetos das ofertas — apenas lê como referência
- Novos arquivos Figma são criados nos **Drafts** do usuário (limitação do MCP) — mova manualmente para o projeto da oferta no Figma se necessário
- Mantenha o `.env` fora do controle de versão (`.gitignore` já cuida disso)

---

## Problemas comuns

**MCP do Figma não conecta / ferramentas Figma não aparecem**
→ O token no `.env` está errado ou vazio. Corrija e reinicie o Claude Code.

**"You don't have access to this file"**
→ Sua conta Figma não tem acesso ao time Cortex. Solicite ao admin.

**Agente lista componentes genéricos, não do Claude System**
→ O token não tem os escopos corretos (`file_content:write`). Regenere com os escopos certos.

**Contexto de projeto não carregou**
→ Verifique se `projects/.active` aponta para um arquivo `.md` existente.
