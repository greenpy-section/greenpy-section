# GreenPy Section — Interface via streamlit

# Durante processo de submissão à revista RENOTE (outubro de 2026):
# Autores: XXX (mantidos em sigilo) XXX 

# Data da última revisão: 20/10/2026

# importa bibliotecas
import io
import os
import math as m
import tempfile
import contextlib
import numpy as np
import pandas as pd
import streamlit as st

# importa módulos próprios
import greenpy_functions as gp 

# ======================================= #
# === Funções e Definições Auxiliares === #
# ======================================= #

APP_TITLE = "GreenPy Section"
TEMP_DIR = tempfile.gettempdir()
TEMP_INPUT = os.path.join(TEMP_DIR, "dados_green_streamlit.txt")

# Arquivos temporários de figuras
TEMP_IMG_PNG_CANDIDATES = ["temp_fig.png", "temp_figura.png", "figura_temp.png"]
TEMP_IMG_SVG_CANDIDATES = ["temp_fig.svg", "temp_figura.svg", "figura_temp.svg"]

def unidades_st(unidade: str):
    """Retorna dicionário com unidade escolhida nas potências {1,2,3,4} ou vazio."""
    if unidade == "Não informar":
        return {1: "", 2: "", 3: "", 4: ""}
    u = unidade.strip()
    return {1: u, 2: u + "²", 3: u + "³", 4: u + "⁴"}

# Tamanho da diagonal das figuras (pol)
SIZE_DIAGONAL_PRESETS_IN = {
    "PP": 7.0,
    "P":  9.0,
    "M":  11.0,
    "G":  13.0,
    "GG": 15.0,
}

# Resoluções das figuras (pixels)
DISPLAY_DIAGONAL_PRESETS_PX = {
    "PP": 420,
    "P":  640,
    "M":  840,
    "G":  980,
    "GG": 1200,
}

# Tamanhos de textos - fatores relativos ao "size")
TEXT_SIZE_PRESETS = {
    "PP": {"title": 0.8, "axis": 0.7, "labels": 0.7},
    "P":  {"title": 1.0, "axis": 0.9, "labels": 0.9},
    "M":  {"title": 1.3, "axis": 1.1, "labels": 1.1},
    "G":  {"title": 1.5, "axis": 1.3, "labels": 1.3},
    "GG": {"title": 1.8, "axis": 1.6, "labels": 1.6},
}

def _find_first(paths):
    return next((p for p in paths if os.path.exists(p)), None)

def render_by_diagonal(caption=None, diag_px=None):
    """
    Renderiza PNG escalado por diagonal desejada (diag_px em pixels).
    A largura exibida = diag_px * (w / sqrt(w^2+h^2)).
    """
    png = _find_first(TEMP_IMG_PNG_CANDIDATES)
    if not png:
        return None

    width_arg = None
    if diag_px is not None:
        try:
            from PIL import Image
            with Image.open(png) as im:
                w, h = im.size
            d = (w**2 + h**2) ** 0.5
            width_arg = int(round(diag_px * (w / d))) if d > 0 else int(diag_px)
        except Exception:
            width_arg = int(diag_px)

    st.image(png, caption=caption, width=width_arg, use_container_width=False)
    return png


def offer_png_download(default_name):
    png = _find_first(TEMP_IMG_PNG_CANDIDATES)
    if png:
        with open(png, "rb") as f:
            st.download_button("Baixar figura (PNG)", f.read(), file_name=default_name, mime="image/png")

def offer_svg_download(default_name):
    svg = _find_first(TEMP_IMG_SVG_CANDIDATES)
    if svg:
        with open(svg, "rb") as f:
            st.download_button("Baixar figura (SVG)", f.read(), file_name=default_name, mime="image/svg+xml")

def capture_stdout(fn, *args, **kwargs) -> str:
    buf = io.StringIO()
    with contextlib.redirect_stdout(buf):
        fn(*args, **kwargs)
    return buf.getvalue()

def df_vazio(n: int, cols=None) -> pd.DataFrame:
    COLS = cols or ['tipo', 'xi', 'yi', 'θ_i', 'θ_f', 'raio', 'xp', 'yp']
    df = pd.DataFrame([{c: "" for c in COLS} for _ in range(int(n))])
    df.index = [f"C{i+1}" for i in range(len(df))]
    return df

def as_df(obj, cols=None, fallback_rows: int = 0) -> pd.DataFrame:
    COLS = cols or ['tipo', 'xi', 'yi', 'θ_i', 'θ_f', 'raio', 'xp', 'yp']
    if isinstance(obj, pd.DataFrame):
        df = obj.reindex(columns=COLS).fillna("")
    else:
        try:
            df = pd.DataFrame(obj).reindex(columns=COLS).fillna("")
        except Exception:
            df = pd.DataFrame([{c: "" for c in COLS} for _ in range(fallback_rows)])
    df.index = [f"C{i+1}" for i in range(len(df))]
    return df

def linha_para_texto(row: dict) -> str:
    """Converte uma linha (dict/pd.Series) no formato do dados_green.txt."""
    def canon_tipo(v):
        try:
            if v is None:
                return ""
            if isinstance(v, (float, np.floating)):
                if np.isnan(v):
                    return ""
                return str(int(round(v)))
            if isinstance(v, (int, np.integer)):
                return str(int(v))
            s = str(v).strip()
            if "–" in s:
                s = s.split("–")[0].strip()
            if s.endswith(".0"):
                s = s[:-2]
            return s
        except Exception:
            return ""
    def cell(v):
        try:
            if v is None:
                return ""
            if isinstance(v, (float, np.floating)) and np.isnan(v):
                return ""
            if pd.isna(v):
                return ""
            return str(v).strip()
        except Exception:
            return ""

    t = canon_tipo(row.get('tipo', ""))
    if t not in {"1", "2", "3", "4"}:
        return ""
    xi = cell(row.get('xi'))
    yi = cell(row.get('yi'))
    ti = cell(row.get('θ_i'))
    tf = cell(row.get('θ_f'))
    raio = cell(row.get('raio'))
    xp = cell(row.get('xp'))
    yp = cell(row.get('yp'))

    if t == "1":
        return f"1 {xi} {yi}"
    if t == "2":
        return f"2 {xi} {yi} {ti} {tf} {raio}"
    if t == "3":
        return f"3 {xi} {yi} {xp} {yp}"
    return f"4 {xi} {yi} {xp} {yp}"

def show_dados_entrada(ntot, n_sup, c, sep_dec, sep_milhar):
    texto = capture_stdout(gp.imprime_dados, ntot, n_sup, c, sep_dec=sep_dec, sep_milhar=sep_milhar)
    st.text(texto)

def imprime_resultados_st(props, unidades, sep_dec, sep_milhar) -> str:
    """
    Usa gp.imprime_resultados para gerar o MESMO texto,
    remove apenas as 4 primeiras linhas de 'enfeite' e exibe como texto simples.
    """
    area, sx, sy, x_c, y_c, ixc, iyc, pxyc, ix, iy, imax, imin, e1, e2, pxy = props
    txt = capture_stdout(
        gp.imprime_resultados,
        area, sx, sy, x_c, y_c, ixc, iyc, pxyc, ix, iy, imax, imin, e1, e2, pxy,
        unidades, sep_dec=sep_dec, sep_milhar=sep_milhar
    )
    linhas = txt.splitlines()
    if len(linhas) > 4:
        linhas = linhas[4:]  # tira o cabeçalho grande
    texto_final = "\n".join(linhas).strip()
    # (removido "Resultados" menor; só mostramos o texto)
    st.text(texto_final)
    return texto_final

# ========================== #
# === Programa principal === #
# ========================== #

st.set_page_config(page_title=APP_TITLE, layout="centered")
st.title(APP_TITLE)
st.caption("Cálculo de propriedades geométricas de seções planas com o Teorema de Green.")

st.caption("Autores: XXX (Mantidos em sigilo durante processo de submissão à revista RENOTE) XXX  \n"
           "XXX (Grupo de pesquisa mantido em sigilo) XXX \n"
           "XXX (Instituição mantida em sigilo) XXX")

# ========================================== #
# === Sidebar (configurações na lateral) === #
# ========================================== #

with st.sidebar:
    
    # Título principal da sidebar
    st.header("Configurações")
    
    # Selecionar unidade de comprimento
    unidade = st.selectbox(
        "Unidade de comprimento",
        ["Não informar", "mm", "cm", "dm", "m", "dam", "hm", "km", "pol", "in", "ft"],
        index=0,
    )
    unidades = unidades_st(unidade)
    
    st.markdown("---")
    
    # Configurar separador decimal e de milhar
    st.subheader("Formatação numérica")
    sep_dec = st.selectbox("Separador decimal", options=[",", "."], index=0)
    usar_milhar = st.checkbox("Usar separador de milhar", value=True)
    sep_milhar = "." if (usar_milhar and sep_dec == ",") else ("," if usar_milhar else "")

    st.markdown("---")
    
    # Configurar opções gerais de desenho (para todos os gráficos)
    st.subheader("Opções de desenho (geral)")
    size_choice = st.select_slider("Tamanho das figuras", options=list(SIZE_DIAGONAL_PRESETS_IN.keys()), value="M")
    size_in = SIZE_DIAGONAL_PRESETS_IN[size_choice]
    disp_px = DISPLAY_DIAGONAL_PRESETS_PX[size_choice]

    text_choice = st.select_slider("Tamanho dos textos", options=list(TEXT_SIZE_PRESETS.keys()), value="M")
    fator_title = TEXT_SIZE_PRESETS[text_choice]["title"]
    fator_axis = TEXT_SIZE_PRESETS[text_choice]["axis"]
    fator_fontsize = TEXT_SIZE_PRESETS[text_choice]["labels"]
    
    st.markdown("---")
    
    # Configurar opções de desenho da figura inicial (conferência dos dados)
    st.subheader("Opções da figura inicial (caminhos)")
    line_color = st.color_picker("Cor das linhas de contorno", value="#7079EF")
    outer_fill_color = st.color_picker("Cor de preenchimento", value="#7079EF")
    fill_alpha = st.slider("Opacidade do preenchimento", 0.0, 1.0, 0.4, 0.05)
    espessura_caminhos = st.slider("Espessura das linhas", 0.5, 3.0, 1.0, 0.1)
    marker_size = st.slider("Tamanho dos pontos", 0.00, 8.00, 4.00, 0.50)  
    grid_opt = st.checkbox("Mostrar grade", value=True)
    
    # Rótulos & offset
    show_labels_conf = st.checkbox("Mostrar rótulos dos caminhos (Ci)", value=True)
    offset_rotulos = st.slider("Offset dos rótulos", -2.0, 2.0, 1.0, 0.1)

    st.markdown("---")
    
    st.subheader("Opções da figura final (resultados)")
    clean_line_color = st.color_picker("Cor das linhas (figura final)", value="#222222")
    clean_fill_color = st.color_picker("Cor de preenchimento (figura final)", value="#7079EF")
    clean_fill_alpha = st.slider("Opacidade do preenchimento (figura final)", 0.0, 1.0, 0.18, 0.02)
    espessura_clean = st.slider("Espessura das linhas (figura final)", 0.5, 3.0, 1.0, 0.1)

# ======================== #
# === Entrada de dados === #
# ======================== #

# === Abas com opções de entrada de dados === #

tabs = st.tabs(["Tabela dinâmica", "Inserir texto", "Enviar arquivo"])

# === Aba 1 — Tabela dinâmica === #

with tabs[0]:
    st.markdown("### Entrada de dados por tabela dinâmica")
    st.caption("Clique em **Aplicar estrutura** antes de editar as tabelas.")

    COLS = ['tipo', 'xi', 'yi', 'θ_i', 'θ_f', 'raio', 'xp', 'yp']

    if 'tbl_cfg' not in st.session_state:
        st.session_state.tbl_cfg = {'ncc': 3, 'nf': 1, 'ncf': [2]}
    if 'tbl_data' not in st.session_state:
        st.session_state.tbl_data = {
            'contorno': df_vazio(st.session_state.tbl_cfg['ncc'], COLS),
            'furos': [df_vazio(n, COLS) for n in st.session_state.tbl_cfg['ncf']],
        }
    cfg = st.session_state.tbl_cfg
    data_tbl = st.session_state.tbl_data

    # Form de estrutura
    with st.form("form_estrutura", clear_on_submit=False):
        st.subheader("Estrutura da seção")
        colA, colB = st.columns(2, gap="medium")
        with colA:
            ncc_in = st.number_input("Número de caminhos do contorno", 1, 500, cfg['ncc'], 1, key="ncc_in")
        with colB:
            nf_in = st.number_input("Número de furos", 0, 50, cfg['nf'], 1, key="nf_in")

        st.markdown("**Número de caminhos por furo:**")
        ncf_inputs = []
        if nf_in > 0:
            for i in range(0, nf_in, 4):
                c1, c2, c3, c4 = st.columns(4, gap="medium")
                with c1:
                    default = cfg['ncf'][i] if i < len(cfg['ncf']) else 0
                    ncf_inputs.append(st.number_input(f"Furo {i+1}", 0, 500, default, 1, key=f"ncf_in_{i}"))
                if i + 1 < nf_in:
                    with c2:
                        default = cfg['ncf'][i+1] if i+1 < len(cfg['ncf']) else 0
                        ncf_inputs.append(st.number_input(f"Furo {i+2}", 0, 500, default, 1, key=f"ncf_in_{i+1}"))
                if i + 2 < nf_in:
                    with c3:
                        default = cfg['ncf'][i+2] if i+2 < len(cfg['ncf']) else 0
                        ncf_inputs.append(st.number_input(f"Furo {i+3}", 0, 500, default, 1, key=f"ncf_in_{i+2}"))
                if i + 3 < nf_in:
                    with c4:
                        default = cfg['ncf'][i+3] if i+3 < len(cfg['ncf']) else 0
                        ncf_inputs.append(st.number_input(f"Furo {i+4}", 0, 500, default, 1, key=f"ncf_in_{i+3}"))
        else:
            st.caption("Sem furos (você pode alterar no campo acima).")

        st.markdown("")
        apply = st.form_submit_button("Aplicar estrutura", type="primary")

    # Legenda de tipos depois do formulário — em cinza
    st.caption("Tipos: 1 – segmento de reta · 2 – arco · 3 – parábola y=f(x) · 4 – parábola x=f(y)")
    
    # Se apertar o botão aplicar:
    if apply:
        cfg['ncc'] = int(ncc_in)
        cfg['nf'] = int(nf_in)
        cfg['ncf'] = [int(x) for x in ncf_inputs]

        old_cont = as_df(data_tbl.get('contorno'), COLS, fallback_rows=cfg['ncc'])
        new_cont = df_vazio(cfg['ncc'], COLS)
        if not old_cont.empty:
            ncopy = min(len(old_cont), len(new_cont))
            new_cont.iloc[:ncopy, :] = old_cont.iloc[:ncopy, :].to_numpy()
        data_tbl['contorno'] = new_cont

        old_furos = [as_df(x, COLS) for x in (data_tbl.get('furos') or [])]
        new_furos = []
        for i, nlin in enumerate(cfg['ncf']):
            df_new = df_vazio(nlin, COLS)
            if i < len(old_furos) and not old_furos[i].empty:
                ncopy = min(len(old_furos[i]), len(df_new))
                df_new.iloc[:ncopy, :] = old_furos[i].iloc[:ncopy, :].to_numpy()
            new_furos.append(df_new)
        data_tbl['furos'] = new_furos

        st.session_state['editor_contorno_state'] = data_tbl['contorno'].copy()
        for k in list(st.session_state.keys()):
            if k.startswith("editor_furo_"):
                del st.session_state[k]
        for i, df in enumerate(data_tbl['furos']):
            st.session_state[f"editor_furo_{i}_state"] = df.copy()

        (st.rerun() if hasattr(st, "rerun") else st.experimental_rerun())

    # Editores
    tipo_opts = ["1", "2", "3", "4"]  # opções de tipo de caminho

    st.markdown("#### Caminhos do contorno")
    if 'editor_contorno_state' not in st.session_state:
        st.session_state['editor_contorno_state'] = data_tbl['contorno'].copy()

    cont_atual = st.data_editor(
        st.session_state['editor_contorno_state'],
        key="editor_contorno",
        use_container_width=True,
        num_rows="fixed",
        column_config={
            'tipo': st.column_config.SelectboxColumn("Tipo", options=tipo_opts,
                                                     help="1=reta, 2=arco, 3=y=f(x), 4=x=f(y)"),
            'xi':   st.column_config.NumberColumn("xi"),
            'yi':   st.column_config.NumberColumn("yi"),
            'θ_i':  st.column_config.NumberColumn("θi (graus)"),
            'θ_f':  st.column_config.NumberColumn("θf (graus)"),
            'raio': st.column_config.NumberColumn("raio"),
            'xp':   st.column_config.NumberColumn("xp"),
            'yp':   st.column_config.NumberColumn("yp"),
        },
    )
    cont_atual = as_df(cont_atual)

    furos_atuais = []
    if cfg['nf'] > 0:
        st.markdown("#### Caminhos dos furos")
        for i in range(cfg['nf']):
            st.markdown(f"**Furo {i+1}**")
            editor_key = f"editor_furo_{i}_state"
            widget_key = f"editor_furo_{i}"
            if editor_key not in st.session_state:
                base = data_tbl['furos'][i] if i < len(data_tbl['furos']) else df_vazio(0, COLS)
                st.session_state[editor_key] = base.copy()

            df_edit = st.data_editor(
                st.session_state[editor_key],
                key=widget_key,
                use_container_width=True,
                num_rows="fixed",
                column_config={
                    'tipo': st.column_config.SelectboxColumn("Tipo", options=tipo_opts,
                                                             help="1=reta, 2=arco, 3=y=f(x), 4=x=f(y)"),
                    'xi':   st.column_config.NumberColumn("xi"),
                    'yi':   st.column_config.NumberColumn("yi"),
                    'θ_i':  st.column_config.NumberColumn("θi (graus)"),
                    'θ_f':  st.column_config.NumberColumn("θf (graus)"),
                    'raio': st.column_config.NumberColumn("raio"),
                    'xp':   st.column_config.NumberColumn("xp"),
                    'yp':   st.column_config.NumberColumn("yp"),
                },
            )
            furos_atuais.append(as_df(df_edit))

    st.divider()
    
    gerar = st.button("Gerar arquivo de dados", type="primary")
    
    if gerar:
        linhas = [
            "# Arquivo de dados gerado via tabela no Streamlit",
            "# Formato: tipo xi yi [θi θf raio | xp yp]",
            "",
        ]
        for _, row in cont_atual.iterrows():
            t = linha_para_texto(row)
            if t:
                linhas.append(t)
        linhas.append("")
        for df in furos_atuais:
            for _, row in df.iterrows():
                t = linha_para_texto(row)
                if t:
                    linhas.append(t)
            linhas.append("")
        conteudo = "\n".join(linhas) + "\n"

        st.markdown("#### Arquivo gerado")
        st.code(conteudo, language="text")

        try:
            with open(TEMP_INPUT, "w", encoding="utf-8") as f:
                f.write(conteudo)
        except Exception as e:
            st.error(f"❌ Erro ao salvar '{TEMP_INPUT}': {e}")
        else:
            st.success(f"✅ Arquivo salvo: {TEMP_INPUT}")
            st.download_button("Baixar arquivo (.txt)", data=conteudo, file_name="dados_green.txt", mime="text/plain")

            try:
                ntot_v, ncc_v, nf_v, ncf_v, n_sup_v, c_v = gp.leitura_de_dados(TEMP_INPUT)
                # Desenho de figura: Prévia da seção
                gp.desenha_caminhos(
                    ntot_v, c_v,
                    size=size_in*0.6, # reduz o tamanho da prévia para 60%
                    fator_fontsize=fator_fontsize, fator_title=0, fator_axis=fator_axis, fator_offset=1.0,
                    jupyter=False, texto_caminho=False, color=line_color,
                    espessura=espessura_caminhos, markersize=marker_size, grid=grid_opt, st=True,
                    section_clean=False, fill_section=True,
                    outer_fill_color=outer_fill_color, fill_alpha_main=fill_alpha,
                    n_sup=n_sup_v,
                )
                render_by_diagonal("Prévia da seção", diag_px=disp_px*0.6)

            except Exception as e:
                st.error(f"❌ Erro na validação ou pré-visualização: {e}")

                
# === Aba 2 — Inserir texto === #

with tabs[1]:
    st.markdown("### Entrada de dados por texto")
    st.caption("Cole ou digite no padrão `dados_green.txt` e salve.")

    instrucao_padrao = (
        "Divida o contorno da seção em caminhos simples.  \n"
        "↶ Contorno: sentido anti-horário.  \n"
        "↷ Furos: sentido horário.\n\n"
        "Tipos de caminhos:  \n"
        "`1 – segmento de reta`  \n"
        "`2 – arco`  \n"
        "`3 – parábola y=f(x)`  \n"
        "`4 – parábola x=f(y)`\n\n"
        "Insira uma linha de dados por caminho, no formato:  \n"
        "`tipo xi yi [θi θf raio | xp yp]`\n\n"
        "Linhas em branco separam grupos de caminhos (contorno ou furos).  \n"
        "Linhas iniciadas por `#` são comentários."
    )

    # >>> Só grava quando submeter <<<
    with st.form("form_inserir_texto", clear_on_submit=False):
        st.caption("Orientações:")
        st.markdown(instrucao_padrao)  # agora aparece como texto normal
        dados_txt = st.text_area("Dados dos caminhos:", height=220, key="dados_txt_area")
        salvar_txt = st.form_submit_button("Salvar texto (Ctrl+Enter)", type="primary")

    if salvar_txt:
        if dados_txt.strip():
            try:
                with open(TEMP_INPUT, "w", encoding="utf-8") as f:
                    f.write(dados_txt)
                st.success(f"✅ Arquivo atualizado: {TEMP_INPUT}")
            except Exception as e:
                st.error(f"❌ Erro ao salvar '{TEMP_INPUT}': {e}")
        else:
            st.warning("O campo 'Dados dos caminhos' está vazio. Nada foi salvo.")


            
# === Aba 3 — Enviar arquivo === #

with tabs[2]:
    st.markdown("### Entrada de dados por arquivo .txt")
    up = st.file_uploader("Selecione um arquivo no padrão do GreenPy (até 1 MB)", type=["txt"], key="upload_txt")
    if up is not None:
        if up.size and up.size > 1_000_000:
            st.error("Arquivo muito grande. Limite: 1 MB.")
        else:
            content = up.read().decode("utf-8", errors="ignore")
            with open(TEMP_INPUT, "w", encoding="utf-8") as f:
                f.write(content)
            st.success(f"Arquivo carregado: {TEMP_INPUT}")

# ==================================================== #
# === Conferência de dados e Cálculo de Resultados === #
# ==================================================== #       
            
st.markdown("---")
c1, c2 = st.columns(2)
with c1:
    check = st.button("Conferir dados")
with c2:
    calc = st.button("Calcular resultados")

parsed = False
if os.path.exists(TEMP_INPUT):
    try:
        ntot, ncc, nf, ncf, n_sup, c = gp.leitura_de_dados(TEMP_INPUT)
        parsed = True
    except Exception:
        parsed = False

if check:
    if not parsed:
        st.warning("Nenhum arquivo válido encontrado. Gere ou carregue um `.txt` nas abas acima.")
    else:
        st.markdown("")
        st.subheader("Conferência de Dados de Entrada")
        gp.desenha_caminhos(
            ntot, c,
            size=size_in, fator_fontsize=fator_fontsize, fator_title=fator_title, fator_axis=fator_axis,
            fator_offset=offset_rotulos,
            texto_caminho=show_labels_conf, color=line_color, espessura=espessura_caminhos, markersize=marker_size,
            grid=grid_opt, jupyter=False, st=True, eixos_principais=False, eixos_ref=False,
            section_clean=False, fill_section=True, outer_fill_color=outer_fill_color,
            fill_alpha_main=fill_alpha, n_sup=n_sup,
        )
        render_by_diagonal(diag_px=disp_px)
        offer_png_download("conferencia_dados.png")
        offer_svg_download("conferencia_dados.svg")
        show_dados_entrada(ntot, n_sup, c, sep_dec=sep_dec, sep_milhar=sep_milhar)

if calc:
    if not parsed:
        st.warning("Nenhum arquivo válido encontrado. Gere ou carregue um `.txt` nas abas acima.")
    else:
        st.markdown("")
        st.subheader("Resultados")
        props = gp.propriedades_geometricas(c)

        # Resultado como o imprime_resultados 
        txt_out = imprime_resultados_st(props, unidades, sep_dec, sep_milhar)
        st.download_button("Baixar resultados (.txt)", data=txt_out, file_name="resultados_green.txt", mime="text/plain")

        # Seção limpa
        gp.desenha_caminhos(
            ntot, c, size=size_in, texto_caminho=False, markersize=0, grid=False,
            jupyter=False, st=True, section_clean=True, color=clean_line_color, espessura=espessura_clean,
            fill_section=True, outer_fill_color=clean_fill_color, fill_alpha_main=clean_fill_alpha,
        )
        st.markdown("**Seção limpa**")
        render_by_diagonal(diag_px=disp_px)
        offer_png_download("secao.png")
        offer_svg_download("secao.svg")

        # Eixos principais
        gp.desenha_caminhos(
            ntot, c, size=size_in, texto_caminho=False, markersize=0, grid=False,
            jupyter=False, st=True, eixos_principais=True, fator_eixos_principais=2,
            color=line_color, espessura=espessura_caminhos, eixos_ref=True,
            fill_section=True, outer_fill_color="#F0F8FF", fill_alpha_main=0.22,
        )
        st.markdown("**Eixos principais**")
        render_by_diagonal(diag_px=disp_px)
        offer_png_download("eixos_principais.png")
        offer_svg_download("eixos_principais.svg")
