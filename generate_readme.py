import os
from pathlib import Path

# 🔗 Lista de plataformas (com emoji + link)
plataformas = [
    {"nome": "Alura", "emoji": "🎓", "link": "https://www.alura.com.br/"},
    {"nome": "Coursera", "emoji": "🌐", "link": "https://pt.coursera.org/"},
    {"nome": "EdX", "emoji": "📘", "link": "https://www.edx.org/"},
    {
        "nome": "Google",
        "emoji": "🔍",
        "link": "https://developers.google.com/?hl=pt-br",
    },
    {"nome": "LeetCode", "emoji": "💡", "link": "https://leetcode.com"},
    {"nome": "Udemy", "emoji": "📚", "link": "https://www.udemy.com/"},
]

# Converte para dict para lookup rápido
plataformas_dict = {p["nome"]: p for p in plataformas}

# 🧠 Caminho raiz do repositório
ROOT_DIR = Path(__file__).parent
README_PATH = ROOT_DIR / "README.md"

# ✨ Introdução aprimorada
HEADER = """# 🧩 Online Courses Repository

Welcome to my **Online Courses Repository** — a personal archive of programming and technology courses 
I've been studying over the years. While not every piece of content I've created is here, this repository 
brings together most of my learning journey in one place.

Each folder represents a learning **platform**, and each subfolder contains a **specific course** I’ve taken 
(or am currently taking).

Explore freely — maybe you’ll find something inspiring too! 🚀

"""


def generate_readme():
    lines = [HEADER]

    # 📂 Percorre as pastas de plataformas
    for platform_dir in sorted(ROOT_DIR.iterdir()):
        if not platform_dir.is_dir() or platform_dir.name.startswith("."):
            continue

        platform_name = platform_dir.name
        platform_info = plataformas_dict.get(platform_name)
        emoji = platform_info["emoji"] if platform_info else "📁"
        link = platform_info["link"] if platform_info else None

        section_header = (
            f"## {emoji} [{platform_name}]({link})"
            if link
            else f"## {emoji} {platform_name}"
        )
        lines.append(section_header + "\n")

        # 📘 Lista de cursos
        courses = sorted([d for d in platform_dir.iterdir() if d.is_dir()])
        if not courses:
            lines.append("* _(no courses found)_\n\n")
            continue

        for course_dir in courses:
            rel_path = course_dir.relative_to(ROOT_DIR)
            course_name = course_dir.name.replace("-", " ")
            lines.append(f"* [{course_name}]({rel_path}/)\n")

        lines.append("\n")

    # 💾 Escreve o README
    with open(README_PATH, "w", encoding="utf-8") as f:
        f.writelines(lines)

    print(f"✅ README.md generated successfully at {README_PATH}")


if __name__ == "__main__":
    generate_readme()
