import streamlit as st
import json
import os
import hashlib
import random
from datetime import date, datetime

APP_TITLE = "FlickPy"
USERS_FILE = "flickpy_users.json"
INVITE_CODES = ["FLICK2026", "PYTHONCLASS", "INVITEFlickPy"]
ADMIN_USER = "admin"
ADMIN_PASS_HASH = hashlib.sha256("admin123".encode("utf-8")).hexdigest()

LESSONS = [
    {
        "id": "intro_vars",
        "title": "Variables",
        "icon": "🟢",
        "xp": 15,
        "difficulty": "Fácil",
        "theory": "Las variables guardan datos. Ejemplo: nombre = 'Ana'",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué tipo de dato guarda texto?",
                "options": ["str", "int", "bool"],
                "answer": "str",
                "explanation": "str representa texto en Python.",
            },
            {
                "type": "fill",
                "prompt": "Completa la variable",
                "starter": "_____ = 'Flick'",
                "answer": "nombre",
                "explanation": "Un ejemplo correcto es nombre = 'Flick'.",
            },
        ],
    },
    {
        "id": "cond_if",
        "title": "Condicionales",
        "icon": "🟡",
        "xp": 20,
        "difficulty": "Fácil",
        "theory": "if, elif y else permiten tomar decisiones según una condición.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué palabra se usa para una ruta alternativa?",
                "options": ["then", "else", "switch"],
                "answer": "else",
                "explanation": "else ejecuta otra ruta cuando la condición no se cumple.",
            },
            {
                "type": "fill",
                "prompt": "Completa la palabra clave",
                "starter": "if x > 5:\n    print('ok')\n_____: \n    print('no')",
                "answer": "else",
                "explanation": "La opción correcta es else.",
            },
        ],
    },
    {
        "id": "loops_for",
        "title": "Bucles",
        "icon": "🔵",
        "xp": 25,
        "difficulty": "Media",
        "theory": "for repite acciones sobre secuencias. range(3) produce 0, 1, 2.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué genera range(3)?",
                "options": ["1,2,3", "0,1,2", "0,1,2,3"],
                "answer": "0,1,2",
                "explanation": "range empieza en 0 y termina antes del número indicado.",
            },
            {
                "type": "fill",
                "prompt": "Completa la función",
                "starter": "for i in _____(5):\n    print(i)",
                "answer": "range",
                "explanation": "range(5) repite 5 veces: 0,1,2,3,4.",
            },
        ],
    },
    {
        "id": "funcs",
        "title": "Funciones",
        "icon": "🟣",
        "xp": 30,
        "difficulty": "Media",
        "theory": "Una función se define con def y puede devolver valores con return.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué palabra define una función?",
                "options": ["func", "def", "return"],
                "answer": "def",
                "explanation": "def crea una función en Python.",
            },
            {
                "type": "fill",
                "prompt": "Completa la palabra clave",
                "starter": "def sumar(a, b):\n    _____ a + b",
                "answer": "return",
                "explanation": "return devuelve el resultado.",
            },
        ],
    },
    {
        "id": "lists",
        "title": "Listas",
        "icon": "🟠",
        "xp": 35,
        "difficulty": "Media",
        "theory": "Las listas almacenan varios elementos en orden. Ejemplo: frutas = ['manzana', 'pera']",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Con qué símbolo se crea una lista?",
                "options": ["()", "[]", "{}"],
                "answer": "[]",
                "explanation": "Las listas usan corchetes.",
            },
            {
                "type": "fill",
                "prompt": "Completa el método",
                "starter": "numeros = [1, 2]\nnumeros._____(3)",
                "answer": "append",
                "explanation": "append agrega un elemento al final de la lista.",
            },
        ],
    },
]

ACHIEVEMENTS = [
    ("start", "Primer login", lambda u: True),
    ("xp50", "50 XP", lambda u: u.get("xp", 0) >= 50),
    ("xp100", "100 XP", lambda u: u.get("xp", 0) >= 100),
    ("streak3", "Racha x3", lambda u: u.get("streak", 0) >= 3),
    ("all_lessons", "Ruta completa", lambda u: len(u.get("completed_lessons", [])) >= len(LESSONS)),
]


def hash_pw(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def default_progress(display_name="Estudiante"):
    return {
        "name": display_name,
        "xp": 0,
        "level": 1,
        "streak": 0,
        "gems": 25,
        "hearts": 5,
        "completed_lessons": [],
        "achievements": [],
        "last_active": "",
        "history": [],
    }


def load_users():
    if not os.path.exists(USERS_FILE):
        return {}
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}


def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=2)


def get_image_path(name):
    for ext in ["png", "jpg", "jpeg", "webp"]:
        path = f"{name}.{ext}"
        if os.path.exists(path):
            return path
    return None


def render_logo(width=120):
    logo = get_image_path("logo")
    if logo:
        st.image(logo, width=width)
    else:
        st.markdown(
            f"""
            <div style='width:{width}px;height:{width}px;border-radius:28px;background:radial-gradient(circle at top,#163b8c,#091126 70%);display:flex;align-items:center;justify-content:center;font-size:52px;border:1px solid rgba(100,255,210,0.28);box-shadow:0 0 30px rgba(0,255,170,0.10)'>🐍</div>
            """,
            unsafe_allow_html=True,
        )


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0,255,170,0.08), transparent 25%),
                radial-gradient(circle at top right, rgba(0,153,255,0.08), transparent 25%),
                linear-gradient(180deg, #050814 0%, #091126 50%, #050814 100%);
        }
        .block-container {
            padding-top: 1.4rem;
            padding-bottom: 2rem;
        }
        .card {
            padding: 22px;
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(7,13,28,0.92), rgba(8,18,36,0.86));
            border: 1px solid rgba(93,255,190,0.16);
            box-shadow: 0 20px 60px rgba(0,0,0,0.35);
        }
        .hero-title {
            color: #f5fbff;
            font-size: 2.6rem;
            font-weight: 900;
            margin-bottom: 0.3rem;
        }
        .hero-sub {
            color:#bfd0ea;
            font-size:1.05rem;
            margin-bottom: 0.8rem;
        }
        .mini-badge {
            display:inline-block;
            padding:8px 12px;
            border-radius:999px;
            margin-right:8px;
            margin-top:8px;
            background:rgba(17, 30, 56, 0.95);
            border:1px solid rgba(70, 255, 190, 0.18);
            color:#d8e6ff;
            font-size:0.85rem;
        }
        .lesson-tile {
            padding: 16px;
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(11,22,43,0.95), rgba(8,15,31,0.92));
            border: 1px solid rgba(93,255,190,0.12);
            text-align: center;
            min-height: 140px;
            margin-bottom: 14px;
        }
        .lesson-icon {
            font-size: 2rem;
            margin-bottom: 8px;
        }
        .lesson-name {
            color: white;
            font-weight: 700;
            font-size: 1rem;
        }
        .lesson-meta {
            color: #aec4e6;
            font-size: 0.85rem;
            margin-top: 6px;
        }
        .path-node {
            width: 72px;
            height: 72px;
            border-radius: 50%;
            display:flex;
            align-items:center;
            justify-content:center;
            font-size:1.7rem;
            margin: 0 auto 8px auto;
            background: linear-gradient(180deg, #1ce783, #0f9b58);
            box-shadow: 0 10px 25px rgba(0,0,0,0.35);
        }
        .path-node.locked {
            background: linear-gradient(180deg, #34445d, #202c3c);
        }
        .centered-small {
            text-align:center;
            color:#c7d7ef;
            font-size:0.9rem;
        }
        .question-card {
            padding: 24px;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(10,20,38,0.98), rgba(8,15,31,0.94));
            border: 1px solid rgba(93,255,190,0.16);
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
            animation: slideUpFade 0.45s ease;
            margin-bottom: 16px;
        }
        .transition-chip {
            display:inline-block;
            padding:10px 14px;
            border-radius:999px;
            background: rgba(28,231,131,0.12);
            border:1px solid rgba(28,231,131,0.24);
            color:#dfffee;
            font-weight:700;
            animation: pulseGlow 0.8s ease-in-out 2;
            margin-bottom: 12px;
        }
        .question-title {
            color:white;
            font-size:1.35rem;
            font-weight:800;
            margin-bottom: 8px;
        }
        @keyframes slideUpFade {
            from {
                opacity: 0;
                transform: translateY(18px) scale(0.98);
            }
            to {
                opacity: 1;
                transform: translateY(0) scale(1);
            }
        }
        @keyframes pulseGlow {
            0% { transform: scale(1); box-shadow: 0 0 0 rgba(28,231,131,0); }
            50% { transform: scale(1.04); box-shadow: 0 0 24px rgba(28,231,131,0.22); }
            100% { transform: scale(1); box-shadow: 0 0 0 rgba(28,231,131,0); }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def unlock_achievements(progress):
    current = set(progress.get("achievements", []))
    for aid, _, cond in ACHIEVEMENTS:
        if aid not in current and cond(progress):
            progress.setdefault("achievements", []).append(aid)


def update_meta(progress):
    today = str(date.today())
    last = progress.get("last_active", "")
    if last:
        try:
            last_date = datetime.strptime(last, "%Y-%m-%d").date()
            diff = (date.today() - last_date).days
            if diff == 1:
                progress["streak"] += 1
            elif diff > 1:
                progress["streak"] = 1
        except Exception:
            progress["streak"] = max(1, progress.get("streak", 0))
    else:
        progress["streak"] = 1
    progress["last_active"] = today
    progress["level"] = max(1, progress.get("xp", 0) // 50 + 1)
    unlock_achievements(progress)
    return progress


def register_user(name, username, password, invite_code):
    users = load_users()
    username = username.strip().lower()
    if invite_code not in INVITE_CODES:
        return False, "Código de invitación inválido."
    if not name or not username or not password:
        return False, "Completa todos los campos."
    if username in users or username == ADMIN_USER:
        return False, "Ese usuario ya existe."
    if len(password) < 6:
        return False, "La contraseña debe tener al menos 6 caracteres."
    users[username] = {
        "name": name.strip(),
        "password": hash_pw(password),
        "created_at": str(date.today()),
        "progress": default_progress(name.strip()),
    }
    save_users(users)
    return True, "Cuenta creada correctamente."


def login_user(username, password):
    username = username.strip().lower()
    if username == ADMIN_USER and hash_pw(password) == ADMIN_PASS_HASH:
        st.session_state["user"] = ADMIN_USER
        st.session_state["admin"] = True
        st.session_state["progress"] = default_progress("Administrador")
        return True, "Acceso de administrador concedido."
    users = load_users()
    user = users.get(username)
    if not user:
        return False, "Ese usuario no existe."
    if user.get("password") != hash_pw(password):
        return False, "Contraseña incorrecta."
    st.session_state["user"] = username
    st.session_state["admin"] = False
    st.session_state["progress"] = user.get("progress", default_progress(user.get("name", username)))
    return True, "Bienvenido a FlickPy."


def persist_progress():
    if st.session_state.get("admin"):
        return
    username = st.session_state.get("user")
    if not username:
        return
    users = load_users()
    if username in users:
        users[username]["progress"] = st.session_state.get("progress", default_progress())
        save_users(users)


def lesson_completed(progress, lesson_id):
    return lesson_id in progress.get("completed_lessons", [])


def next_lesson_id(progress):
    for lesson in LESSONS:
        if lesson["id"] not in progress.get("completed_lessons", []):
            return lesson["id"]
    return None


def is_lesson_locked(progress, lesson_id):
    nxt = next_lesson_id(progress)
    if nxt is None:
        return False
    return lesson_id != nxt and lesson_id not in progress.get("completed_lessons", [])


def auth_screen():
    if st.session_state.get("user"):
        return
    inject_css()
    c1, c2 = st.columns([1, 2])
    with c1:
        render_logo(180)
    with c2:
        st.markdown("<div class='card'>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title'>FlickPy</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-sub'>Aprende Python desde 0 con progreso real, XP, logros y una interfaz tipo Duolingo.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<span class='mini-badge'>Invitación requerida</span>"
            "<span class='mini-badge'>XP · Racha · Logros</span>"
            "<span class='mini-badge'>Modo Admin</span>",
            unsafe_allow_html=True,
        )
        t1, t2 = st.tabs(["Iniciar sesión", "Crear cuenta"])
        with t1:
            u = st.text_input("Usuario", key="login_u")
            p = st.text_input("Contraseña", type="password", key="login_p")
            if st.button("Entrar", use_container_width=True):
                ok, msg = login_user(u, p)
                if ok:
                    st.success(msg)
                    st.rerun()
                else:
                    st.error(msg)
        with t2:
            n = st.text_input("Nombre visible", key="reg_n")
            u2 = st.text_input("Usuario nuevo", key="reg_u")
            p2 = st.text_input("Contraseña", type="password", key="reg_p")
            code = st.text_input("Código de invitación", key="reg_code")
            if st.button("Crear cuenta", use_container_width=True):
                ok, msg = register_user(n, u2, p2, code)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()


def render_header(progress):
    left, right = st.columns([5, 1])
    with left:
        st.title(f"{APP_TITLE} · aprende Python jugando")
    with right:
        render_logo(84)
        if st.session_state.get("admin"):
            st.caption("Modo administrador")
        st.caption(f"Sesión: {st.session_state.get('user', 'guest')}")
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    a, b, c, d, e = st.columns(5)
    a.metric("Nivel", progress.get("level", 1))
    b.metric("XP", progress.get("xp", 0))
    c.metric("Racha", progress.get("streak", 0))
    d.metric("Gemas", progress.get("gems", 0))
    e.metric("Corazones", progress.get("hearts", 5))


def render_learning_path(progress):
    st.markdown("### Ruta visual")
    cols = st.columns(len(LESSONS))
    nxt = next_lesson_id(progress)
    for i, lesson in enumerate(LESSONS):
        done = lesson_completed(progress, lesson["id"])
        is_next = lesson["id"] == nxt
        locked = not done and not is_next and nxt is not None
        node_class = "path-node locked" if locked else "path-node"
        label = "✅" if done else ("▶️" if is_next else "🔒")
        with cols[i]:
            st.markdown(
                f"""
                <div class='{node_class}'>{lesson['icon']}</div>
                <div class='centered-small'><strong>{lesson['title']}</strong></div>
                <div class='centered-small'>{label} · {lesson['xp']} XP</div>
                """,
                unsafe_allow_html=True,
            )


def render_home(progress):
    st.subheader(f"Hola, {progress.get('name', 'Estudiante')} 👋")
    total = len(LESSONS)
    done = len(progress.get("completed_lessons", []))
    nxt = next_lesson_id(progress)
    st.progress(done / total if total else 0, text=f"Ruta completada: {done}/{total}")
    st.write("Completa misiones, sube de nivel y desbloquea nuevos temas de Python.")
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown("<div class='card'><h4 style='color:white;'>Siguiente misión</h4><p style='color:#c7d7ef;'>Sigue tu ruta principal y gana XP, gemas y logros.</p></div>", unsafe_allow_html=True)
    with c2:
        st.markdown("<div class='card'><h4 style='color:white;'>Vidas</h4><p style='color:#c7d7ef;'>Cada error puede costarte una vida. Entrena con cuidado.</p></div>", unsafe_allow_html=True)
    with c3:
        st.markdown("<div class='card'><h4 style='color:white;'>Recompensas</h4><p style='color:#c7d7ef;'>Usa tus gemas para recuperar vidas en la tienda.</p></div>", unsafe_allow_html=True)
    if nxt:
        lesson = next(l for l in LESSONS if l["id"] == nxt)
        st.markdown("### Continúa tu ruta")
        st.info(f"Tu siguiente lección es: {lesson['icon']} {lesson['title']} · {lesson['xp']} XP")
        if st.button("▶️ Continuar aprendizaje", type="primary", use_container_width=True):
            st.session_state["selected_lesson_id"] = nxt
            st.session_state["go_to_lessons"] = True
            st.rerun()
    else:
        st.success("Terminaste toda la ruta actual. Ya puedes repetir lecciones o agregar nuevas unidades.")
    render_learning_path(progress)
    st.markdown("### Unidades")
    cols = st.columns(min(3, len(LESSONS)))
    for idx, lesson in enumerate(LESSONS):
        with cols[idx % len(cols)]:
            done = lesson_completed(progress, lesson["id"])
            locked = is_lesson_locked(progress, lesson["id"])
            status = "Completada ✅" if done else ("Bloqueada 🔒" if locked else "Disponible 🟡")
            st.markdown(
                f"""
                <div class='lesson-tile'>
                    <div class='lesson-icon'>{lesson['icon']}</div>
                    <div class='lesson-name'>{lesson['title']}</div>
                    <div class='lesson-meta'>{lesson['difficulty']} · {lesson['xp']} XP</div>
                    <div class='lesson-meta'>{status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )


def render_lessons(progress):
    st.subheader("Ruta de aprendizaje")
    lesson_map = {f"{l['icon']} {l['title']} · {l['difficulty']}": l for l in LESSONS}
    labels = list(lesson_map.keys())
    default_index = 0
    selected_lesson_id = st.session_state.get("selected_lesson_id")
    if selected_lesson_id:
        for i, lesson in enumerate(LESSONS):
            if lesson["id"] == selected_lesson_id:
                default_index = i
                break
    selected = st.selectbox("Elige una lección", labels, index=default_index)
    lesson = lesson_map[selected]
    if is_lesson_locked(progress, lesson["id"]):
        nxt = next_lesson_id(progress)
        next_title = next((l["title"] for l in LESSONS if l["id"] == nxt), "la siguiente")
        st.warning(f"Esta lección está bloqueada. Primero debes completar: {next_title}.")
        return
    lesson_key = f"lesson_state_{lesson['id']}"
    transition_key = f"transition_msg_{lesson['id']}"
    if lesson_key not in st.session_state:
        st.session_state[lesson_key] = {
            "index": 0,
            "correct": 0,
            "finished": False,
            "awarded": False,
        }
    state = st.session_state[lesson_key]
    with st.container(border=True):
        st.markdown(f"## {lesson['icon']} {lesson['title']}")
        st.caption(f"Dificultad: {lesson['difficulty']} · Recompensa: {lesson['xp']} XP")
        st.write(lesson["theory"])
    total_q = len(lesson["questions"])
    if state["finished"]:
        st.success(f"Lección terminada. Aciertos: {state['correct']}/{total_q}")
        if state["correct"] == total_q:
            if lesson["id"] not in progress["completed_lessons"] and not state["awarded"]:
                progress["completed_lessons"].append(lesson["id"])
                progress["xp"] += lesson["xp"]
                progress["gems"] += 5
                progress["history"].append({"title": lesson["title"], "date": str(date.today()), "xp": lesson["xp"]})
                update_meta(progress)
                st.session_state["progress"] = progress
                persist_progress()
                state["awarded"] = True
                st.session_state[lesson_key] = state
                st.session_state["selected_lesson_id"] = next_lesson_id(progress)
                st.balloons()
                st.success("Perfecto. Completaste la lección y ganaste recompensas.")
            elif lesson["id"] in progress["completed_lessons"]:
                st.info("Ya habías completado esta lección.")
        else:
            st.warning("No lograste un perfecto. Puedes reintentar la lección para completarla.")
        c1, c2 = st.columns(2)
        with c1:
            if st.button("Reintentar lección", use_container_width=True):
                st.session_state[lesson_key] = {
                    "index": 0,
                    "correct": 0,
                    "finished": False,
                    "awarded": False,
                }
                st.session_state[transition_key] = ""
                st.rerun()
        with c2:
            if lesson["id"] in progress.get("completed_lessons", []):
                st.success("✅ Lección completada")
            else:
                st.info("💡 Debes acertar todas para completarla")
        return
    q_index = state["index"]
    q = lesson["questions"][q_index]
    st.progress((q_index + 1) / total_q, text=f"Pregunta {q_index + 1} de {total_q}")
    if st.session_state.get(transition_key):
        st.markdown(f"<div class='transition-chip'>{st.session_state[transition_key]}</div>", unsafe_allow_html=True)
        st.session_state[transition_key] = ""
    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-title'>{q['prompt']}</div>", unsafe_allow_html=True)
    answer_key = f"answer_{lesson['id']}_{q_index}"
    if q["type"] == "mc":
        ans = st.radio("Selecciona una opción", q["options"], index=None, key=answer_key)
    else:
        st.code(q["starter"], language="python")
        ans = st.text_input("Completa", key=answer_key)
    if st.button("Comprobar", type="primary", use_container_width=True, key=f"check_{lesson['id']}_{q_index}"):
        if ans is None or str(ans).strip() == "":
            st.warning("Debes responder antes de continuar.")
        else:
            ok = str(ans).strip() == str(q["answer"]).strip()
            if ok:
                state["correct"] += 1
                st.session_state[transition_key] = "✅ Correcto. Avanzando..."
            else:
                progress["hearts"] = max(0, progress.get("hearts", 5) - 1)
                st.session_state["progress"] = progress
                persist_progress()
                st.session_state[transition_key] = "⚡ Siguiente reto..."
            state["index"] += 1
            if state["index"] >= total_q:
                state["finished"] = True
            st.session_state[lesson_key] = state
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)


def render_practice(progress):
    st.subheader("Práctica rápida")
    if progress.get("hearts", 5) <= 0:
        st.error("No tienes vidas disponibles. Usa gemas en la tienda para recuperar una.")
        return
    lesson = random.choice(LESSONS)
    q = random.choice(lesson["questions"])
    st.caption(f"Tema: {lesson['title']}")
    st.write(q["prompt"])
    if q["type"] == "mc":
        ans = st.radio("Tu respuesta", q["options"], index=None)
    else:
        st.code(q["starter"], language="python")
        ans = st.text_input("Completa")
    if st.button("Comprobar práctica", use_container_width=True):
        if ans is None or str(ans).strip() == "":
            st.warning("Debes responder antes de continuar.")
            return
        ok = str(ans).strip() == str(q["answer"]).strip()
        if ok:
            progress["xp"] += 5
            progress["gems"] += 1
            progress["history"].append({"title": f"Práctica · {lesson['title']}", "date": str(date.today()), "xp": 5})
            update_meta(progress)
            st.session_state["progress"] = progress
            persist_progress()
            st.success("Correcto. +5 XP y +1 gema")
        else:
            progress["hearts"] = max(0, progress.get("hearts", 5) - 1)
            st.session_state["progress"] = progress
            persist_progress()
            st.error(f"Incorrecto. Respuesta esperada: {q['answer']}")
            if progress["hearts"] <= 0:
                st.warning("Te quedaste sin vidas 💔")
            else:
                st.warning(f"Perdiste 1 vida. Te quedan {progress['hearts']}.")


def render_shop(progress):
    st.subheader("Tienda")
    st.write("Canjea gemas por vidas para seguir aprendiendo.")
    c1, c2 = st.columns(2)
    with c1:
        with st.container(border=True):
            st.markdown("### ❤️ 1 vida")
            st.caption("Costo: 10 gemas")
            if st.button("Comprar 1 vida", use_container_width=True):
                if progress.get("gems", 0) >= 10:
                    progress["gems"] -= 10
                    progress["hearts"] += 1
                    st.session_state["progress"] = progress
                    persist_progress()
                    st.success("Compraste 1 vida.")
                else:
                    st.error("No tienes suficientes gemas.")
    with c2:
        with st.container(border=True):
            st.markdown("### ❤️❤️ pack x3")
            st.caption("Costo: 25 gemas")
            if st.button("Comprar pack x3", use_container_width=True):
                if progress.get("gems", 0) >= 25:
                    progress["gems"] -= 25
                    progress["hearts"] += 3
                    st.session_state["progress"] = progress
                    persist_progress()
                    st.success("Compraste 3 vidas.")
                else:
                    st.error("No tienes suficientes gemas.")


def render_achievements(progress):
    st.subheader("Logros")
    unlocked = set(progress.get("achievements", []))
    cols = st.columns(2)
    for idx, (aid, name, _) in enumerate(ACHIEVEMENTS):
        with cols[idx % 2]:
            with st.container(border=True):
                st.markdown(f"### {'🏆' if aid in unlocked else '🔒'} {name}")
                st.caption("Desbloqueado" if aid in unlocked else "Bloqueado")


def render_stats(progress):
    st.subheader("Tus estadísticas")
    c1, c2, c3 = st.columns(3)
    c1.metric("Lecciones", len(progress.get("completed_lessons", [])))
    c2.metric("Historial", len(progress.get("history", [])))
    c3.metric("XP total", progress.get("xp", 0))
    st.markdown("### Actividad reciente")
    history = progress.get("history", [])
    if not history:
        st.info("Aún no hay actividad.")
    else:
        for item in reversed(history[-10:]):
            with st.container(border=True):
                st.write(f"**{item['title']}**")
                st.caption(f"{item['date']} · +{item['xp']} XP")


def render_editor():
    st.subheader("Editor rápido")
    st.code(
        """LESSONS = [{
    'id': 'nuevo_tema',
    'title': 'Nuevo tema',
    'icon': '🧠',
    'xp': 20,
    'difficulty': 'Fácil',
    'theory': 'Explicación breve...',
    'questions': []
}]

INVITE_CODES = ['FLICK2026', 'NUEVOCODIGO']
""",
        language="python",
    )


def render_admin():
    st.subheader("Panel de administración")
    users = load_users()
    total_users = len(users)
    total_xp = sum(v.get("progress", {}).get("xp", 0) for v in users.values())
    total_done = sum(len(v.get("progress", {}).get("completed_lessons", [])) for v in users.values())
    c1, c2, c3 = st.columns(3)
    c1.metric("Usuarios", total_users)
    c2.metric("XP total", total_xp)
    c3.metric("Lecciones completadas", total_done)
    if not users:
        st.info("Todavía no hay usuarios registrados.")
        return
    for username, data in users.items():
        progress = data.get("progress", default_progress(data.get("name", username)))
        with st.container(border=True):
            st.markdown(f"**{data.get('name', username)}** · @{username}")
            a, b, c, d = st.columns(4)
            a.metric("Nivel", progress.get("level", 1))
            b.metric("XP", progress.get("xp", 0))
            c.metric("Racha", progress.get("streak", 0))
            d.metric("Lecciones", len(progress.get("completed_lessons", [])))


def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🐍", layout="wide")
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "admin" not in st.session_state:
        st.session_state["admin"] = False
    if "progress" not in st.session_state:
        st.session_state["progress"] = default_progress()
    auth_screen()
    inject_css()
    progress = st.session_state.get("progress", default_progress())
    if not st.session_state.get("admin"):
        progress = update_meta(progress)
        st.session_state["progress"] = progress
        persist_progress()
    render_header(progress)
    if st.session_state.get("admin"):
        render_admin()
        st.markdown("### Compartir con tu clase")
        st.code("python -m streamlit run flickpy_duolingo_style_app.py", language="bash")
        return
    tabs = st.tabs(["Inicio", "Lecciones", "Práctica", "Tienda", "Logros", "Estadísticas", "Editor"])
    if st.session_state.get("go_to_lessons"):
        st.session_state["go_to_lessons"] = False
        st.info("Abre la pestaña 'Lecciones' para continuar tu ruta.")
    with tabs[0]:
        render_home(progress)
    with tabs[1]:
        render_lessons(progress)
    with tabs[2]:
        render_practice(progress)
    with tabs[3]:
        render_shop(progress)
    with tabs[4]:
        render_achievements(progress)
    with tabs[5]:
        render_stats(progress)
    with tabs[6]:
        render_editor()


if __name__ == "__main__":
    main()
