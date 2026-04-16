#!/usr/bin/env python3
"""
Hook SessionStart — verifica requisitos e injeta contexto do projeto ativo.
"""

import json
import os
import sys

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.dirname(SCRIPT_DIR)

# ── 1. Verificar .env e FIGMA_ACCESS_TOKEN ─────────────────────────────────

env_path = os.path.join(REPO_ROOT, ".env")
env_example_path = os.path.join(REPO_ROOT, ".env.example")

token = os.environ.get("FIGMA_ACCESS_TOKEN", "").strip()

# Tenta ler do .env se não estiver no ambiente
if not token and os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("FIGMA_ACCESS_TOKEN="):
                token = line.split("=", 1)[1].strip()
                break

missing_env = not os.path.exists(env_path)
missing_token = not token

if missing_env or missing_token:
    issues = []

    if missing_env:
        issues.append(
            "**`.env` não encontrado.**\n"
            "Crie o arquivo copiando o exemplo:\n"
            "```bash\n"
            "cp .env.example .env\n"
            "```"
        )

    if missing_token:
        issues.append(
            "**`FIGMA_ACCESS_TOKEN` não está preenchido no `.env`.**\n\n"
            "Como gerar o token:\n"
            "1. Acesse figma.com → clique no seu avatar (canto superior direito)\n"
            "2. Vá em **Settings → Security → Personal access tokens**\n"
            "3. Clique em **Generate new token**\n"
            "4. Nome sugerido: `cortex-figma-agent`\n"
            "5. Marque os escopos obrigatórios:\n"
            "   - `file_content:write`\n"
            "   - `files:write`\n"
            "   - `file_comments:write`\n"
            "6. Clique em **Generate token** — ele aparece **apenas uma vez**, copie agora\n"
            "7. Cole no `.env`:\n"
            "   ```\n"
            "   FIGMA_ACCESS_TOKEN=figd_seu_token_aqui\n"
            "   ```\n"
            "8. **Reinicie o Claude Code** para que o MCP do Figma carregue o token."
        )

    context = "## ⚠️ SETUP NECESSÁRIO\n\n" + "\n\n---\n\n".join(issues)
    context += "\n\n---\n\nApós corrigir, reinicie o Claude Code nesta pasta."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": context
        }
    }))
    sys.exit(0)

# ── 2. Carregar projeto ativo ───────────────────────────────────────────────

ACTIVE_REF = os.path.join(REPO_ROOT, "projects", ".active")

if not os.path.exists(ACTIVE_REF):
    sys.exit(0)

with open(ACTIVE_REF) as f:
    project_path = f.read().strip()

if not os.path.isabs(project_path):
    project_path = os.path.join(REPO_ROOT, project_path)

if not os.path.exists(project_path):
    sys.exit(0)

with open(project_path, encoding="utf-8") as f:
    content = f.read()

project_rel = os.path.relpath(project_path, REPO_ROOT)
is_new = "(a definir)" in content

if is_new:
    instrucao = (
        "Este é um PROJETO NOVO. O arquivo tem campos a preencher.\n"
        "Antes de qualquer ação:\n"
        "1. Pergunte ao usuário qual a oferta (Geofusion, Growth, Brand, Reach ou Outros)\n"
        "2. Pergunte o objetivo da demanda em 1-2 frases\n"
        "3. Atualize o frontmatter do arquivo de projeto (oferta, prefixo) via Edit tool\n"
        "4. Só então prossiga com o fluxo normal de criação"
    )
else:
    instrucao = (
        "Este é um PROJETO EM ANDAMENTO. Leia o conteúdo abaixo e cumprimente o usuário "
        "mencionando o projeto pelo nome. Ofereça continuar de onde parou, "
        "resumindo brevemente o que já foi feito (elementos criados, última decisão)."
    )

context = f"""## PROJETO ATIVO

**Arquivo de acompanhamento:** `{project_rel}`

{instrucao}

Mantenha o arquivo de projeto atualizado durante toda a sessão:
- Ao criar o arquivo Figma: preencha `figma_file_id`, `figma_url` e `figma_nome`
- Ao criar cada página no Figma: adicione na seção "Páginas"
- Ao criar cada screen/modal/drawer/etc: adicione na tabela "Elementos criados"
- Ao tomar decisões com o usuário: adicione em "Requisitos e decisões"
- Ao encerrar: adicione entrada no "Histórico" e atualize o campo `atualizado` no frontmatter

---

{content}
"""

print(json.dumps({
    "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": context
    }
}))
