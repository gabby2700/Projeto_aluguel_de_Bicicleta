import streamlit as st
import joblib
from pathlib import Path

st.set_page_config(page_title="LocaBike", page_icon="🚲", layout="wide")

if not st.session_state.get("modelo", ""):
    st.session_state["modelo"] = joblib.load(Path("models") / "bicicleta.pkl")

# ---------------------------------------------------------------- imagens
# A imagem do cadastro era um link de compartilhamento do ChatGPT, que não
# carrega como imagem. Troque pela sua (URL ou caminho local, ex: "img/cadastro.jpg").
IMG_CADASTRO = "https://preview.redd.it/opinion-on-the-ns-liar-4x-frame-v0-h4h03n08r1ta1.jpg?width=564&format=pjpg&auto=webp&s=4fa0cdaaa5e783448a2cf028a0bbcc2f9a9c3eda"
IMG_ALUGUEL = IMG_CADASTRO

BICICLETAS = [
    ("Bicicleta urbana", "https://tse3.mm.bing.net/th/id/OIP.Oh5XDJypZVvKp3sqezYPSQHaEK?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"),
    ("Bicicleta para passeio", "https://m.media-amazon.com/images/I/81Xoyx1xtZL._AC_SX300_SY300_QL70_ML2_.jpg"),
    ("Bicicleta infantil", "https://tse3.mm.bing.net/th/id/OIP.5QVQOQDr13w4Ly-tB6MMjwHaFj?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"),
    ("Bicicleta de duas pessoas", "https://tse4.mm.bing.net/th/id/OIP.mV3_C60p43cU8nuyh1pgiAHaHa?r=0&rs=1&pid=ImgDetMain&o=7&rm=3"),
    ("Bicicleta com cadeirinha", "https://melhordosbebes.com.br/wp-content/uploads/img/melhores-cadeirinhas-bebeteca.jpg"),
]

# ---------------------------------------------------------------- estilo
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,500;12..96,700;12..96,800&family=DM+Sans:wght@400;500;700&display=swap');

:root {
    --ink: #14213D;
    --sun: #FFC21A;
    --sky: #E8EEF9;
    --paper: #F7F8FB;
    --line: #D9E0EE;
}

html, body, .stApp, [data-testid="stAppViewContainer"] {
    background: var(--paper);
    font-family: 'DM Sans', sans-serif;
    color: var(--ink);
}
.stApp p, .stApp label, .stApp li, .stApp span { color: var(--ink); }
h1, h2, h3, h4 {
    font-family: 'Bricolage Grotesque', sans-serif !important;
    color: var(--ink) !important;
    letter-spacing: -0.02em;
}

/* limpa o visual padrão do Streamlit */
#MainMenu, footer { visibility: hidden; }
header[data-testid="stHeader"] { background: transparent; }
.block-container { max-width: 1180px; padding-top: 1.5rem; padding-bottom: 3rem; }

/* ---------- barra de navegação ---------- */
.nav {
    display: flex; align-items: center; justify-content: space-between;
    padding: 0.4rem 0 1.2rem 0;
}
.nav .logo {
    font-family: 'Bricolage Grotesque', sans-serif;
    font-weight: 800; font-size: 1.6rem; color: var(--ink);
}
.nav .logo b { color: var(--sun); background: var(--ink); padding: 0 .35rem; border-radius: 8px; margin-left: 2px; }
.nav .links { display: flex; gap: 1.6rem; font-weight: 500; }
.nav .links span { color: var(--ink); opacity: .75; }

/* ---------- hero ---------- */
.hero {
    background: var(--ink);
    border-radius: 28px;
    padding: 4rem 3.5rem;
    position: relative;
    overflow: hidden;
    margin-bottom: 2.5rem;
}
.hero::after {
    content: "";
    position: absolute; right: -90px; top: -90px;
    width: 340px; height: 340px; border-radius: 50%;
    border: 38px solid var(--sun); opacity: .95;
}
.hero::before {
    content: "";
    position: absolute; right: 120px; bottom: -120px;
    width: 220px; height: 220px; border-radius: 50%;
    border: 24px solid rgba(255,255,255,.12);
}
.hero h1 {
    color: #fff !important;
    font-size: clamp(2.4rem, 5vw, 4.2rem);
    line-height: 1.02; margin: 0 0 1rem 0; max-width: 620px;
    font-weight: 800;
}
.hero p { color: #C9D3EA !important; font-size: 1.15rem; max-width: 480px; margin: 0 0 1.8rem 0; }
.hero .chips { display: flex; gap: .7rem; flex-wrap: wrap; position: relative; z-index: 1; }
.hero .chip {
    background: var(--sun); color: var(--ink) !important;
    font-weight: 700; padding: .55rem 1.1rem; border-radius: 999px; font-size: .95rem;
}
.hero .chip.ghost { background: transparent; border: 1.5px solid rgba(255,255,255,.35); color: #fff !important; }

/* ---------- abas ---------- */
.stTabs [data-baseweb="tab-list"] {
    gap: .5rem; background: var(--sky); padding: .35rem; border-radius: 999px; width: fit-content;
}
.stTabs [data-baseweb="tab"] {
    height: auto; padding: .55rem 1.4rem; border-radius: 999px;
    font-weight: 700; color: var(--ink); background: transparent;
}
.stTabs [aria-selected="true"] { background: var(--ink) !important; }
.stTabs [aria-selected="true"] p { color: #fff !important; }
.stTabs [data-baseweb="tab-highlight"], .stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------- cartões de formulário ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #fff; border: 1px solid var(--line) !important;
    border-radius: 22px; padding: .8rem;
    box-shadow: 0 10px 30px rgba(20, 33, 61, .06);
}

/* ---------- campos ---------- */
.stTextInput input, .stNumberInput input {
    background: var(--paper) !important; border-radius: 12px !important;
    border: 1.5px solid var(--line) !important; color: var(--ink) !important;
}
.stTextInput input:focus, .stNumberInput input:focus { border-color: var(--ink) !important; }

/* ---------- botões ---------- */
.stButton > button {
    background: var(--sun); color: var(--ink); border: none;
    border-radius: 999px; padding: .7rem 1.8rem;
    font-weight: 700; font-size: 1rem; transition: transform .15s, background .15s;
}
.stButton > button:hover { background: var(--ink); color: #fff; transform: translateY(-1px); }
.stButton > button:focus-visible { outline: 3px solid var(--ink); outline-offset: 2px; }

/* ---------- imagens ---------- */
[data-testid="stImage"] img {
    width: 100% !important;
    border-radius: 18px;
    aspect-ratio: 4 / 3;
    object-fit: cover;
}
[data-testid="stImageCaption"] { font-weight: 700; color: var(--ink); text-align: center; }

/* ---------- resumo do valor ---------- */
.resumo {
    background: var(--sky); border-radius: 16px; padding: 1rem 1.3rem; margin: .8rem 0 1.2rem 0;
}
.resumo .linha { display: flex; justify-content: space-between; padding: .2rem 0; }
.resumo .total {
    border-top: 1.5px dashed var(--line); margin-top: .5rem; padding-top: .7rem;
    font-family: 'Bricolage Grotesque', sans-serif; font-size: 1.6rem; font-weight: 800;
}

/* ---------- barra lateral ---------- */
[data-testid="stSidebar"] { background: var(--ink); }
[data-testid="stSidebar"] * { color: #fff !important; }
[data-testid="stSidebar"] h1 { color: var(--sun) !important; }

/* ---------- rodapé ---------- */
.rodape {
    margin-top: 3rem; padding-top: 1.5rem; border-top: 1px solid var(--line);
    display: flex; justify-content: space-between; flex-wrap: wrap; gap: .5rem;
    font-size: .9rem; opacity: .8;
}

@media (max-width: 700px) {
    .hero { padding: 2.5rem 1.5rem; }
    .nav .links { display: none; }
}
</style>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- navegação + hero
st.markdown(
    """
<div class="nav">
  <div class="logo">Loca<b>Bike</b></div>
  <div class="links"><span>Cadastro</span><span>Aluguel</span><span>Bicicletas</span></div>
</div>

<div class="hero">
  <h1>Pedale com liberdade.</h1>
  <p>Escolha a bicicleta, aluguel por minuto e pagamento só pelo tempo que você usar.</p>
  <div class="chips">
    <span class="chip">Aluguel por minuto</span>
    <span class="chip ghost">Bikes para todas as idades</span>
  </div>
</div>
""",
    unsafe_allow_html=True,
)

# ---------------------------------------------------------------- abas
pag1, pag2 = st.tabs(["Cadastro de cliente", "Aluguel"])

with pag1:
    esq, dir_ = st.columns([1.2, 1], gap="large")

    with esq:
        with st.container(border=True):
            st.header("Cadastro de clientes")
            nome = st.text_input("Nome do cliente")
            telefone = st.text_input("Telefone")
            email = st.text_input("E-mail")

            if st.button("Cadastrar cliente"):
                if nome and telefone:
                    st.success("Cliente cadastrado com sucesso!")
                else:
                    st.warning("Preencha o nome e o telefone.")

    with dir_:
        st.image(IMG_CADASTRO)

with pag2:
    esq, dir_ = st.columns([1.2, 1], gap="large")

    preco = 0.10

    with esq:
        with st.container(border=True):
            st.header("Concluir aluguel")
            minutos = st.number_input(
                "Minutos de aluguel", min_value=0, max_value=600, value=0
            )
            valor = minutos * preco

            st.markdown(
                f"""
<div class="resumo">
  <div class="linha"><span>Valor por minuto</span><span>R$ {preco:.2f}</span></div>
  <div class="linha"><span>Tempo de aluguel</span><span>{minutos} minutos</span></div>
  <div class="linha total"><span>Valor total</span><span>R$ {valor:.2f}</span></div>
</div>
""",
                unsafe_allow_html=True,
            )

            if st.button("Calcular usando machine learning"):
                if minutos > 0:
                    st.success("Deu certo!")
                    st.info(f"Total a pagar: R$ {valor:.2f}")
                else:
                    st.warning("Informe os minutos de aluguel.")

    with dir_:
        st.image(IMG_ALUGUEL)

# ---------------------------------------------------------------- bicicletas
st.write("")
st.subheader("Nossas bicicletas")

colunas = st.columns(len(BICICLETAS), gap="medium")
for coluna, (legenda, url) in zip(colunas, BICICLETAS):
    with coluna:
        st.image(url, caption=legenda)

# ---------------------------------------------------------------- barra lateral
st.sidebar.title("LocaBike")
st.sidebar.write("Aluguel de bicicletas")
st.sidebar.write("Pedale com liberdade!")

st.sidebar.markdown("### Preços")
st.sidebar.write("R$ 1,50 por minuto")
st.sidebar.write("R$ 6,00 por hora")

# ---------------------------------------------------------------- rodapé
st.markdown(
    """
<div class="rodape">
  <span>© LocaBike · Aluguel de bicicletas</span>
  <span>Pedale com liberdade!</span>
</div>
""",
    unsafe_allow_html=True,
)