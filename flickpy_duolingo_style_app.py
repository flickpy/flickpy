# ==============================
# FLICKPY - VERSION PRO ESTABLE
# ==============================

import streamlit as st
import json
import os
import hashlib
import random
from datetime import date

APP_TITLE = "FlickPy"
USERS_FILE = "flickpy_users.json"
INVITE_CODES = ["FLICK2026", "PYTHONCLASS", "INVITEFlickPy"]

# ==============================
# BASE DE LECCIONES + 40 EXTRA
# ==============================

BASE_LESSONS = [
    {
        "id": "vars_01",
        "title": "Variables 1",
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
                "explanation": "str representa texto.",
            },
            {
                "type": "fill",
                "prompt": "Completa la variable",
                "starter": "_____ = 'Flick'",
                "answer": "nombre",
                "explanation": "Un ejemplo válido es nombre = 'Flick'.",
            },
        ],
    },
    {
        "id": "if_01",
        "title": "Condicionales 1",
        "icon": "🟡",
        "xp": 18,
        "difficulty": "Fácil",
        "theory": "if y else permiten tomar decisiones.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué palabra marca la ruta alternativa?",
                "options": ["then", "else", "switch"],
                "answer": "else",
                "explanation": "else ejecuta otra ruta.",
            },
            {
                "type": "fill",
                "prompt": "Completa la estructura",
                "starter": "if x > 5:\n    print('ok')\n_____: \n    print('no')",
                "answer": "else",
                "explanation": "La opción correcta es else.",
            },
        ],
    },
    {
        "id": "for_01",
        "title": "Bucles 1",
        "icon": "🔵",
        "xp": 20,
        "difficulty": "Fácil",
        "theory": "for repite acciones sobre secuencias.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué genera range(3)?",
                "options": ["1,2,3", "0,1,2", "0,1,2,3"],
                "answer": "0,1,2",
                "explanation": "range empieza en 0 y termina antes del 3.",
            },
            {
                "type": "fill",
                "prompt": "Completa la función",
                "starter": "for i in _____(5):\n    print(i)",
                "answer": "range",
                "explanation": "range(5) produce 0,1,2,3,4.",
            },
        ],
    },
    {
        "id": "func_01",
        "title": "Funciones 1",
        "icon": "🟣",
        "xp": 22,
        "difficulty": "Media",
        "theory": "Las funciones se crean con def y pueden devolver valores con return.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué palabra define una función?",
                "options": ["func", "def", "return"],
                "answer": "def",
                "explanation": "def crea una función.",
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
        "id": "list_01",
        "title": "Listas 1",
        "icon": "🟠",
        "xp": 24,
        "difficulty": "Media",
        "theory": "Las listas almacenan varios elementos en orden.",
        "questions": [
            {
                "type": "mc",
                "prompt": "¿Qué símbolo usa una lista?",
                "options": ["()", "[]", "{}"],
                "answer": "[]",
                "explanation": "Las listas usan corchetes.",
            },
            {
                "type": "fill",
                "prompt": "Completa el método",
                "starter": "numeros = [1, 2]\nnumeros._____(3)",
                "answer": "append",
                "explanation": "append agrega un elemento.",
            },
        ],
    },
]

EXTRA_LESSON_SPECS = [
    ("Strings", "🔤", "Media", 26, "Los strings son texto y tienen métodos útiles.", [
        ("mc", "¿Qué método convierte a mayúsculas?", ["upper", "split", "append"], "upper", "upper convierte el texto a mayúsculas.", None),
        ("fill", "Completa el método", None, "lower", "lower pasa el texto a minúsculas.", "texto = 'HOLA'\ntexto._____()"),
    ]),
    ("Print e input", "⌨️", "Fácil", 18, "print muestra texto y input recibe datos del usuario.", [
        ("mc", "¿Qué función muestra texto en pantalla?", ["input", "print", "len"], "print", "print muestra texto.", None),
        ("fill", "Completa la función", None, "input", "input permite escribir datos.", "nombre = _____('Tu nombre: ')"),
    ]),
    ("While", "🔁", "Media", 28, "while repite mientras una condición sea verdadera.", [
        ("mc", "¿Cuál palabra crea un bucle condicional?", ["for", "loop", "while"], "while", "while repite según una condición.", None),
        ("fill", "Completa la palabra", None, "while", "Se usa while.", "_____ x < 5:\n    x += 1"),
    ]),
    ("Booleanos", "⚪", "Fácil", 16, "Los booleanos representan verdadero o falso.", [
        ("mc", "¿Cuál es un valor booleano?", ["True", "'True'", "1"], "True", "True es booleano real.", None),
        ("fill", "Completa el valor", None, "False", "False también es booleano.", "activo = _____"),
    ]),
    ("Comparaciones", "⚖️", "Fácil", 18, "Comparar permite evaluar igualdad o diferencia.", [
        ("mc", "¿Qué operador significa igual a?", ["=", "==", "!="], "==", "== compara igualdad.", None),
        ("fill", "Completa el operador", None, ">", "> significa mayor que.", "print(5 _____ 3)"),
    ]),
    ("Operadores lógicos", "🧠", "Media", 24, "and, or y not combinan condiciones.", [
        ("mc", "¿Qué operador exige que ambas condiciones sean verdaderas?", ["or", "and", "not"], "and", "and requiere ambas verdaderas.", None),
        ("fill", "Completa la palabra", None, "not", "not invierte una condición.", "print(_____ True)"),
    ]),
    ("Tuplas", "📦", "Media", 25, "Las tuplas son similares a listas pero inmutables.", [
        ("mc", "¿Qué símbolo usa una tupla?", ["[]", "()", "{}"], "()", "Las tuplas usan paréntesis.", None),
        ("fill", "Completa la estructura", None, "(", "Una tupla empieza con paréntesis.", "datos = _____1, 2, 3)"),
    ]),
    ("Sets", "🧩", "Media", 27, "Los sets no guardan duplicados.", [
        ("mc", "¿Qué colección evita duplicados?", ["list", "set", "tuple"], "set", "set no guarda repetidos.", None),
        ("fill", "Completa la palabra", None, "set", "set crea un conjunto.", "numeros = _____([1,1,2])"),
    ]),
    ("Diccionarios", "📘", "Media", 30, "Los diccionarios guardan clave y valor.", [
        ("mc", "¿Qué símbolo usa un diccionario?", ["[]", "{}", "()"], "{}", "Los diccionarios usan llaves.", None),
        ("fill", "Completa el método", None, "get", "get obtiene un valor por clave.", "persona = {'nombre': 'Ana'}\npersona._____('nombre')"),
    ]),
    ("Métodos de lista", "📋", "Media", 30, "Las listas tienen métodos como append y pop.", [
        ("mc", "¿Qué método agrega un elemento?", ["push", "append", "add"], "append", "append agrega al final.", None),
        ("fill", "Completa el método", None, "pop", "pop elimina un elemento.", "datos = [1,2,3]\ndatos._____()"),
    ]),
    ("Slicing", "✂️", "Media", 32, "El slicing toma porciones de una secuencia.", [
        ("mc", "¿Qué obtiene texto[0:2]?", ["primer carácter", "dos primeros caracteres", "todo el texto"], "dos primeros caracteres", "0:2 toma desde 0 hasta antes de 2.", None),
        ("fill", "Completa el ejemplo", None, ":", "El slicing usa dos puntos.", "sub = texto[0____2]"),
    ]),
    ("Enumerate", "🔢", "Media", 32, "enumerate permite recorrer índice y valor.", [
        ("mc", "¿Qué función da índice y valor?", ["range", "enumerate", "zip"], "enumerate", "enumerate da índice y valor.", None),
        ("fill", "Completa la función", None, "enumerate", "Se usa enumerate.", "for i, valor in _____(lista):\n    print(i, valor)"),
    ]),
    ("Zip", "🪢", "Media", 34, "zip combina elementos de varias secuencias.", [
        ("mc", "¿Qué función combina listas en pares?", ["zip", "join", "merge"], "zip", "zip combina secuencias.", None),
        ("fill", "Completa la función", None, "zip", "zip une elementos por posición.", "pares = _____(nombres, edades)"),
    ]),
    ("Funciones 2", "🛠️", "Media", 34, "Las funciones pueden recibir parámetros y reutilizar lógica.", [
        ("mc", "¿Cómo se llaman los valores que recibe una función?", ["métodos", "parámetros", "índices"], "parámetros", "Se llaman parámetros.", None),
        ("fill", "Completa la palabra", None, "def", "def define la función.", "_____ saludar(nombre):\n    print(nombre)"),
    ]),
    ("Return", "↩️", "Media", 34, "return devuelve un resultado desde una función.", [
        ("mc", "¿Qué palabra devuelve un valor?", ["print", "return", "yield"], "return", "return devuelve el resultado.", None),
        ("fill", "Completa la palabra", None, "return", "return envía el valor hacia afuera.", "def doble(x):\n    _____ x * 2"),
    ]),
    ("Scope", "🌐", "Difícil", 36, "El scope define dónde existe una variable.", [
        ("mc", "¿Dónde vive una variable creada dentro de una función?", ["scope global", "scope local", "archivo entero"], "scope local", "Dentro de funciones suele ser local.", None),
        ("fill", "Completa la palabra", None, "global", "global permite referirse a una variable global.", "_____ puntos"),
    ]),
    ("Try Except", "🛡️", "Media", 36, "try y except permiten manejar errores.", [
        ("mc", "¿Qué bloque captura un error?", ["except", "error", "raise"], "except", "except captura excepciones.", None),
        ("fill", "Completa la palabra", None, "try", "Se usa try para envolver el riesgo.", "_____:\n    x = 1 / 0"),
    ]),
    ("Archivos", "📂", "Media", 38, "open permite leer y escribir archivos.", [
        ("mc", "¿Qué función abre un archivo?", ["file", "open", "read"], "open", "open abre archivos.", None),
        ("fill", "Completa el modo", None, "r", "r sirve para leer.", "archivo = open('datos.txt', '_____')"),
    ]),
    ("Clases", "🏛️", "Difícil", 42, "Las clases permiten crear objetos y agrupar comportamiento.", [
        ("mc", "¿Qué palabra define una clase?", ["class", "def", "object"], "class", "class define una clase.", None),
        ("fill", "Completa la palabra", None, "class", "Se usa class.", "_____ Persona:\n    pass"),
    ]),
    ("Objetos", "🧱", "Difícil", 42, "Un objeto es una instancia de una clase.", [
        ("mc", "¿Qué es p = Persona()?", ["una clase", "una instancia", "un módulo"], "una instancia", "Es un objeto creado desde la clase.", None),
        ("fill", "Completa el método especial", None, "__init__", "__init__ inicializa atributos.", "def _____(self, nombre):\n    self.nombre = nombre"),
    ]),
]


def build_extra_lessons():
    lessons = []
    for idx in range(40):
        name, icon, difficulty, xp, theory, qspecs = EXTRA_LESSON_SPECS[idx % len(EXTRA_LESSON_SPECS)]
        lesson_num = idx + 1
        questions = []
        for q_index, spec in enumerate(qspecs):
            q_type, prompt, options, answer, explanation, starter = spec
            if q_type == "mc":
                questions.append(
                    {
                        "type": "mc",
                        "prompt": f"{prompt}",
                        "options": options,
                        "answer": answer,
                        "explanation": explanation,
                    }
                )
            else:
                questions.append(
                    {
                        "type": "fill",
                        "prompt": prompt,
                        "starter": starter,
                        "answer": answer,
                        "explanation": explanation,
                    }
                )
        lessons.append(
            {
                "id": f"extra_{lesson_num:02d}",
                "title": f"{name} {lesson_num}",
                "icon": icon,
                "xp": xp + (idx % 4) * 2,
                "difficulty": difficulty,
                "theory": theory,
                "questions": questions,
            }
        )
    return lessons


LESSONS = BASE_LESSONS + build_extra_lessons()

# ==============================
# LOGROS
# ==============================

ACHIEVEMENTS = [
    ("first_login", "Primer login", lambda p: True),
    ("xp_100", "100 XP", lambda p: p.get("xp", 0) >= 100),
    ("xp_300", "300 XP", lambda p: p.get("xp", 0) >= 300),
    ("lessons_10", "10 lecciones", lambda p: len(p.get("completed", [])) >= 10),
    ("lessons_30", "30 lecciones", lambda p: len(p.get("completed", [])) >= 30),
    ("full_route", "Ruta completa", lambda p: len(p.get("completed", [])) >= len(LESSONS)),
]

# ==============================
# UTILIDADES
# ==============================


def hash_pw(text):
    return hashlib.sha256(text.encode("utf-8")).hexdigest()



def default_progress(display_name="Estudiante"):
    return {
        "name": display_name,
        "xp": 0,
        "level": 1,
        "gems": 25,
        "hearts": 5,
        "streak": 0,
        "completed": [],
        "history": [],
        "achievements": [],
        "infinite_streak": 0,
        "best_infinite_streak": 0,
        "last_active": "",
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



def persist_current_user():
    if "user" not in st.session_state:
        return
    users = load_users()
    username = st.session_state["user"]
    if username in users:
        users[username]["progress"] = st.session_state["progress"]
        save_users(users)



def update_meta(progress):
    progress["level"] = max(1, progress.get("xp", 0) // 80 + 1)
    today = str(date.today())
    if progress.get("last_active") != today:
        progress["streak"] = progress.get("streak", 0) + 1
        progress["last_active"] = today
    unlock_achievements(progress)
    return progress



def unlock_achievements(progress):
    unlocked = set(progress.get("achievements", []))
    for aid, _, rule in ACHIEVEMENTS:
        if aid not in unlocked and rule(progress):
            progress.setdefault("achievements", []).append(aid)



def lesson_completed(progress, lesson_id):
    return lesson_id in progress.get("completed", [])



def next_lesson_id(progress):
    for lesson in LESSONS:
        if lesson["id"] not in progress.get("completed", []):
            return lesson["id"]
    return None



def is_lesson_locked(progress, lesson_id):
    nxt = next_lesson_id(progress)
    if nxt is None:
        return False
    return lesson_id != nxt and lesson_id not in progress.get("completed", [])



def get_leaderboard():
    users = load_users()
    rows = []
    for username, data in users.items():
        p = data.get("progress", default_progress(data.get("name", username)))
        rows.append(
            {
                "username": username,
                "name": p.get("name", username),
                "xp": p.get("xp", 0),
                "level": p.get("level", 1),
                "completed": len(p.get("completed", [])),
                "streak": p.get("streak", 0),
            }
        )
    rows.sort(key=lambda x: (x["xp"], x["completed"], x["streak"]), reverse=True)
    return rows

# ==============================
# UI
# ==============================


def inject_css():
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at top left, rgba(0,255,170,0.08), transparent 20%),
                radial-gradient(circle at top right, rgba(0,153,255,0.08), transparent 22%),
                linear-gradient(180deg, #06111f 0%, #0b1730 48%, #08111f 100%);
        }
        .block-container {padding-top: 1.2rem; padding-bottom: 2rem; max-width: 1200px;}
        .glass {
            padding: 20px;
            border-radius: 22px;
            background: linear-gradient(180deg, rgba(9,18,36,0.96), rgba(10,20,42,0.86));
            border: 1px solid rgba(90,255,200,0.14);
            box-shadow: 0 18px 40px rgba(0,0,0,0.30);
        }
        .hero-title {
            color: white;
            font-size: 2.7rem;
            font-weight: 900;
            line-height: 1.1;
        }
        .hero-sub {
            color: #bfd0ea;
            margin-top: 8px;
            font-size: 1.02rem;
        }
        .pill {
            display:inline-block;
            padding: 8px 12px;
            border-radius: 999px;
            background: rgba(20,31,57,0.96);
            border: 1px solid rgba(90,255,200,0.16);
            color: #dff8ff;
            margin-right: 8px;
            margin-top: 10px;
            font-size: 0.83rem;
        }
        .lesson-card {
            padding: 16px;
            border-radius: 20px;
            background: linear-gradient(180deg, rgba(11,22,43,0.95), rgba(8,15,31,0.92));
            border: 1px solid rgba(93,255,190,0.12);
            min-height: 150px;
            margin-bottom: 12px;
        }
        .lesson-icon {font-size: 2rem; margin-bottom: 8px;}
        .lesson-title {color: white; font-size: 1rem; font-weight: 800;}
        .lesson-meta {color:#aec4e6; font-size:0.85rem; margin-top:6px;}
        .question-card {
            padding: 24px;
            border-radius: 24px;
            background: linear-gradient(180deg, rgba(10,20,38,0.98), rgba(8,15,31,0.94));
            border: 1px solid rgba(93,255,190,0.16);
            box-shadow: 0 18px 40px rgba(0,0,0,0.35);
            animation: slideUpFade 0.38s ease;
            margin-bottom: 16px;
        }
        .question-title {color:white; font-size:1.35rem; font-weight:800; margin-bottom: 6px;}
        .transition-chip {
            display:inline-block;
            padding:10px 14px;
            border-radius:999px;
            background: rgba(28,231,131,0.12);
            border:1px solid rgba(28,231,131,0.24);
            color:#dfffee;
            font-weight:700;
            margin-bottom: 12px;
        }
        .path-node {
            width: 72px; height: 72px; border-radius: 50%;
            display:flex; align-items:center; justify-content:center;
            font-size: 1.7rem; margin: 0 auto 10px auto;
            background: linear-gradient(180deg, #1ce783, #0f9b58);
            box-shadow: 0 10px 25px rgba(0,0,0,0.35);
        }
        .path-node.locked {background: linear-gradient(180deg, #34445d, #202c3c);}
        .center-small {text-align:center; color:#c7d7ef; font-size:0.9rem;}
        @keyframes slideUpFade {
            from {opacity:0; transform: translateY(14px) scale(0.99);} 
            to {opacity:1; transform: translateY(0) scale(1);} 
        }
        </style>
        """,
        unsafe_allow_html=True,
    )



def auth_screen():
    if st.session_state.get("user"):
        return
    inject_css()
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            "<div class='glass' style='display:flex;align-items:center;justify-content:center;height:220px;font-size:88px;'>🐍</div>",
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown("<div class='glass'>", unsafe_allow_html=True)
        st.markdown("<div class='hero-title'>FlickPy</div>", unsafe_allow_html=True)
        st.markdown(
            "<div class='hero-sub'>Aprende Python jugando con niveles, vidas, ranking y modo infinito.</div>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<span class='pill'>42 niveles</span>"
            "<span class='pill'>Ranking</span>"
            "<span class='pill'>Modo infinito</span>",
            unsafe_allow_html=True,
        )
        t1, t2 = st.tabs(["Entrar", "Crear cuenta"])
        with t1:
            u = st.text_input("Usuario", key="login_user")
            p = st.text_input("Contraseña", type="password", key="login_pass")
            if st.button("Entrar", use_container_width=True):
                users = load_users()
                user = users.get(u.strip().lower())
                if user and user.get("password") == hash_pw(p):
                    st.session_state["user"] = u.strip().lower()
                    st.session_state["progress"] = user.get("progress", default_progress(u))
                    st.rerun()
                else:
                    st.error("Usuario o contraseña incorrectos.")
        with t2:
            name = st.text_input("Nombre visible", key="reg_name")
            u2 = st.text_input("Usuario nuevo", key="reg_user")
            p2 = st.text_input("Contraseña", type="password", key="reg_pass")
            code = st.text_input("Código de invitación", key="reg_code")
            if st.button("Crear cuenta", use_container_width=True):
                username = u2.strip().lower()
                users = load_users()
                if code not in INVITE_CODES:
                    st.error("Código inválido.")
                elif not username or not p2 or not name:
                    st.error("Completa todos los campos.")
                elif username in users:
                    st.error("Ese usuario ya existe.")
                else:
                    users[username] = {
                        "password": hash_pw(p2),
                        "progress": default_progress(name.strip()),
                    }
                    save_users(users)
                    st.success("Cuenta creada. Ahora puedes entrar.")
        st.markdown("</div>", unsafe_allow_html=True)
    st.stop()



def render_header(progress):
    left, right = st.columns([5, 1])
    with left:
        st.title(f"{APP_TITLE} · Python game mode")
        st.caption(f"Sesión: {st.session_state.get('user')} · {progress.get('name', 'Estudiante')}")
    with right:
        if st.button("Cerrar sesión", use_container_width=True):
            st.session_state.clear()
            st.rerun()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Nivel", progress.get("level", 1))
    c2.metric("XP", progress.get("xp", 0))
    c3.metric("❤️ Vidas", progress.get("hearts", 5))
    c4.metric("💎 Gemas", progress.get("gems", 0))
    c5.metric("🔥 Racha", progress.get("streak", 0))



def render_path(progress):
    st.markdown("### Ruta principal")
    preview = LESSONS[:8]
    cols = st.columns(len(preview))
    nxt = next_lesson_id(progress)
    for idx, lesson in enumerate(preview):
        done = lesson_completed(progress, lesson["id"])
        locked = not done and lesson["id"] != nxt and nxt is not None
        node_class = "path-node locked" if locked else "path-node"
        label = "✅" if done else ("▶️" if lesson["id"] == nxt else "🔒")
        with cols[idx]:
            st.markdown(
                f"""
                <div class='{node_class}'>{lesson['icon']}</div>
                <div class='center-small'><strong>{lesson['title']}</strong></div>
                <div class='center-small'>{label}</div>
                """,
                unsafe_allow_html=True,
            )



def render_home(progress):
    st.subheader(f"Hola, {progress.get('name', 'Estudiante')} 👋")
    total = len(LESSONS)
    done = len(progress.get("completed", []))
    nxt = next_lesson_id(progress)
    st.progress(done / total if total else 0, text=f"Ruta completada: {done}/{total} niveles")

    a, b, c = st.columns(3)
    with a:
        st.markdown("<div class='glass'><h4 style='color:white;'>Siguiente misión</h4><p style='color:#c7d7ef;'>Continúa tu ruta y desbloquea nuevos temas.</p></div>", unsafe_allow_html=True)
    with b:
        st.markdown("<div class='glass'><h4 style='color:white;'>Modo infinito</h4><p style='color:#c7d7ef;'>Suma XP extra con retos sin límite.</p></div>", unsafe_allow_html=True)
    with c:
        st.markdown("<div class='glass'><h4 style='color:white;'>Ranking</h4><p style='color:#c7d7ef;'>Compite con tus amigos por el top 1.</p></div>", unsafe_allow_html=True)

    if nxt:
        lesson = next(l for l in LESSONS if l["id"] == nxt)
        st.info(f"Tu siguiente nivel es: {lesson['icon']} {lesson['title']} · {lesson['xp']} XP")
        if st.button("▶️ Continuar aprendizaje", type="primary", use_container_width=True):
            st.session_state["selected_lesson_id"] = nxt
            st.session_state["go_to_lessons"] = True
            st.rerun()
    else:
        st.success("🎉 Ya terminaste toda la ruta base. Ahora manda en el modo infinito.")

    render_path(progress)

    st.markdown("### Catálogo de niveles")
    cols = st.columns(3)
    for idx, lesson in enumerate(LESSONS):
        done = lesson_completed(progress, lesson["id"])
        locked = is_lesson_locked(progress, lesson["id"])
        status = "Completada ✅" if done else ("Bloqueada 🔒" if locked else "Disponible 🟡")
        with cols[idx % 3]:
            st.markdown(
                f"""
                <div class='lesson-card'>
                    <div class='lesson-icon'>{lesson['icon']}</div>
                    <div class='lesson-title'>{lesson['title']}</div>
                    <div class='lesson-meta'>{lesson['difficulty']} · {lesson['xp']} XP</div>
                    <div class='lesson-meta'>{status}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )



def render_lessons(progress):
    st.subheader("Lecciones")
    labels = [f"{l['icon']} {l['title']} · {l['difficulty']}" for l in LESSONS]
    default_index = 0
    selected_id = st.session_state.get("selected_lesson_id")
    if selected_id:
        for i, lesson in enumerate(LESSONS):
            if lesson["id"] == selected_id:
                default_index = i
                break
    selected = st.selectbox("Elige una lección", labels, index=default_index)
    lesson = next(l for l in LESSONS if f"{l['icon']} {l['title']} · {l['difficulty']}" == selected)

    if is_lesson_locked(progress, lesson["id"]):
        st.warning("Esa lección está bloqueada. Completa la ruta en orden.")
        return

    lesson_key = f"lesson_state_{lesson['id']}"
    transition_key = f"transition_{lesson['id']}"
    if lesson_key not in st.session_state:
        st.session_state[lesson_key] = {"index": 0, "correct": 0, "finished": False, "awarded": False}
    state = st.session_state[lesson_key]

    with st.container(border=True):
        st.markdown(f"## {lesson['icon']} {lesson['title']}")
        st.caption(f"{lesson['difficulty']} · {lesson['xp']} XP")
        st.write(lesson["theory"])

    total_q = len(lesson["questions"])

    if state["finished"]:
        st.success(f"Lección terminada. Aciertos: {state['correct']}/{total_q}")
        if state["correct"] == total_q:
            if lesson["id"] not in progress["completed"] and not state["awarded"]:
                progress["completed"].append(lesson["id"])
                progress["xp"] += lesson["xp"]
                progress["gems"] += 4
                progress["history"].append({"title": lesson["title"], "xp": lesson["xp"], "date": str(date.today())})
                update_meta(progress)
                st.session_state["progress"] = progress
                state["awarded"] = True
                st.session_state[lesson_key] = state
                persist_current_user()
                st.balloons()
                st.success("Perfecto. Lección completada y recompensas entregadas.")
                st.session_state["selected_lesson_id"] = next_lesson_id(progress)
        else:
            st.warning("No fue perfecta. Reintenta para completar el nivel.")

        c1, c2 = st.columns(2)
        with c1:
            if st.button("Reintentar", use_container_width=True):
                st.session_state[lesson_key] = {"index": 0, "correct": 0, "finished": False, "awarded": False}
                st.session_state[transition_key] = ""
                st.rerun()
        with c2:
            if lesson_completed(progress, lesson["id"]):
                st.success("✅ Nivel completado")
            else:
                st.info("💡 Debes acertar todo")
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
                st.session_state[transition_key] = f"❌ Incorrecto. Quedan {progress['hearts']} vidas"
                persist_current_user()
            state["index"] += 1
            if state["index"] >= total_q:
                state["finished"] = True
            st.session_state[lesson_key] = state
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)



def render_practice(progress):
    st.subheader("Práctica rápida")
    if progress.get("hearts", 0) <= 0:
        st.error("No tienes vidas. Compra más en la tienda.")
        return
    lesson = random.choice(LESSONS)
    q = random.choice(lesson["questions"])
    st.caption(f"Tema: {lesson['title']}")
    if q["type"] == "mc":
        ans = st.radio(q["prompt"], q["options"], index=None)
    else:
        st.write(q["prompt"])
        st.code(q["starter"], language="python")
        ans = st.text_input("Respuesta práctica")
    if st.button("Comprobar práctica", use_container_width=True):
        if ans is None or str(ans).strip() == "":
            st.warning("Debes responder antes de continuar.")
            return
        if str(ans).strip() == str(q["answer"]).strip():
            progress["xp"] += 6
            progress["gems"] += 1
            progress["history"].append({"title": f"Práctica · {lesson['title']}", "xp": 6, "date": str(date.today())})
            update_meta(progress)
            st.session_state["progress"] = progress
            persist_current_user()
            st.success("Correcto. +6 XP y +1 gema")
        else:
            progress["hearts"] = max(0, progress.get("hearts", 5) - 1)
            st.session_state["progress"] = progress
            persist_current_user()
            st.error(f"Incorrecto. Respuesta: {q['answer']}")



def render_infinite(progress):
    st.subheader("Modo infinito ♾️")
    st.write("Retos aleatorios para seguir sumando XP sin límite.")
    if progress.get("hearts", 0) <= 0:
        st.error("No tienes vidas. Recupera corazones en la tienda.")
        return
    if "infinite_question" not in st.session_state:
        lesson = random.choice(LESSONS)
        st.session_state["infinite_question"] = {"lesson": lesson, "question": random.choice(lesson["questions"])}
    payload = st.session_state["infinite_question"]
    lesson = payload["lesson"]
    q = payload["question"]

    a, b, c = st.columns(3)
    a.metric("Racha infinita", progress.get("infinite_streak", 0))
    b.metric("Mejor racha", progress.get("best_infinite_streak", 0))
    c.metric("Recompensa", "+8 XP")

    st.markdown("<div class='question-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='question-title'>{q['prompt']}</div>", unsafe_allow_html=True)
    st.caption(f"Tema: {lesson['title']}")
    inf_key = f"infinite_{lesson['id']}_{q['prompt']}"
    if q["type"] == "mc":
        ans = st.radio("Selecciona una opción", q["options"], index=None, key=inf_key)
    else:
        st.code(q["starter"], language="python")
        ans = st.text_input("Completa", key=inf_key)

    if st.button("Responder reto infinito", type="primary", use_container_width=True):
        if ans is None or str(ans).strip() == "":
            st.warning("Debes responder antes de continuar.")
        else:
            if str(ans).strip() == str(q["answer"]).strip():
                progress["xp"] += 8
                progress["gems"] += 2
                progress["infinite_streak"] = progress.get("infinite_streak", 0) + 1
                progress["best_infinite_streak"] = max(progress.get("best_infinite_streak", 0), progress["infinite_streak"])
                progress["history"].append({"title": f"Infinito · {lesson['title']}", "xp": 8, "date": str(date.today())})
                update_meta(progress)
                st.session_state["progress"] = progress
                persist_current_user()
                st.success("Correcto. +8 XP y +2 gemas")
            else:
                progress["hearts"] = max(0, progress.get("hearts", 5) - 1)
                progress["infinite_streak"] = 0
                st.session_state["progress"] = progress
                persist_current_user()
                st.error(f"Incorrecto. Respuesta: {q['answer']}")
            lesson = random.choice(LESSONS)
            st.session_state["infinite_question"] = {"lesson": lesson, "question": random.choice(lesson["questions"])}
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)



def render_shop(progress):
    st.subheader("Tienda")
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
                    persist_current_user()
                    st.success("Compraste 1 vida")
                else:
                    st.error("No tienes suficientes gemas")
    with c2:
        with st.container(border=True):
            st.markdown("### ❤️❤️ pack x3")
            st.caption("Costo: 25 gemas")
            if st.button("Comprar pack x3", use_container_width=True):
                if progress.get("gems", 0) >= 25:
                    progress["gems"] -= 25
                    progress["hearts"] += 3
                    st.session_state["progress"] = progress
                    persist_current_user()
                    st.success("Compraste 3 vidas")
                else:
                    st.error("No tienes suficientes gemas")



def render_achievements(progress):
    st.subheader("Logros")
    unlocked = set(progress.get("achievements", []))
    for aid, name, _ in ACHIEVEMENTS:
        with st.container(border=True):
            st.markdown(f"### {'🏆' if aid in unlocked else '🔒'} {name}")
            st.caption("Desbloqueado" if aid in unlocked else "Bloqueado")



def render_leaderboard(progress):
    st.subheader("Ranking online")
    st.caption("Este ranking se comparte entre usuarios de la misma app desplegada.")
    leaderboard = get_leaderboard()
    if not leaderboard:
        st.info("Aún no hay usuarios en el ranking.")
        return
    for idx, row in enumerate(leaderboard[:15], start=1):
        badge = "🥇" if idx == 1 else ("🥈" if idx == 2 else ("🥉" if idx == 3 else f"#{idx}"))
        me = row["username"] == st.session_state.get("user")
        with st.container(border=True):
            st.markdown(f"**{badge} {row['name']}** {'← tú' if me else ''}")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("XP", row["xp"])
            c2.metric("Nivel", row["level"])
            c3.metric("Lecciones", row["completed"])
            c4.metric("Racha", row["streak"])



def render_stats(progress):
    st.subheader("Estadísticas")
    a, b, c = st.columns(3)
    a.metric("Lecciones completadas", len(progress.get("completed", [])))
    b.metric("XP total", progress.get("xp", 0))
    c.metric("Mejor racha infinita", progress.get("best_infinite_streak", 0))
    st.markdown("### Actividad reciente")
    history = progress.get("history", [])
    if not history:
        st.info("Aún no hay actividad")
    else:
        for item in reversed(history[-10:]):
            with st.container(border=True):
                st.write(f"**{item['title']}**")
                st.caption(f"{item['date']} · +{item['xp']} XP")



def main():
    st.set_page_config(page_title=APP_TITLE, page_icon="🐍", layout="wide")
    if "user" not in st.session_state:
        st.session_state["user"] = None
    if "progress" not in st.session_state:
        st.session_state["progress"] = default_progress()

    auth_screen()
    inject_css()

    progress = st.session_state.get("progress", default_progress())
    progress = update_meta(progress)
    st.session_state["progress"] = progress
    persist_current_user()

    render_header(progress)

    tabs = st.tabs(["Inicio", "Lecciones", "Práctica", "Infinito", "Tienda", "Ranking", "Logros", "Stats"])
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
        render_infinite(progress)
    with tabs[4]:
        render_shop(progress)
    with tabs[5]:
        render_leaderboard(progress)
    with tabs[6]:
        render_achievements(progress)
    with tabs[7]:
        render_stats(progress)


if __name__ == "__main__":
    main()
