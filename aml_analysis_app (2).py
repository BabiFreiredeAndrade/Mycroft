import streamlit as st
import json
import datetime
import uuid
from pathlib import Path

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Mycroft NuPay",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

/* ── Globals ── */
html, body, [class*="css"] {
    font-family: 'IBM Plex Sans', sans-serif;
}

/* ── Background ── */
.stApp {
    background-color: #0d0f14;
    color: #e2e8f0;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #111318;
    border-right: 1px solid #1e2330;
}
section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] label {
    color: #8892a4;
    font-size: 0.78rem;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}

/* ── Header card ── */
.header-card {
    background: linear-gradient(135deg, #1a1f2e 0%, #141824 100%);
    border: 1px solid #2a3040;
    border-left: 4px solid #6366f1;
    border-radius: 8px;
    padding: 20px 28px;
    margin-bottom: 24px;
}
.header-card h1 {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.5rem;
    color: #e2e8f0;
    margin: 0 0 4px 0;
    letter-spacing: -0.02em;
}
.header-card p {
    color: #6b7a99;
    font-size: 0.85rem;
    margin: 0;
}
.badge {
    display: inline-block;
    background: #2a1a4a;
    color: #a78bfa;
    border: 1px solid #4c3285;
    border-radius: 4px;
    padding: 2px 10px;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.06em;
    margin-right: 8px;
}
.badge-red { background: #2a1010; color: #f87171; border-color: #7f1d1d; }
.badge-green { background: #0d2a1a; color: #4ade80; border-color: #14532d; }
.badge-yellow { background: #2a2010; color: #fbbf24; border-color: #78350f; }

/* ── Section headers ── */
.section-title {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: #6366f1;
    border-bottom: 1px solid #1e2330;
    padding-bottom: 8px;
    margin: 28px 0 18px 0;
}

/* ── Cards ── */
.info-card {
    background: #141824;
    border: 1px solid #1e2330;
    border-radius: 6px;
    padding: 16px 20px;
    margin-bottom: 12px;
}
.info-card label {
    font-size: 0.72rem;
    color: #6b7a99;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    display: block;
    margin-bottom: 4px;
}
.info-card .value {
    font-size: 0.95rem;
    color: #e2e8f0;
    font-weight: 500;
}

/* ── Risk indicators ── */
.risk-high { color: #f87171; font-weight: 600; }
.risk-medium { color: #fbbf24; font-weight: 600; }
.risk-low { color: #4ade80; font-weight: 600; }

/* ── Metric boxes ── */
.metric-row {
    display: flex;
    gap: 12px;
    margin-bottom: 20px;
}
.metric-box {
    flex: 1;
    background: #141824;
    border: 1px solid #1e2330;
    border-radius: 6px;
    padding: 14px 16px;
    text-align: center;
}
.metric-box .metric-val {
    font-family: 'IBM Plex Mono', monospace;
    font-size: 1.6rem;
    font-weight: 600;
    line-height: 1;
}
.metric-box .metric-label {
    font-size: 0.7rem;
    color: #6b7a99;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-top: 4px;
}

/* ── Streamlit widget overrides ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div > div {
    background-color: #141824 !important;
    border: 1px solid #2a3040 !important;
    border-radius: 5px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: #6366f1 !important;
    box-shadow: 0 0 0 2px rgba(99,102,241,0.15) !important;
}
.stSelectbox > div > div > div:hover {
    border-color: #6366f1 !important;
}

/* ── Buttons ── */
.stButton > button {
    background-color: #6366f1 !important;
    color: #fff !important;
    border: none !important;
    border-radius: 5px !important;
    font-family: 'IBM Plex Sans', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 8px 22px !important;
    transition: background 0.2s !important;
}
.stButton > button:hover {
    background-color: #4f46e5 !important;
}
.stButton > button[kind="secondary"] {
    background-color: #1e2330 !important;
    color: #a0aec0 !important;
}

/* ── Radio / checkbox ── */
.stRadio label, .stCheckbox label {
    color: #c4cdd8 !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background-color: #141824 !important;
    border: 1px solid #1e2330 !important;
    border-radius: 5px !important;
    color: #e2e8f0 !important;
    font-family: 'IBM Plex Mono', monospace !important;
    font-size: 0.82rem !important;
    letter-spacing: 0.04em !important;
}

/* ── Divider ── */
hr { border-color: #1e2330 !important; }

/* ── Labels ── */
.stTextInput label, .stTextArea label, .stSelectbox label,
.stRadio label > div, .stDateInput label {
    color: #8892a4 !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
}

/* ── Success / warning / error boxes ── */
.stSuccess { background: #0d2a1a !important; border-color: #14532d !important; }
.stWarning { background: #2a2010 !important; border-color: #78350f !important; }
.stError   { background: #2a1010 !important; border-color: #7f1d1d !important; }

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111318;
    border-bottom: 1px solid #1e2330;
    gap: 2px;
}
.stTabs [data-baseweb="tab"] {
    background: transparent;
    color: #6b7a99;
    border-radius: 0;
    font-family: 'IBM Plex Mono', monospace;
    font-size: 0.78rem;
    letter-spacing: 0.06em;
    padding: 10px 20px;
}
.stTabs [aria-selected="true"] {
    background: transparent !important;
    color: #e2e8f0 !important;
    border-bottom: 2px solid #6366f1 !important;
}

/* ── Number input ── */
.stNumberInput input {
    background-color: #141824 !important;
    border: 1px solid #2a3040 !important;
    color: #e2e8f0 !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: #0d0f14; }
::-webkit-scrollbar-thumb { background: #2a3040; border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: #3a4050; }
</style>
""", unsafe_allow_html=True)

# ── Session state init ─────────────────────────────────────────────────────
if "casos" not in st.session_state:
    st.session_state.casos = {}
if "current_caso" not in st.session_state:
    st.session_state.current_caso = None
if "socios" not in st.session_state:
    st.session_state.socios = [{}]

# ── Helpers ───────────────────────────────────────────────────────────────
def novo_caso_id():
    return str(uuid.uuid4())[:8].upper()

def calcular_risco(kyc, socios, mlro_dec):
    score = 0
    flags = []

    # PEP check
    for s in socios:
        if s.get("pep") == "Sim":
            score += 30
            flags.append("Sócio PEP identificado")
        if s.get("midia_negativa") == "Sim":
            score += 25
            flags.append("Mídia negativa em sócio")

    if kyc.get("regiao_fronteiricia") == "Sim":
        score += 20
        flags.append("Região fronteiriça")
    if kyc.get("midia_negativa") == "Sim":
        score += 25
        flags.append("Mídia negativa na empresa")

    cap = kyc.get("faturamento", 0)
    if cap > 10_000_000:
        score += 10
        flags.append("Alto faturamento declarado")

    if mlro_dec and mlro_dec not in ["N/A", "Aprovado", ""]:
        score += 15

    nivel = "ALTO" if score >= 50 else "MÉDIO" if score >= 25 else "BAIXO"
    return score, nivel, flags

# ── SIDEBAR ───────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🔍 MYCROFT NUPAY")
    st.markdown("---")

    st.markdown("**NAVEGAÇÃO**")
    pagina = st.radio(
        "",
        ["📋 Novo Caso", "🚨 Fator Gerador", "🗂️ Casos Salvos", "📊 Dashboard"],
        label_visibility="collapsed",
    )

    st.markdown("---")
    st.markdown(f"**CASOS ATIVOS:** `{len(st.session_state.casos)}`")

    if st.session_state.casos:
        st.markdown("**RECENTES**")
        for cid, c in list(st.session_state.casos.items())[-5:]:
            cnpj = c.get("kyc", {}).get("cnpj", "—")
            nivel = c.get("risco_nivel", "—")
            cor = {"ALTO": "🔴", "MÉDIO": "🟡", "BAIXO": "🟢"}.get(nivel, "⚪")
            if st.button(f"{cor} {cnpj[:14]}", key=f"nav_{cid}", use_container_width=True):
                st.session_state.current_caso = cid

    st.markdown("---")
    st.caption("Mycroft NuPay · AML · Lote 2026")

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: NOVO CASO
# ─────────────────────────────────────────────────────────────────────────────
if "Novo" in pagina:

    st.markdown("""
    <div class="header-card">
        <h1>🔍 Mycroft NuPay — Nova Análise AML</h1>
        <p>Preencha os dados do caso. Todos os campos marcados são obrigatórios para gerar o parecer.</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([
        "01 · KYC EMPRESA",
        "02 · QUADRO SOCIETÁRIO",
        "03 · DECISÃO MLRO",
        "04 · PARECER ANALISTA",
    ])


    # ── TAB 1: KYC ────────────────────────────────────────────────────────
    with tab1:
        st.markdown('<div class="section-title">Identificação</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            cnpj = st.text_input("CNPJ *", placeholder="00.000.000/0000-00")
            razao_social = st.text_input("Razão Social *", placeholder="Ex: EMPRESA LTDA.")
            nome_fantasia = st.text_input("Nome Fantasia", placeholder="(opcional)")
        with col2:
            data_fund = st.date_input(
                "Data de Fundação",
                value=datetime.date(2020, 1, 1),
                min_value=datetime.date(1900, 1, 1),
            )
            nat_juridica = st.selectbox(
                "Natureza Jurídica",
                ["Sociedade Limitada (LTDA)", "SA Aberta", "SA Fechada", "EIRELI", "MEI", "Outra"],
            )
            porte = st.selectbox(
                "Porte",
                ["Micro", "Pequeno Porte", "Médio Porte", "Grande Porte"],
            )

        st.markdown('<div class="section-title">Atividade Econômica</div>', unsafe_allow_html=True)

        col1, col2 = st.columns([1, 2])
        with col1:
            cnae = st.text_input("CNAE Primário", placeholder="0000-0/00")
        with col2:
            desc_cnae = st.text_input("Descrição CNAE", placeholder="Descrição da atividade")

        desc_atividade = st.text_area(
            "Descrição da Atividade da Empresa *",
            height=100,
            placeholder="Descreva detalhadamente a atividade exercida pela empresa...",
        )

        st.markdown('<div class="section-title">Capacidade Financeira</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            capital_social = st.number_input(
                "Capital Social (R$)", min_value=0.0, step=1000.0, format="%.2f"
            )
        with col2:
            faturamento = st.number_input(
                "Faturamento Presumido (R$)", min_value=0.0, step=10000.0, format="%.2f"
            )

        st.markdown('<div class="section-title">Localização & Fachada</div>', unsafe_allow_html=True)

        endereco = st.text_input(
            "Endereço Completo",
            placeholder="Rua, número, complemento, bairro, cidade, estado, CEP",
        )

        col1, col2 = st.columns(2)
        with col1:
            regiao_front = st.selectbox("Região Fronteiriça?", ["Não", "Sim"])
            link_fachada = st.text_input("Link Fachada (Maps)", placeholder="https://...")
        with col2:
            desc_fachada = st.text_area("Descrição da Fachada", height=80)
            data_foto = st.text_input("Data da Foto (MM/AAAA)", placeholder="Ex: Março/2023")

        st.markdown('<div class="section-title">Tipo de Cliente</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            tipo_cliente = st.selectbox(
                "Tipo de Cliente *",
                [
                    "Fintech de Pagamentos",
                    "Fintech de Crédito",
                    "Banco / Instituição Financeira",
                    "Câmbio / Remessas",
                    "Comércio Varejista",
                    "Comércio Atacadista",
                    "Marketplace",
                    "Prestação de Serviços",
                    "Indústria",
                    "Holding / Investimentos",
                    "ONG / Associação",
                    "Outro",
                ],
            )
        with col2:
            subtipo_cliente = st.text_input("Subtipo / Segmento", placeholder="Ex: Pagamentos cross-border, Crédito consignado...")

        st.markdown('<div class="section-title">Website & Redes Sociais</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            website = st.text_input("Website", placeholder="https://www.empresa.com.br")
            linkedin = st.text_input("LinkedIn", placeholder="https://linkedin.com/company/...")
        with col2:
            instagram = st.text_input("Instagram", placeholder="https://instagram.com/...")
            outras_redes = st.text_input("Outras redes sociais", placeholder="Facebook, Twitter/X, YouTube...")

        desc_website_redes = st.text_area(
            "Descrição do Website e Redes Sociais",
            height=100,
            placeholder=(
                "Descreva o conteúdo do website e redes sociais: coerência com a atividade declarada, "
                "qualidade das informações, presença de produtos/serviços, data de criação, "
                "número de seguidores, regularidade de publicações, etc."
            ),
        )

        st.markdown('<div class="section-title">Mídia Negativa</div>', unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col1:
            midia_neg_emp = st.selectbox("Mídia Negativa (empresa)?", ["Não", "Sim", "N/A"])
        with col2:
            tipo_kyc = st.selectbox(
                "Tipo de KYC", ["Elaboração do KYC", "Reutilização de KYC", "Atualização"]
            )
        with col3:
            link_kyc = st.text_input("Link KYC anterior", placeholder="https://... (se reutilização)")

        if midia_neg_emp == "Sim":
            col1, col2 = st.columns(2)
            with col1:
                midia_fonte = st.text_input(
                    "Fonte(s) da mídia negativa",
                    placeholder="Ex: G1, UOL, Reclame Aqui, Diário Oficial...",
                )
                midia_data_pub = st.text_input(
                    "Data de publicação", placeholder="Ex: Janeiro/2024"
                )
            with col2:
                midia_tipo = st.multiselect(
                    "Tipo de ocorrência",
                    [
                        "Fraude / Estelionato",
                        "Lavagem de Dinheiro",
                        "Evasão Fiscal",
                        "Reclamações de consumidores",
                        "Processo judicial",
                        "Sanção regulatória",
                        "Corrupção / Improbidade",
                        "Outro",
                    ],
                )
            midia_desc = st.text_area(
                "Descrição da mídia negativa *",
                height=100,
                placeholder="Descreva detalhadamente as ocorrências encontradas, links de referência e impacto na análise de risco...",
            )
        else:
            midia_fonte = ""
            midia_data_pub = ""
            midia_tipo = []
            midia_desc = ""

        obs_kyc = st.text_area("Observações adicionais (KYC)", height=80)

    # ── TAB 2: SÓCIOS ─────────────────────────────────────────────────────
    with tab2:
        st.markdown('<div class="section-title">Quadro de Sócios e Administradores</div>', unsafe_allow_html=True)

        n_socios = st.number_input(
            "Número de sócios/administradores", min_value=1, max_value=20, value=1, step=1
        )

        # Ensure list length
        while len(st.session_state.socios) < n_socios:
            st.session_state.socios.append({})
        while len(st.session_state.socios) > n_socios:
            st.session_state.socios.pop()

        for i in range(int(n_socios)):
            with st.expander(f"SÓCIO / ADMINISTRADOR {i+1}", expanded=(i == 0)):
                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.socios[i]["nome"] = st.text_input(
                        "Nome *", key=f"s_nome_{i}", placeholder="Nome completo"
                    )
                    st.session_state.socios[i]["cpf_cnpj"] = st.text_input(
                        "CPF / CNPJ *", key=f"s_doc_{i}", placeholder="000.000.000-00"
                    )
                    st.session_state.socios[i]["qualificacao"] = st.selectbox(
                        "Qualificação",
                        ["Sócio Administrador", "Sócio", "Administrador", "Diretor", "Procurador"],
                        key=f"s_qual_{i}",
                    )
                with col2:
                    st.session_state.socios[i]["participacao"] = st.text_input(
                        "Participação (%)", key=f"s_part_{i}", placeholder="Ex: 50%"
                    )
                    st.session_state.socios[i]["pep"] = st.selectbox(
                        "PEP (Pessoa Exposta Politicamente)?",
                        ["Não", "Sim"],
                        key=f"s_pep_{i}",
                    )
                    st.session_state.socios[i]["midia_negativa"] = st.selectbox(
                        "Mídia Negativa?", ["Não", "Sim", "N/A"], key=f"s_midia_{i}"
                    )

                col1, col2 = st.columns(2)
                with col1:
                    st.session_state.socios[i]["conta_nubank"] = st.selectbox(
                        "Conta Nubank?", ["Não", "Sim"], key=f"s_nu_{i}"
                    )
                    st.session_state.socios[i]["marcadores_risco"] = st.selectbox(
                        "Marcadores de Risco",
                        ["N/A", "Baixo", "Médio", "Alto"],
                        key=f"s_risco_{i}",
                    )
                with col2:
                    st.session_state.socios[i]["resumo_conta"] = st.text_area(
                        "Resumo da Conta Nubank",
                        key=f"s_resumo_{i}",
                        height=80,
                        placeholder="Descreva o perfil transacional...",
                    )

    # ── TAB 3: MLRO ───────────────────────────────────────────────────────
    with tab3:
        st.markdown('<div class="section-title">Decisão MLRO (SE APLICÁVEL)</div>', unsafe_allow_html=True)

        mlro_aplicavel = st.selectbox(
            "MLRO aplicável a este caso?", ["Não (N/A)", "Sim"]
        )

        mlro_dec = "N/A"
        mlro_resp = ""
        mlro_data = None
        mlro_obs = ""

        if mlro_aplicavel == "Sim":
            col1, col2 = st.columns(2)
            with col1:
                mlro_dec = st.selectbox(
                    "Decisão *",
                    ["Pendente", "Aprovado", "Aprovado com ressalvas", "Reprovado", "Em análise"],
                )
                mlro_resp = st.text_input("Responsável MLRO", placeholder="Nome do analista MLRO")
            with col2:
                mlro_data = st.date_input("Data da Decisão", value=datetime.date.today())
                mlro_score = st.selectbox(
                    "Score de Risco MLRO", ["Baixo", "Médio", "Alto", "Crítico"]
                )

            mlro_obs = st.text_area(
                "Observações MLRO *",
                height=120,
                placeholder="Descreva os fundamentos da decisão MLRO...",
            )

            st.markdown('<div class="section-title">Alertas & Indicadores</div>', unsafe_allow_html=True)
            col1, col2, col3 = st.columns(3)
            with col1:
                alerta_estruturacao = st.checkbox("Estruturação suspeita")
                alerta_smurfing = st.checkbox("Smurfing")
            with col2:
                alerta_layering = st.checkbox("Layering")
                alerta_pep = st.checkbox("Operações com PEP")
            with col3:
                alerta_int = st.checkbox("Transações internacionais atípicas")
                alerta_caixa = st.checkbox("Movimentações em espécie")

    # ── TAB 4: PARECER ────────────────────────────────────────────────────
    with tab4:
        st.markdown('<div class="section-title">Parecer do Analista</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            analista_nome = st.text_input("Nome do Analista *", placeholder="Nome completo")
            analista_data = st.date_input("Data do Parecer", value=datetime.date.today())
        with col2:
            decisao_final = st.selectbox(
                "Decisão Final *",
                [
                    "Selecione...",
                    "✅ Aprovado",
                    "✅ Aprovado com monitoramento",
                    "⚠️ Aprovado com ressalvas",
                    "🔴 Reprovado",
                    "🔄 Encaminhar para MLRO",
                    "📋 Aguardando documentação",
                ],
            )
            nivel_risco_manual = st.selectbox(
                "Nível de Risco Avaliado", ["Baixo", "Médio", "Alto", "Crítico"]
            )

        parecer_texto = st.text_area(
            "Parecer Detalhado *",
            height=180,
            placeholder=(
                "Descreva sua análise: contexto do cliente, movimentações identificadas, "
                "riscos observados, diligências realizadas e fundamentação da decisão..."
            ),
        )

        st.markdown('<div class="section-title">Diligências Realizadas</div>', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            dil_receita = st.checkbox("Consulta Receita Federal")
            dil_maps = st.checkbox("Verificação fachada (Maps)")
            dil_pep = st.checkbox("Consulta PEP")
        with col2:
            dil_midia = st.checkbox("Pesquisa mídia negativa")
            dil_scr = st.checkbox("Consulta SCR/Bacen")
            dil_siscoaf = st.checkbox("SISCOAF")
        with col3:
            dil_caf = st.checkbox("CAF / Biometria")
            dil_docs = st.checkbox("Documentação societária OK")
            dil_visita = st.checkbox("Visita presencial")

        recomendacoes = st.text_area(
            "Recomendações de Monitoramento",
            height=80,
            placeholder="Ex: Monitorar transações acima de R$ 50.000 por 6 meses...",
        )

    # ── SAVE BUTTON ────────────────────────────────────────────────────────
    st.markdown("---")
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        salvar = st.button("💾  SALVAR E GERAR ANÁLISE", use_container_width=True)
    with col2:
        limpar = st.button("🗑️  Limpar Formulário", use_container_width=True)

    if salvar:
        if not cnpj or not razao_social or not desc_atividade:
            st.error("⚠️  Preencha os campos obrigatórios: CNPJ, Razão Social e Descrição da Atividade.")
        elif decisao_final == "Selecione...":
            st.error("⚠️  Selecione a Decisão Final na aba Parecer do Analista.")
        elif not analista_nome:
            st.error("⚠️  Informe o nome do analista.")
        else:
            kyc_data = {
                "cnpj": cnpj,
                "razao_social": razao_social,
                "nome_fantasia": nome_fantasia,
                "data_fundacao": str(data_fund),
                "nat_juridica": nat_juridica,
                "porte": porte,
                "cnae": cnae,
                "desc_cnae": desc_cnae,
                "desc_atividade": desc_atividade,
                "tipo_cliente": tipo_cliente,
                "subtipo_cliente": subtipo_cliente,
                "capital_social": capital_social,
                "faturamento": faturamento,
                "endereco": endereco,
                "regiao_fronteiricia": regiao_front,
                "link_fachada": link_fachada,
                "desc_fachada": desc_fachada,
                "website": website,
                "linkedin": linkedin,
                "instagram": instagram,
                "outras_redes": outras_redes,
                "desc_website_redes": desc_website_redes,
                "midia_negativa": midia_neg_emp,
                "midia_fonte": midia_fonte,
                "midia_data_pub": midia_data_pub,
                "midia_tipo": midia_tipo,
                "midia_desc": midia_desc,
                "tipo_kyc": tipo_kyc,
                "obs": obs_kyc,
            }

            score, nivel, flags = calcular_risco(
                kyc_data,
                st.session_state.socios,
                mlro_dec,
            )

            caso_id = novo_caso_id()
            st.session_state.casos[caso_id] = {
                "id": caso_id,
                "criado_em": str(datetime.datetime.now()),
                "kyc": kyc_data,
                "socios": list(st.session_state.socios),
                "mlro": {
                    "aplicavel": mlro_aplicavel,
                    "decisao": mlro_dec,
                    "responsavel": mlro_resp,
                    "obs": mlro_obs,
                },
                "parecer": {
                    "analista": analista_nome,
                    "data": str(analista_data),
                    "decisao": decisao_final,
                    "nivel_risco": nivel_risco_manual,
                    "texto": parecer_texto,
                    "recomendacoes": recomendacoes,
                },
                "risco_score": score,
                "risco_nivel": nivel,
                "risco_flags": flags,
            }
            st.session_state.current_caso = caso_id
            st.success(f"✅  Caso **{caso_id}** salvo com sucesso! Risco calculado: **{nivel}** (score {score})")

            # Show risk summary
            if flags:
                st.warning("🚩 Fatores de risco identificados: " + " · ".join(flags))

    if limpar:
        st.session_state.socios = [{}]
        st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: FATOR GERADOR DO ALERTA
# ─────────────────────────────────────────────────────────────────────────────
elif "Fator" in pagina:

    st.markdown("""
    <div class="header-card">
        <h1>🚨 Mycroft NuPay — Fator Gerador do Alerta</h1>
        <p>Registre a origem, tipologia e contexto do alerta que motivou esta análise AML.</p>
    </div>
    """, unsafe_allow_html=True)

    # Vincular a caso existente (opcional)
    st.markdown('<div class="section-title">Vínculo com Caso</div>', unsafe_allow_html=True)

    casos_opcoes = {"— Nenhum (registro avulso) —": None}
    for cid, c in st.session_state.casos.items():
        label = f"[{cid}] {c['kyc']['razao_social']} — {c['kyc']['cnpj']}"
        casos_opcoes[label] = cid

    caso_vinculado_label = st.selectbox("Vincular a caso existente", list(casos_opcoes.keys()))
    caso_vinculado_id = casos_opcoes[caso_vinculado_label]

    st.markdown('<div class="section-title">Origem do Alerta</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        origem_alerta = st.selectbox(
            "Origem do Alerta *",
            [
                "Selecione...",
                "Sistema de Monitoramento Transacional (STM)",
                "Regra Automática (Motor de Regras)",
                "Denúncia Interna",
                "Denúncia Externa / Whistleblower",
                "COAF / SISCOAF",
                "Bacen / Regulatório",
                "Polícia Federal / MP",
                "Interpol / OFAC / Lista Restritiva",
                "Parceiro Comercial",
                "Revisão Periódica KYC",
                "Análise de Carteira",
                "Outro",
            ],
        )
        id_alerta = st.text_input("ID / Número do Alerta", placeholder="Ex: ALT-2026-00123")
        data_alerta = st.date_input("Data do Alerta", value=datetime.date.today())
    with col2:
        sistema_origem = st.text_input(
            "Sistema / Ferramenta de Origem",
            placeholder="Ex: Hawk AI, NICE Actimize, interno...",
        )
        prioridade = st.selectbox(
            "Prioridade do Alerta",
            ["Crítica", "Alta", "Média", "Baixa"],
        )
        status_alerta = st.selectbox(
            "Status do Alerta",
            ["Em Análise", "Pendente", "Escalado para MLRO", "Encerrado — Falso Positivo", "Encerrado — Suspeito Confirmado"],
        )

    st.markdown('<div class="section-title">Tipologia do Alerta</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        tipologia_principal = st.selectbox(
            "Tipologia Principal *",
            [
                "Selecione...",
                "Estruturação / Fracionamento (Smurfing)",
                "Layering — Camadas de transações",
                "Integração de recursos ilícitos",
                "Operações com PEP sem justificativa",
                "Transações internacionais atípicas",
                "Movimentações em espécie incompatíveis",
                "Uso de laranjas / Interpostas pessoas",
                "Evasão Fiscal / Sonegação",
                "Financiamento ao Terrorismo (FT)",
                "Proliferação de Armas (FPArmas)",
                "Corrupção / Suborno",
                "Fraude / Estelionato",
                "Inconsistência com perfil declarado",
                "Outro",
            ],
        )
        tipologias_secundarias = st.multiselect(
            "Tipologias Secundárias",
            [
                "Estruturação / Fracionamento",
                "Layering",
                "Operações com PEP",
                "Transações internacionais atípicas",
                "Movimentações em espécie",
                "Uso de laranjas",
                "Evasão Fiscal",
                "Financiamento ao Terrorismo",
                "Fraude",
                "Inconsistência de perfil",
                "Outro",
            ],
        )
    with col2:
        regra_disparada = st.text_input(
            "Regra / Score Disparado",
            placeholder="Ex: Regra 47 — Fracionamento > R$10k, Score 850...",
        )
        threshold_valor = st.number_input(
            "Valor Transacionado em Alerta (R$)", min_value=0.0, step=1000.0, format="%.2f"
        )
        periodo_analisado = st.text_input(
            "Período Analisado", placeholder="Ex: Jan/2025 – Mar/2025 (90 dias)"
        )

    st.markdown('<div class="section-title">Descrição do Fator Gerador</div>', unsafe_allow_html=True)

    descricao_fator = st.text_area(
        "Descrição Detalhada do Fator Gerador *",
        height=160,
        placeholder=(
            "Descreva com detalhes o que originou o alerta: padrão de transações identificado, "
            "comportamento atípico observado, inconsistências entre perfil declarado e movimentações reais, "
            "contrapartes envolvidas, canais utilizados, datas e valores relevantes..."
        ),
    )

    st.markdown('<div class="section-title">Contrapartes & Contexto</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        n_transacoes = st.number_input("Nº de Transações Suspeitas", min_value=0, step=1)
        contrapartes = st.text_area(
            "Contrapartes Identificadas",
            height=90,
            placeholder="Liste CPFs/CNPJs ou nomes das contrapartes envolvidas...",
        )
    with col2:
        canais = st.multiselect(
            "Canais Utilizados",
            ["PIX", "TED", "DOC", "Boleto", "Cartão", "Câmbio", "Crypto", "Espécie", "Outro"],
        )
        jurisdicoes = st.text_input(
            "Jurisdições Envolvidas",
            placeholder="Ex: Brasil, Ilhas Cayman, Panamá...",
        )

    st.markdown('<div class="section-title">Evidências & Documentos</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        link_evidencia = st.text_input("Link / Referência da Evidência", placeholder="https://...")
        link_relatorio = st.text_input("Link Relatório Transacional", placeholder="https://...")
    with col2:
        obs_evidencia = st.text_area("Observações sobre as Evidências", height=80,
            placeholder="Detalhes sobre screenshots, extratos, registros de sistema...")

    st.markdown('<div class="section-title">Encaminhamento</div>', unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    with col1:
        encaminhar_mlro = st.checkbox("Escalar para MLRO")
        comunicar_coaf = st.checkbox("Comunicar ao COAF")
    with col2:
        bloquear_conta = st.checkbox("Sugerir bloqueio de conta")
        solicitar_docs = st.checkbox("Solicitar documentação ao cliente")
    with col3:
        encerrar_rel = st.checkbox("Recomendar encerramento de relacionamento")
        monitoramento_intenso = st.checkbox("Monitoramento intensificado")

    encaminhamento_obs = st.text_area(
        "Justificativa do Encaminhamento",
        height=80,
        placeholder="Fundamente a decisão de encaminhamento...",
    )

    st.markdown("---")
    col1, col2 = st.columns([2, 1])
    with col1:
        salvar_fg = st.button("💾  SALVAR FATOR GERADOR", use_container_width=True)

    if salvar_fg:
        if origem_alerta == "Selecione..." or tipologia_principal == "Selecione...":
            st.error("⚠️  Preencha a Origem do Alerta e a Tipologia Principal.")
        elif not descricao_fator:
            st.error("⚠️  A Descrição do Fator Gerador é obrigatória.")
        else:
            fg_data = {
                "caso_vinculado": caso_vinculado_id,
                "origem": origem_alerta,
                "id_alerta": id_alerta,
                "data": str(data_alerta),
                "sistema": sistema_origem,
                "prioridade": prioridade,
                "status": status_alerta,
                "tipologia_principal": tipologia_principal,
                "tipologias_secundarias": tipologias_secundarias,
                "regra": regra_disparada,
                "valor": threshold_valor,
                "periodo": periodo_analisado,
                "descricao": descricao_fator,
                "n_transacoes": n_transacoes,
                "contrapartes": contrapartes,
                "canais": canais,
                "jurisdicoes": jurisdicoes,
                "encaminhamento": {
                    "mlro": encaminhar_mlro,
                    "coaf": comunicar_coaf,
                    "bloqueio": bloquear_conta,
                    "docs": solicitar_docs,
                    "encerrar": encerrar_rel,
                    "monitoramento": monitoramento_intenso,
                    "obs": encaminhamento_obs,
                },
            }

            # Attach to case if linked
            if caso_vinculado_id and caso_vinculado_id in st.session_state.casos:
                st.session_state.casos[caso_vinculado_id]["fator_gerador"] = fg_data
                st.success(f"✅ Fator Gerador salvo e vinculado ao caso **{caso_vinculado_id}**.")
            else:
                if "fatores_geradores" not in st.session_state:
                    st.session_state.fatores_geradores = []
                st.session_state.fatores_geradores.append(fg_data)
                st.success("✅ Fator Gerador salvo como registro avulso.")

            # Summary card
            cor_prio = {"Crítica": "🔴", "Alta": "🟠", "Média": "🟡", "Baixa": "🟢"}.get(prioridade, "⚪")
            st.info(
                f"{cor_prio} **{tipologia_principal}** · Origem: {origem_alerta} · "
                f"Valor: R$ {threshold_valor:,.2f} · Status: {status_alerta}"
            )

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: CASOS SALVOS
# ─────────────────────────────────────────────────────────────────────────────
elif "Casos" in pagina:

    st.markdown("""
    <div class="header-card">
        <h1>🗂️ Mycroft NuPay — Casos Salvos</h1>
        <p>Histórico de análises AML realizadas nesta sessão.</p>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.casos:
        st.info("Nenhum caso salvo ainda. Use 'Novo Caso' para iniciar uma análise.")
    else:
        for cid, caso in st.session_state.casos.items():
            nivel = caso.get("risco_nivel", "—")
            score = caso.get("risco_score", 0)
            cor_badge = {"ALTO": "badge-red", "MÉDIO": "badge-yellow", "BAIXO": "badge-green"}.get(nivel, "badge")
            cnpj_ = caso["kyc"]["cnpj"]
            razao_ = caso["kyc"]["razao_social"]
            decisao_ = caso["parecer"]["decisao"]
            analista_ = caso["parecer"]["analista"]
            data_ = caso["criado_em"][:16]

            with st.expander(f"[{cid}]  {razao_}  —  {cnpj_}", expanded=False):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown(f"**CNPJ:** `{cnpj_}`")
                    st.markdown(f"**Razão Social:** {razao_}")
                    st.markdown(f"**Porte:** {caso['kyc']['porte']}")
                with col2:
                    st.markdown(f"**Decisão:** {decisao_}")
                    st.markdown(f"**Analista:** {analista_}")
                    st.markdown(f"**Data:** {data_}")
                with col3:
                    st.markdown(
                        f"**Nível de Risco:** "
                        f"<span class='risk-{'high' if nivel=='ALTO' else 'medium' if nivel=='MÉDIO' else 'low'}'>{nivel}</span> "
                        f"(score: {score})",
                        unsafe_allow_html=True,
                    )
                    if caso["risco_flags"]:
                        for f in caso["risco_flags"]:
                            st.markdown(f"🚩 {f}")

                # Full JSON export
                if st.button("📄 Ver JSON completo", key=f"json_{cid}"):
                    st.json(caso)

                if st.button("🗑️ Remover caso", key=f"del_{cid}"):
                    del st.session_state.casos[cid]
                    st.rerun()

# ─────────────────────────────────────────────────────────────────────────────
#  PAGE: DASHBOARD
# ─────────────────────────────────────────────────────────────────────────────
elif "Dashboard" in pagina:

    st.markdown("""
    <div class="header-card">
        <h1>📊 Mycroft NuPay — Dashboard AML</h1>
        <p>Visão consolidada dos casos analisados nesta sessão.</p>
    </div>
    """, unsafe_allow_html=True)

    casos = st.session_state.casos

    if not casos:
        st.info("Nenhum caso registrado ainda.")
    else:
        total = len(casos)
        altos = sum(1 for c in casos.values() if c["risco_nivel"] == "ALTO")
        medios = sum(1 for c in casos.values() if c["risco_nivel"] == "MÉDIO")
        baixos = sum(1 for c in casos.values() if c["risco_nivel"] == "BAIXO")
        aprovados = sum(1 for c in casos.values() if "Aprovado" in c["parecer"]["decisao"])
        reprovados = sum(1 for c in casos.values() if "Reprovado" in c["parecer"]["decisao"])

        st.markdown(f"""
        <div class="metric-row">
            <div class="metric-box">
                <div class="metric-val" style="color:#6366f1">{total}</div>
                <div class="metric-label">Total de Casos</div>
            </div>
            <div class="metric-box">
                <div class="metric-val risk-high">{altos}</div>
                <div class="metric-label">Risco Alto</div>
            </div>
            <div class="metric-box">
                <div class="metric-val risk-medium">{medios}</div>
                <div class="metric-label">Risco Médio</div>
            </div>
            <div class="metric-box">
                <div class="metric-val risk-low">{baixos}</div>
                <div class="metric-label">Risco Baixo</div>
            </div>
            <div class="metric-box">
                <div class="metric-val" style="color:#4ade80">{aprovados}</div>
                <div class="metric-label">Aprovados</div>
            </div>
            <div class="metric-box">
                <div class="metric-val" style="color:#f87171">{reprovados}</div>
                <div class="metric-label">Reprovados</div>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Table
        st.markdown('<div class="section-title">Todos os Casos</div>', unsafe_allow_html=True)

        import pandas as pd

        rows = []
        for cid, c in casos.items():
            rows.append({
                "ID": cid,
                "CNPJ": c["kyc"]["cnpj"],
                "Razão Social": c["kyc"]["razao_social"],
                "Porte": c["kyc"]["porte"],
                "Risco": c["risco_nivel"],
                "Score": c["risco_score"],
                "Decisão": c["parecer"]["decisao"],
                "Analista": c["parecer"]["analista"],
                "Data": c["criado_em"][:10],
            })

        df = pd.DataFrame(rows)
        st.dataframe(
            df,
            use_container_width=True,
            hide_index=True,
            column_config={
                "Score": st.column_config.ProgressColumn(
                    "Score Risco", min_value=0, max_value=100
                )
            },
        )

        # Export
        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇️  Exportar CSV",
            data=csv,
            file_name=f"aml_casos_{datetime.date.today()}.csv",
            mime="text/csv",
        )
