from pathlib import Path


def run():
    root = Path.cwd()

    print("\n========== AUDITORÍA INUTUX ==========\n")

    apps = [
        p.name
        for p in root.iterdir()
        if p.is_dir() and (p / "models.py").exists()
    ]

    print(f"Apps encontradas: {len(apps)}")
    for app in apps:
        print(f"  ✔ {app}")

    print()

    py_files = list(root.rglob("*.py"))
    migrations = list(root.rglob("migrations/*.py"))
    models = list(root.rglob("models.py"))
    admins = list(root.rglob("admin.py"))

    print(f"Archivos Python : {len(py_files)}")
    print(f"Modelos         : {len(models)}")
    print(f"Admins          : {len(admins)}")
    print(f"Migraciones     : {len(migrations)}")

    print("\nAuditoría completada.")