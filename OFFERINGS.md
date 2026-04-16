# Ofertas Cortex — Contexto para o Agente

Arquivo de referência com contexto sobre cada oferta da Cortex Intelligence.
Use este arquivo para entender o domínio, os usuários e os padrões de cada produto
antes de criar telas.

---

## Geofusion

**O que é:** Plataforma de inteligência geoespacial. Análise de territórios,
pontos de interesse (POIs), audiências e mobilidade urbana em mapas interativos.

**Usuário-alvo:** Analistas de geomarketing, planejadores de expansão, gestores de rede.

**Jornadas principais:**
- Análise de território e cobertura de rede
- Busca e avaliação de pontos de interesse (POIs)
- Configuração e monitoramento de alertas geográficos
- Geração de relatórios geoespaciais
- Importação e mapeamento de bases de dados próprias

**Padrões de tela identificados:**
- Canvas de mapa full-width como área principal (sem sidebar fixa)
- Header global: logo + breadcrumb/título da ferramenta + toolbar de ícones à direita
- Painel lateral direito contextual (~320px) para detalhe de entidade selecionada
- Toolbar flutuante do mapa (zoom, seleção, camadas, medição)
- Modal split para configuração: ~50% esquerda, mapa visível à direita
- Métricas em cards empilhados: ícone + valor numérico grande + label descritivo

**Projeto Figma:** https://www.figma.com/files/project/284089424

---

## Growth

**O que é:** Plataforma de expansão de carteira e prospecção B2B. Identifica oportunidades
de crescimento, analisa o perfil de clientes existentes e encontra empresas semelhantes
(lookalikes) para prospecção.

**Usuário-alvo:** Times de vendas, analistas de expansão comercial, gestores de CRM.

**Jornadas principais:**
- Criação de listas de prospecção por segmento e perfil
- Score e qualificação de leads com base em fit de cliente ideal (ICP)
- Visualização de oportunidades por território e verticais
- Enriquecimento de base com dados Cortex
- Exportação de listas para CRM (Salesforce, HubSpot, etc.)

**Padrões esperados:**
- Listas com score visual por linha
- Filtros avançados por atributo (setor, porte, região, CNAE)
- Cards de empresa com indicadores de fit
- Fluxos de configuração em etapas (wizard/stepper)

**Projeto Figma:** https://www.figma.com/files/project/43838342

---

## Brand

**O que é:** Plataforma de análise de presença de marca e mídia out-of-home (OOH).
Mede audiência, alcance e impacto de pontos de mídia no território urbano.

**Usuário-alvo:** Planejadores de mídia, analistas de marketing, gestores de marca.

**Jornadas principais:**
- Seleção e avaliação de pontos de mídia OOH (outdoors, painéis, mobiliário urbano)
- Análise de audiência e perfil demográfico de impacto
- Comparação de alternativas de mídia por localização e custo
- Planejamento de campanha com cobertura geográfica
- Relatórios de reach e frequência estimados

**Padrões esperados:**
- Mapa como base com pins de pontos de mídia
- Comparativo lado a lado de 2–3 pontos selecionados
- Gráficos de perfil demográfico (donut, barra horizontal)
- Métricas de alcance e impacto em destaque

**Projeto Figma:** https://www.figma.com/files/project/61425821

---

## Reach

**O que é:** Plataforma de engajamento e análise de performance de campanhas digitais.
Integra dados de tráfego, conversão e comportamento de audiência online.

**Usuário-alvo:** Analistas de marketing digital, gestores de performance, mídia paga.

**Jornadas principais:**
- Dashboard de performance de campanhas (sessões, conversão, rejeição)
- Análise de conversão por canal (orgânico, pago, social, direto)
- Comparativo de audiências e segmentos por período
- Análise de engajamento por landing page e campanha
- Exportação de relatórios de performance

**Padrões identificados:**
- Layout de dashboard: KPIs numéricos no topo + gráficos de tendência abaixo
- Filtros globais no topo: período, canal, feature, segmento
- Gráficos de linha/área para tendências temporais
- Gráficos de barra horizontal para comparativos por categoria
- Tabelas de performance com ranking e variação percentual
- Tipografia de display (REM) em valores numéricos grandes

**Projeto Figma:** https://www.figma.com/files/project/255743376

---

## Outros

**O que é:** Projetos internos, ferramentas transversais e iniciativas que não se
encaixam nas ofertas principais. Inclui componentes de plataforma, experiências de
onboarding, configurações globais, integrações e experimentos de produto.

**Usuário-alvo:** Varia por projeto — pode ser usuário final, cliente ou time interno.

**Contexto de uso:**
- Telas de onboarding e ativação (primeiro acesso às ofertas)
- Configurações de conta, times e permissões
- Integrações com sistemas externos (CRM, ERP, etc.)
- Protótipos e experimentos ainda sem oferta definida
- Componentes e padrões transversais entre ofertas

**Projeto Figma:** https://www.figma.com/files/project/43713678
