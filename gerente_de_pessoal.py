import time
import pandas as pd
import streamlit as st

# --- CONFIGURAÇÃO INICIAL DA PÁGINA ---
st.set_page_config(
    page_title="Batata frita RH - Sistema de Gestão & Finanças",
    page_icon="🏢",
    layout="wide",
)

# --- DADOS FICTÍCIOS INICIAIS ---
INITIAL_EMPLOYEES = [
    {
        "id": 1,
        "name": "Ana Silva",
        "role": "Engenheira de Software Senior",
        "department": "Tecnologia",
        "salary": 12500.0,
        "status": "Ativo",
        "contract": "CLT",
        "email": "ana.silva@empresa.com",
    },
    {
        "id": 2,
        "name": "Carlos Oliveira",
        "role": "Gerente de Produtos",
        "department": "Produto",
        "salary": 14000.0,
        "status": "Ativo",
        "contract": "CLT",
        "email": "carlos.o@empresa.com",
    },
    {
        "id": 3,
        "name": "Mariana Santos",
        "role": "Designer UX/UI",
        "department": "Design",
        "salary": 8500.0,
        "status": "Ativo",
        "contract": "PJ",
        "email": "mariana.s@empresa.com",
    },
    {
        "id": 4,
        "name": "Roberto Lima",
        "role": "Analista de RH Pleno",
        "department": "Recursos Humanos",
        "salary": 6200.0,
        "status": "Ativo",
        "contract": "CLT",
        "email": "roberto.l@empresa.com",
    },
    {
        "id": 5,
        "name": "Fernanda Costa",
        "role": "Especialista em Marketing",
        "department": "Marketing",
        "salary": 7800.0,
        "status": "Ativo",
        "contract": "PJ",
        "email": "fernanda.c@empresa.com",
    },
    {
        "id": 6,
        "name": "Lucas Mendes",
        "role": "Desenvolvedor Frontend",
        "department": "Tecnologia",
        "salary": 7500.0,
        "status": "Ativo",
        "contract": "CLT",
        "email": "lucas.m@empresa.com",
    },
]

INITIAL_CANDIDATES = [
    {
        "id": 101,
        "name": "Gabriel Rodrigues",
        "role": "Desenvolvedor Backend",
        "department": "Tecnologia",
        "stage": "triagem",
        "expectedSalary": 9000.0,
        "email": "gabriel.r@email.com",
    },
    {
        "id": 102,
        "name": "Beatriz Lima",
        "role": "Analista de Dados",
        "department": "Tecnologia",
        "stage": "entrevista",
        "expectedSalary": 8000.0,
        "email": "beatriz.l@email.com",
    },
    {
        "id": 103,
        "name": "Thiago Souza",
        "role": "Coordenador de Vendas",
        "department": "Comercial",
        "stage": "teste",
        "expectedSalary": 9500.0,
        "email": "thiago.s@email.com",
    },
    {
        "id": 104,
        "name": "Camila Rocha",
        "role": "Product Owner",
        "department": "Produto",
        "stage": "contratado",
        "expectedSalary": 11000.0,
        "email": "camila.r@email.com",
    },
    {
        "id": 105,
        "name": "Felipe Alves",
        "role": "Designer de Interação",
        "department": "Design",
        "stage": "inscrito",
        "expectedSalary": 6500.0,
        "email": "felipe.a@email.com",
    },
]

# Estágios do processo seletivo
STAGES = [
    {"id": "inscrito", "title": "Triagem Inicial"},
    {"id": "triagem", "title": "Entrevista RH"},
    {"id": "entrevista", "title": "Entrevista Técnica"},
    {"id": "teste", "title": "Proposta / Ajustes"},
    {"id": "contratado", "title": "Pronto p/ Contratar"},
]

DEPARTMENTS = [
    "Tecnologia",
    "Produto",
    "Design",
    "Recursos Humanos",
    "Marketing",
    "Comercial",
]

# --- ESTADOS NATIVOS (SESSION STATE) ---
if "employees" not in st.session_state:
    st.session_state.employees = INITIAL_EMPLOYEES.copy()

if "candidates" not in st.session_state:
    st.session_state.candidates = INITIAL_CANDIDATES.copy()

# Dados Financeiros Ajustáveis
if "company_revenue" not in st.session_state:
    st.session_state.company_revenue = 250000.0  # Faturamento Mensal

if "other_expenses" not in st.session_state:
    st.session_state.other_expenses = 65000.0  # Outras despesas operacionais

# Estado para edição de funcionário
if "editing_emp_id" not in st.session_state:
    st.session_state.editing_emp_id = None


def format_brl(value: float) -> str:
    """Formata um número float para o padrão monetário brasileiro (R$)."""
    return f"R$ {value:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


# --- CÁLCULOS E DERIVADOS ---
employees_list = st.session_state.employees
candidates_list = st.session_state.candidates

total_payroll = sum(float(emp.get("salary", 0)) for emp in employees_list)
total_expenses = total_payroll + float(st.session_state.other_expenses)
net_profit = float(st.session_state.company_revenue) - total_expenses
profit_margin = (
    round((net_profit / float(st.session_state.company_revenue)) * 100, 1)
    if st.session_state.company_revenue and st.session_state.company_revenue > 0
    else 0.0
)

# Estatísticas por Departamento
dept_stats = {}
for emp in employees_list:
    dept = emp.get("department") or "Outros"
    if dept not in dept_stats:
        dept_stats[dept] = {"count": 0, "totalSalary": 0.0}
    dept_stats[dept]["count"] += 1
    dept_stats[dept]["totalSalary"] += float(emp.get("salary", 0))


# --- HANDLERS: FUNCIONÁRIOS ---
def handle_delete_emp(emp_id: int):
    """Remove um funcionário da lista pelo ID."""
    st.session_state.employees = [
        emp for emp in st.session_state.employees if emp["id"] != emp_id
    ]


# --- HANDLERS: RECRUTAMENTO ---
def handle_move_stage(candidate_id: int, new_stage: str):
    """Atualiza o estágio de um candidato no funil de recrutamento."""
    for cand in st.session_state.candidates:
        if cand["id"] == candidate_id:
            cand["stage"] = new_stage
            break


def handle_delete_candidate(candidate_id: int):
    """Remove ou reprova um candidato do processo seletivo."""
    st.session_state.candidates = [
        c for c in st.session_state.candidates if c["id"] != candidate_id
    ]


def handle_hire_candidate(candidate: dict):
    """Efetiva o candidato: adiciona como funcionário e remove da lista de candidatos."""
    new_emp = {
        "id": int(time.time() * 1000),
        "name": candidate["name"],
        "role": candidate["role"],
        "department": candidate["department"],
        "salary": float(candidate.get("expectedSalary") or 5000.0),
        "status": "Ativo",
        "contract": "CLT",
        "email": candidate["email"],
    }
    st.session_state.employees.append(new_emp)
    st.session_state.candidates = [
        c for c in st.session_state.candidates if c["id"] != candidate["id"]
    ]


# --- NAVEGAÇÃO SUPERIOR / CABEÇALHO ---
st.title("🏢 Batata frita RH")
st.caption("Sistema de Gestão & Finanças")

# Abas de Navegação (equivalente a 'employees', 'financial', 'recruitment')
tab_employees, tab_financial, tab_recruitment = st.tabs([
    "👥 Gestão de Pessoal",
    "📈 Cálculos & Lucro",
    "➕ Processo Seletivo",
])

# ================= ABA 1: GESTÃO DE PESSOAL =================
with tab_employees:
    # Header com Resumo (Métricas principais)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Total de Funcionários", len(employees_list))
    with col2:
        st.metric("Folha Mensal Total", format_brl(total_payroll))
    with col3:
        avg_salary = total_payroll / len(employees_list) if employees_list else 0.0
        st.metric("Média Salarial", format_brl(avg_salary))

    st.divider()

    # Filtros de Funcionários
    filter_col1, filter_col2 = st.columns([2, 1])
    with filter_col1:
        search_term = st.text_input(
            "Buscar por nome ou cargo",
            placeholder="Digite um nome ou cargo...",
            label_visibility="collapsed",
        )
    with filter_col2:
        selected_dept = st.selectbox(
            "Departamento",
            options=["Todos"] + DEPARTMENTS,
            label_visibility="collapsed",
        )

    # Filtragem da lista de funcionários
    filtered_employees = [
        emp
        for emp in employees_list
        if (
            search_term.lower() in emp["name"].lower()
            or search_term.lower() in emp["role"].lower()
        )
        and (selected_dept == "Todos" or emp["department"] == selected_dept)
    ]

    # Formulário de Novo / Edição de Funcionário (Expansível)
    emp_to_edit = next(
        (e for e in employees_list if e["id"] == st.session_state.editing_emp_id),
        None,
    )
    with st.expander(
        "✏️ Editar Funcionário" if emp_to_edit else "➕ Novo Funcionário",
        expanded=emp_to_edit is not None,
    ):
        with st.form("employee_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                emp_name = st.text_input(
                    "Nome Completo *",
                    value=emp_to_edit["name"] if emp_to_edit else "",
                )
                emp_role = st.text_input(
                    "Cargo *",
                    value=emp_to_edit["role"] if emp_to_edit else "",
                )
                emp_salary = st.number_input(
                    "Salário (R$) *",
                    min_value=0.0,
                    step=100.0,
                    value=float(emp_to_edit["salary"]) if emp_to_edit else 0.0,
                )
            with f_col2:
                emp_email = st.text_input(
                    "E-mail *",
                    value=emp_to_edit["email"] if emp_to_edit else "",
                )
                default_dept_idx = (
                    DEPARTMENTS.index(emp_to_edit["department"])
                    if emp_to_edit and emp_to_edit["department"] in DEPARTMENTS
                    else 0
                )
                emp_dept = st.selectbox(
                    "Departamento",
                    options=DEPARTMENTS,
                    index=default_dept_idx,
                )
                default_contract_idx = (
                    0 if not emp_to_edit or emp_to_edit["contract"] == "CLT" else 1
                )
                emp_contract = st.selectbox(
                    "Tipo de Contrato",
                    options=["CLT", "PJ"],
                    index=default_contract_idx,
                )

            submit_emp = st.form_submit_button("Salvar Funcionário")
            if submit_emp:
                if emp_name and emp_role and emp_salary > 0:
                    if emp_to_edit:
                        # Atualiza funcionário existente
                        for emp in st.session_state.employees:
                            if emp["id"] == emp_to_edit["id"]:
                                emp.update({
                                    "name": emp_name,
                                    "role": emp_role,
                                    "email": emp_email,
                                    "department": emp_dept,
                                    "salary": float(emp_salary),
                                    "contract": emp_contract,
                                })
                                break
                        st.session_state.editing_emp_id = None
                    else:
                        # Cria novo funcionário
                        new_emp = {
                            "id": int(time.time() * 1000),
                            "name": emp_name,
                            "role": emp_role,
                            "email": emp_email,
                            "department": emp_dept,
                            "salary": float(emp_salary),
                            "contract": emp_contract,
                            "status": "Ativo",
                        }
                        st.session_state.employees.append(new_emp)
                    st.rerun()
                else:
                    st.warning("Preencha nome, cargo e um salário válido.")

        if emp_to_edit and st.button("Cancelar Edição"):
            st.session_state.editing_emp_id = None
            st.rerun()

    # Tabela de Funcionários
    st.subheader("Quadro de Funcionários")
    if filtered_employees:
        df_emp = pd.DataFrame(filtered_employees)
        df_display = df_emp[[
            "name",
            "role",
            "email",
            "department",
            "contract",
            "salary",
            "status",
        ]].copy()
        df_display["salary"] = df_display["salary"].apply(format_brl)
        df_display.columns = [
            "Funcionário",
            "Cargo",
            "E-mail",
            "Departamento",
            "Contrato",
            "Salário",
            "Status",
        ]
        st.dataframe(df_display, use_container_width=True, hide_index=True)

        # Ações rápidas por funcionário (Editar / Excluir)
        st.caption("Ações rápidas por funcionário:")
        for emp in filtered_employees:
            act_col1, act_col2, act_col3 = st.columns([4, 1, 1])
            with act_col1:
                st.write(
                    f"**{emp['name']}** — {emp['role']} ({emp['department']} | {format_brl(emp['salary'])})"
                )
            with act_col2:
                if st.button("Editar", key=f"edit_emp_{emp['id']}"):
                    st.session_state.editing_emp_id = emp["id"]
                    st.rerun()
            with act_col3:
                if st.button("Excluir", key=f"del_emp_{emp['id']}"):
                    handle_delete_emp(emp["id"])
                    st.rerun()
    else:
        st.info("Nenhum funcionário encontrado.")

# ================= ABA 2: CÁLCULOS FINANCEIROS =================
with tab_financial:
    st.subheader("Simulador de Balanço Mensal")

    # Controles de Configuração Financeira
    fin_in_1, fin_in_2 = st.columns(2)
    with fin_in_1:
        st.session_state.company_revenue = st.number_input(
            "Faturamento Bruto Mensal (R$)",
            min_value=0.0,
            step=5000.0,
            value=float(st.session_state.company_revenue),
            help="Entrada total estimada da empresa.",
        )
    with fin_in_2:
        st.session_state.other_expenses = st.number_input(
            "Outras Despesas Operacionais (R$)",
            min_value=0.0,
            step=1000.0,
            value=float(st.session_state.other_expenses),
            help="Impostos, infraestrutura, software, etc.",
        )

    # Recalcula após possível alteração nos inputs
    total_expenses = total_payroll + float(st.session_state.other_expenses)
    net_profit = float(st.session_state.company_revenue) - total_expenses
    profit_margin = (
        round((net_profit / float(st.session_state.company_revenue)) * 100, 1)
        if st.session_state.company_revenue and st.session_state.company_revenue > 0
        else 0.0
    )

    st.divider()

    # Dashboard de Lucro & Métricas
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.metric("Faturamento", format_brl(float(st.session_state.company_revenue)))
    with m2:
        st.metric(
            "Total Despesas",
            format_brl(total_expenses),
            delta="Folha + Custos Operacionais",
            delta_color="off",
        )
    with m3:
        st.metric(
            "Lucro Líquido",
            format_brl(net_profit),
            delta=f"{net_profit >= 0 and 'Positivo' or 'Negativo'}",
        )
    with m4:
        st.metric("Margem de Lucro", f"{profit_margin}%")

    st.divider()

    # Gráficos e Divisão Proporcional
    chart_col1, chart_col2 = st.columns(2)

    # Distribuição Salarial por Departamento
    with chart_col1:
        st.markdown("### Distribuição da Folha de Pagamento")
        if dept_stats:
            for dept, data in dept_stats.items():
                percentage = (
                    round((data["totalSalary"] / total_payroll) * 100, 1)
                    if total_payroll > 0
                    else 0.0
                )
                st.write(
                    f"**{dept}** ({data['count']} func.) — {format_brl(data['totalSalary'])} ({percentage}%)"
                )
                st.progress(min(max(percentage / 100.0, 0.0), 1.0))
        else:
            st.info("Sem dados de folha por departamento.")

    # Proporção Salarial em Relação à Receita
    with chart_col2:
        st.markdown("### Divisão Proporcional do Faturamento")
        rev = float(st.session_state.company_revenue)

        payroll_pct = round((total_payroll / rev) * 100, 1) if rev > 0 else 0.0
        other_pct = (
            round((float(st.session_state.other_expenses) / rev) * 100, 1)
            if rev > 0
            else 0.0
        )
        profit_pct = round((net_profit / rev) * 100, 1) if rev > 0 else 0.0

        st.write(f"**Folha Salarial** — {payroll_pct}%")
        st.progress(min(max(payroll_pct / 100.0, 0.0), 1.0))

        st.write(f"**Outras Despesas Operacionais** — {other_pct}%")
        st.progress(min(max(other_pct / 100.0, 0.0), 1.0))

        st.write(f"**Margem Líquida Retida** — {profit_pct}%")
        st.progress(min(max(profit_pct / 100.0, 0.0), 1.0))

# ================= ABA 3: PROCESSO SELETIVO =================
with tab_recruitment:
    # Header de Ação
    st.subheader("Funil de Recrutamento")
    st.caption(
        "Gerencie candidatos e altere o status das etapas do processo seletivo."
    )

    # Formulário de Novo Candidato
    with st.expander("➕ Novo Candidato"):
        with st.form("candidate_form", clear_on_submit=True):
            c_col1, c_col2 = st.columns(2)
            with c_col1:
                cand_name = st.text_input("Nome Completo *")
                cand_role = st.text_input("Cargo Pretendido *")
                cand_salary = st.number_input(
                    "Pretensão Salarial (R$)", min_value=0.0, step=500.0, value=0.0
                )
            with c_col2:
                cand_email = st.text_input("E-mail *")
                cand_dept = st.selectbox("Departamento", options=DEPARTMENTS)
                stage_options = {s["id"]: s["title"] for s in STAGES if s["id"] != "contratado"}
                cand_stage = st.selectbox(
                    "Etapa Inicial",
                    options=list(stage_options.keys()),
                    format_func=lambda x: stage_options[x],
                )

            submit_cand = st.form_submit_button("Cadastrar Candidato")
            if submit_cand:
                if cand_name and cand_role and cand_email:
                    new_candidate = {
                        "id": int(time.time() * 1000),
                        "name": cand_name,
                        "role": cand_role,
                        "email": cand_email,
                        "department": cand_dept,
                        "expectedSalary": float(cand_salary),
                        "stage": cand_stage,
                    }
                    st.session_state.candidates.append(new_candidate)
                    st.rerun()
                else:
                    st.warning("Preencha nome, cargo e e-mail do candidato.")

    st.divider()

    # Board Kanban de Etapas
    kanban_cols = st.columns(len(STAGES))
    for idx, stage in enumerate(STAGES):
        stage_candidates = [
            c for c in candidates_list if c["stage"] == stage["id"]
        ]
        with kanban_cols[idx]:
            st.markdown(f"#### {stage['title']} ({len(stage_candidates)})")

            if stage_candidates:
                for cand in stage_candidates:
                    with st.container(border=True):
                        st.markdown(f"**{cand['name']}**")
                        st.caption(f"{cand['role']} • {cand['department']}")
                        st.write(
                            f"Pretensão: **{format_brl(float(cand.get('expectedSalary', 0)))}**"
                        )

                        # Movimentação de Estágio / Contratação / Remoção
                        if stage["id"] == "contratado":
                            if st.button(
                                "✅ Efetivar Contratação",
                                key=f"hire_{cand['id']}",
                                use_container_width=True,
                            ):
                                handle_hire_candidate(cand)
                                st.rerun()
                        else:
                            nav_col1, nav_col2 = st.columns(2)
                            with nav_col1:
                                if idx > 0:
                                    if st.button("← Voltar", key=f"prev_{cand['id']}"):
                                        handle_move_stage(
                                            cand["id"], STAGES[idx - 1]["id"]
                                        )
                                        st.rerun()
                            with nav_col2:
                                if idx < len(STAGES) - 1:
                                    if st.button("Avançar →", key=f"next_{cand['id']}"):
                                        handle_move_stage(
                                            cand["id"], STAGES[idx + 1]["id"]
                                        )
                                        st.rerun()

                        if st.button(
                            "🗑️ Remover",
                            key=f"del_cand_{cand['id']}",
                            use_container_width=True,
                        ):
                            handle_delete_candidate(cand["id"])
                            st.rerun()
            else:
                st.caption("Sem candidatos")