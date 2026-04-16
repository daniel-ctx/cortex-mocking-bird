# Skill: update-design-system

Atualiza os snapshots locais do design system Cortex buscando dados atualizados do arquivo Claude System.

**Acionar quando:** o usuário pedir "atualiza o design system", "refresh dos componentes", "sincroniza o DSR" ou similar.

---

## O que fazer

### 1. Buscar componentes (fileKey: 9zSZlgwQ9GvVB5et8VyRUj)

Execute as seguintes buscas via `search_design_system` com `fileKey=9zSZlgwQ9GvVB5et8VyRUj`:

```
queries de componentes:
- "button icon button floating"
- "input text field"
- "dropdown select multiselect"
- "checkbox radio toggle switch"
- "table grid data"
- "tab group navigation"
- "dialog modal"
- "tooltip snackbar banner alert notification"
- "avatar breadcrumb pagination stepper"
- "progress skeleton spinner loader"
- "chip tag badge label"
- "slider range"
- "date picker calendar"
- "card accordion panel"
- "topbar navbar sidebar header"
```

Para cada resultado, manter apenas os que pertencem à biblioteca:
- `Claude System`

### 2. Buscar tokens/variáveis (fileKey: 9zSZlgwQ9GvVB5et8VyRUj)

Execute as seguintes buscas com `includeVariables=true, includeStyles=true, includeComponents=false`:

```
queries de tokens:
- "color primary violet purple"
- "color neutral gray dark"
- "color success green"
- "color error danger red"
- "color warning yellow orange"
- "color info blue"
- "typography heading body label caption"
- "font size weight"
- "spacing padding margin"
- "radius border"
- "shadow elevation"
```

Manter apenas resultados da biblioteca:
- `Claude System`

### 3. Buscar ícones (fileKey: 9zSZlgwQ9GvVB5et8VyRUj)

Execute buscas com `includeComponents=true, includeStyles=false, includeVariables=false`:

```
queries de ícones:
- "arrow chevron"
- "check close"
- "user profile"
- "settings config"
- "filter sort"
- "download upload"
- "edit delete add"
- "location pin map"
- "chart graph analytics"
- "calendar date"
- "search"
- "warning alert info"
- "home dashboard"
- "lock unlock"
- "notification bell"
- "share export"
- "eye visibility"
- "star favorite"
- "refresh reload"
- "menu list"
```

Manter apenas resultados da biblioteca:
- `Claude System`

### 4. Atualizar os arquivos

Após coletar todos os dados:

1. **Atualizar** `design-system/components.json` — mesclar novos componentes, preservar categorias existentes, remover entradas obsoletas
2. **Atualizar** `design-system/tokens.json` — atualizar variáveis de cor e estilos encontrados
3. **Atualizar** `design-system/icons.json` — adicionar ícones novos encontrados
4. **Atualizar** o campo `_meta.updatedAt` nos três arquivos com a data atual
5. **NÃO alterar** `design-system/libraries.json` a menos que a biblioteca mude

### 5. Reportar

Ao final, listar:
- Quantos componentes novos foram adicionados
- Quantos tokens/variáveis novos foram adicionados
- Quantos ícones novos foram adicionados
- Algum item que aparecia antes mas não foi encontrado agora (possível remoção do Claude System)
