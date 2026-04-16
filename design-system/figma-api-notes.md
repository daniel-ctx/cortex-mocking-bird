# Figma Plugin API — Notas e Gotchas

Referência rápida para evitar erros recorrentes ao escrever código para `use_figma`.

---

## Auto-layout — PROIBIDO

**Nunca use auto-layout.** Não defina `layoutMode`, `primaryAxisSizingMode`, `counterAxisSizingMode`,
`layoutSizingHorizontal`, `layoutSizingVertical`, `primaryAxisAlignItems`, `counterAxisAlignItems`,
`itemSpacing`, `paddingLeft`, `paddingRight`, `paddingTop` ou `paddingBottom`.

Essas propriedades causam erros em runtime difíceis de rastrear (ex: `HUG can only be set on
auto-layout frames`) e produzem layouts frágeis. Todo posicionamento é feito com coordenadas
absolutas e `resize()`.

**Posicionamento manual (padrão obrigatório):**
```js
// Posicionar com x, y e dimensões explícitas — sempre
node.x = 24;
node.y = 16;
node.resize(200, 40);

// Para empilhar itens verticalmente, calcule o y acumulado:
let currentY = 0;
for (const item of items) {
  item.y = currentY;
  currentY += item.height + 8; // 8px de gap
}
```

---

## Importar componentes de bibliotecas externas

> **OBRIGATÓRIO**: todo elemento de UI deve vir do Claude System via instância.
> Nunca crie botões, inputs, checkboxes ou qualquer componente catalogado do zero com shapes.
> Leia `design-system/components.json` para obter a `componentKey` e o `importMethod` corretos.

| `type` no snapshot | Método correto |
|---|---|
| `"component_set"` | `await figma.importComponentSetByKeyAsync(key)` → retorna o set; use `.defaultVariant` para criar instância |
| `"component"` | `await figma.importComponentByKeyAsync(key)` → retorna o componente diretamente; chame `.createInstance()` |

**Nunca** use `importComponentByKeyAsync` para um `component_set` — vai lançar "Component not found".

### Padrão de uso — componentes mais comuns

```js
// ─── Button (component_set) ────────────────────────────────────────────────
const btnSet = await figma.importComponentSetByKeyAsync("04ccbe877e820d6da2eb4704e02d8d50fb5cf534");
const btn = btnSet.defaultVariant.createInstance();
btn.setProperties({ "Type": "Primary", "State": "Enabled" });
// Editar label:
const btnLabel = btn.findOne(n => n.type === 'TEXT' && n.characters.length > 0);
if (btnLabel) {
  await figma.loadFontAsync(btnLabel.fontName);
  btnLabel.characters = "Entrar";
}
btn.x = 24; btn.y = 200;
parent.appendChild(btn);

// ─── Input Text (component_set) ────────────────────────────────────────────
const inputSet = await figma.importComponentSetByKeyAsync("f76dac609f20065612b011b089543ad585c10ba3");
const input = inputSet.defaultVariant.createInstance();
// Editar placeholder:
const placeholder = input.findOne(n => n.type === 'TEXT');
if (placeholder) {
  await figma.loadFontAsync(placeholder.fontName);
  placeholder.characters = "E-mail";
}
input.x = 24; input.y = 80;
parent.appendChild(input);

// ─── Checkbox (component_set) ──────────────────────────────────────────────
const cbSet = await figma.importComponentSetByKeyAsync("92189b912d65f5788e2b1393937280fa80c59e8c");
const cb = cbSet.defaultVariant.createInstance();
cb.x = 24; cb.y = 160;
parent.appendChild(cb);

// ─── Dialog (component — não é component_set) ──────────────────────────────
const dialogComp = await figma.importComponentByKeyAsync("c2f86c06ef3c5ef34b659259c586b102f054c643");
const dialog = dialogComp.createInstance();
dialog.x = 400; dialog.y = 100;
parent.appendChild(dialog);
```

### Posicionamento após importar

Instâncias do Claude System têm tamanho próprio — não chame `resize()` a não ser que precise escalar.
Use `x` e `y` para posicionar dentro do frame pai.

---

## Fontes: sempre carregar antes de escrever

```js
await figma.loadFontAsync({ family: "REM", style: "SemiBold" });
// só então:
text.fontName = { family: "REM", style: "SemiBold" };
text.characters = "Título";
```

Para nós de texto dentro de instâncias de componente:
```js
const textNode = instance.findOne(n => n.type === 'TEXT');
await figma.loadFontAsync(textNode.fontName as FontName);
textNode.characters = "Novo label";
```

---

## Mudar página ativa

```js
// ERRADO — não suportado:
figma.currentPage = outraPage;

// CORRETO:
await figma.setCurrentPageAsync(outraPage);
```

---

## Variantes de componente: setProperties

```js
// Descobrir propriedades disponíveis (só para debug, não usar em produção):
console.log(Object.keys(instance.componentProperties));

// Aplicar variante direto quando props são conhecidas (preferir este):
instance.setProperties({ "Type": "Primary", "State": "Enabled" });
```

Props do Button Claude System (verificado em 2026-04-15):
- `Type`: `"Primary"` | `"Secondary"` | `"Ghost"` | `"Danger"`
- `State`: `"Enabled"` | `"Hovered"` | `"Focused"` | `"Disabled"`

---

## Stroke align

```js
frame.strokeAlign = 'INSIDE';  // não afeta o tamanho externo
frame.strokeAlign = 'OUTSIDE';
frame.strokeAlign = 'CENTER';
```

---

## Efeitos (sombra)

```js
frame.effects = [{
  type: 'DROP_SHADOW',
  color: { r: 0, g: 0, b: 0, a: 0.08 },
  offset: { x: 0, y: 2 },
  radius: 8,
  spread: 0,
  visible: true,
  blendMode: 'NORMAL'
}];
```

---

## Sticky notes — padrão sem corte

Frames de sticky note DEVEM ter `clipsContent = false`, caso contrário o texto é cortado.
Sempre ajuste a altura do frame ao conteúdo real depois de adicionar os textos.

```js
// ─── Sticky note correto ──────────────────────────────────────────────────────
const sticky = figma.createFrame();
sticky.name = "frame/design-note";
sticky.clipsContent = false;                        // OBRIGATÓRIO
sticky.fills = [{ type: 'SOLID', color: { r: 1, g: 0.98, b: 0.78 } }];
sticky.effects = [{
  type: 'DROP_SHADOW',
  color: { r: 0, g: 0, b: 0, a: 0.08 },
  offset: { x: 0, y: 4 }, radius: 12, spread: 0,
  visible: true, blendMode: 'NORMAL'
}];

// Posição: 80px à direita do frame principal, alinhado ao topo
sticky.x = screen.x + screen.width + 80;
sticky.y = screen.y;
sticky.resize(360, 40);  // altura mínima, será ajustada
page.appendChild(sticky);

await figma.loadFontAsync({ family: "Open Sans", style: "SemiBold" });
const noteTitle = figma.createText();
noteTitle.name = "text/note-title";
noteTitle.fontName = { family: "Open Sans", style: "SemiBold" };
noteTitle.fontSize = 13;
noteTitle.textAutoResize = "WIDTH_AND_HEIGHT";
noteTitle.characters = "Racional de design";
noteTitle.fills = [{ type: 'SOLID', color: { r: 0.2, g: 0.2, b: 0.2 } }];
noteTitle.x = 20; noteTitle.y = 20;
sticky.appendChild(noteTitle);

await figma.loadFontAsync({ family: "Open Sans", style: "Regular" });
const noteBody = figma.createText();
noteBody.name = "text/note-body";
noteBody.fontName = { family: "Open Sans", style: "Regular" };
noteBody.fontSize = 12;
noteBody.lineHeight = { value: 18, unit: "PIXELS" };
noteBody.textAutoResize = "HEIGHT";   // largura fixa, altura cresce
noteBody.resize(320, 40);
noteBody.characters = "Texto do racional...";
noteBody.fills = [{ type: 'SOLID', color: { r: 0.25, g: 0.25, b: 0.25 } }];
noteBody.x = 20;
noteBody.y = noteTitle.y + noteTitle.height + 8;
sticky.appendChild(noteBody);

// OBRIGATÓRIO: ajustar altura do sticky após definir o conteúdo
sticky.resize(360, noteBody.y + noteBody.height + 24);
```

---

## Hierarquia de página — título, subtítulo e screens

Background, títulos e screens seguem uma hierarquia vertical obrigatória com gaps de 300px.
Sempre calcule posições dinamicamente — nunca use offsets fixos.

```js
// ─── 1. Background da página (fazer uma vez por página) ──────────────────────
page.backgrounds = [{ type: 'SOLID', color: { r: 0.18, g: 0.18, b: 0.18 } }]; // #2E2E2E

// ─── 2. Título do tema (REM 300, branco) ─────────────────────────────────────
await figma.loadFontAsync({ family: "REM", style: "Regular" });
const flowTitle = figma.createText();
flowTitle.name = "text/flow-title";
flowTitle.fontName = { family: "REM", style: "Regular" };
flowTitle.fontSize = 300;
flowTitle.textAutoResize = "WIDTH_AND_HEIGHT";
flowTitle.characters = "NOME DO FLUXO";
flowTitle.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }]; // #fff
flowTitle.x = 80;
flowTitle.y = 80;
page.appendChild(flowTitle);

// ─── 3. Subtítulo da variação (REM 300, branco, 300px abaixo do título) ──────
const varTitle = figma.createText();
varTitle.name = "text/variation-title";
varTitle.fontName = { family: "REM", style: "Regular" };
varTitle.fontSize = 300;
varTitle.textAutoResize = "WIDTH_AND_HEIGHT";
varTitle.characters = "VARIAÇÃO A — SPLIT PANEL";
varTitle.fills = [{ type: 'SOLID', color: { r: 1, g: 1, b: 1 } }]; // #fff
varTitle.x = 80;
varTitle.y = flowTitle.y + flowTitle.height + 300; // 300px abaixo do bottom do título
page.appendChild(varTitle);

// ─── 4. Screen (300px abaixo do bottom do subtítulo) ─────────────────────────
screen.x = 80;
screen.y = varTitle.y + varTitle.height + 300;
page.appendChild(screen);

// ─── 5. Telas adicionais do mesmo fluxo: 150px à direita ─────────────────────
nextScreen.x = screen.x + screen.width + 150;
nextScreen.y = screen.y;
page.appendChild(nextScreen);
```

> ⚠️ Com REM 300, a altura renderizada é ~380px. Sempre leia `text.height` após definir `characters` — nunca assuma valor fixo. O título do tema aparece uma única vez por página; o subtítulo aparece antes de cada variação.

---

## Quando chamar search_design_system

**Não chamar** apenas para verificar se uma chave do snapshot está correta.
Chamar **somente se**:
1. `importComponentSetByKeyAsync` / `importComponentByKeyAsync` lançar erro explícito
2. O componente necessário não existir em `components.json`
3. O usuário solicitar `/update-design-system`
