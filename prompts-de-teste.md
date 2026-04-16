# Prompts de teste — Cortex Figma Agent

Suite de validação para confirmar que o agente está configurado corretamente
antes de usar em demandas reais. Execute em ordem — cada nível depende do anterior.

---

## Nível 1 — Leitura e observação (valida acesso ao Figma)

Esses testes confirmam que o token está correto e o agente consegue ler os
arquivos de referência. Se falharem, o setup não está completo.

**Teste 1.1 — Claude System**
```
Leia o arquivo Claude System e liste 10 componentes disponíveis,
agrupados por categoria (ex: inputs, navegação, feedback, dados).
```
✅ Esperado: lista de componentes reais como Table, Button, Tab Group, Input Text, Menu Filter.
❌ Falha: componentes genéricos ou erro de acesso → verifique `FIGMA_ACCESS_TOKEN`.

**Teste 1.2 — Projeto de uma oferta**
```
Acesse o projeto Geofusion no Figma e liste os 5 arquivos modificados mais
recentemente, com data e uma frase descrevendo o que cada um parece ser.
```
✅ Esperado: lista com nomes reais de arquivos do projeto (ex: Pulso Urbano V1, Mobilidade V2).
❌ Falha: erro de acesso → sua conta Figma não tem acesso ao time Cortex.

**Teste 1.3 — Tokens do Claude System**
```
Leia o arquivo Claude System e liste as principais cores da paleta
com os hex codes, a família tipográfica principal e os tokens de espaçamento.
```
✅ Esperado: paleta com hexes reais (ex: `#540B6E`, `#009F7F`), fontes REM e Open Sans.
❌ Falha: valores arbitrários ou erro → problema no `FIGMA_SYSTEM_FILE_ID`.

---

## Nível 2 — Criação simples (valida escrita no Figma)

Esses testes confirmam que o agente consegue criar conteúdo no arquivo de trabalho.
Execute um de cada vez, verificando o resultado no Figma após cada prompt.

**Teste 2.1 — Modal de confirmação (Geofusion)**
```
Crie 2 variações de um modal de confirmação de exclusão de território salvo
no Geofusion. Variação A: padrão destrutivo com botão vermelho. Variação B:
abordagem mais suave com etapa de confirmação por digitação do nome.
```
✅ Esperado: 2 frames no `[GEO] Screen Builder — Rascunhos` com sticky notes.

**Teste 2.2 — Card de resultado (Growth)**
```
Crie 2 variações de um card de empresa em lista de prospecção no Growth.
Mostre: nome, segmento, cidade, score de fit e ações rápidas.
```
✅ Esperado: 2 frames no `[GRO] Screen Builder — Rascunhos`.

---

## Nível 3 — Criação a partir de contexto real

**Teste 3.1 — Geofusion (a partir de referência existente)**
```
Acesse o arquivo mais recente do projeto Geofusion. Identifique o padrão de
header e painel lateral. Com base nesses padrões, crie 2 variações de tela
para configuração de camadas de dados no mapa — o usuário ativa/desativa
camadas e ajusta parâmetros de visualização.
```

**Teste 3.2 — Reach (a partir de demanda descrita)**
```
Crie 3 variações de tela de comparativo de períodos para o Reach.
O usuário seleciona dois períodos e compara: sessões, taxa de conversão,
taxa de rejeição e conversão de meta. Variações devem ser arquiteturalmente
distintas (não apenas visuais).
```

**Teste 3.3 — Brand (com mapa + comparativo)**
```
Crie 2 variações de tela de seleção de pontos de mídia OOH para o Brand.
O usuário filtra por tipo de mídia, audiência mínima e raio de abrangência,
e seleciona pontos diretamente no mapa ou em lista.
```

---

## Nível 4 — Edição e iteração

**Teste 4.1 — Refinamento de variação**
```
Pegue a Variação A criada no Teste 2.1. Faça os seguintes ajustes:
- Aumente o espaçamento interno do modal para 32px
- Mova os botões para a esquerda
- Adicione um ícone de alerta no título
Documente as alterações no sticky note existente.
```

**Teste 4.2 — Consistência com padrão existente**
```
Compare a tela criada no Teste 3.1 com o padrão de header encontrado no
projeto Geofusion. Identifique 3 inconsistências e corrija no frame.
```

---

## Flags de problema

Se algum comportamento abaixo ocorrer, o setup tem um problema específico:

| Comportamento | Causa provável |
|---|---|
| Componentes genéricos (não do DSR) | Token sem `file_content:write` |
| Variações visualmente idênticas | Regras de variação não foram lidas pelo agente |
| Layers sem nome | `CLAUDE.md` não foi carregado corretamente |
| Agente não encontra arquivo de trabalho | `FIGMA_*_WORKING_FILE_ID` incorreto ou em branco |
| Agente pergunta qual oferta em todo prompt | Contexto não está claro — seja explícito no prompt |
| Erro "You don't have access" | Conta Figma sem acesso ao time Cortex |
