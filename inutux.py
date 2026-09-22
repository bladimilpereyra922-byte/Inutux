import argparse


def main():
    parser = argparse.ArgumentParser(
        prog="inutux",
        description="CLI oficial de Inutux Marketplace"
    )

    sub = parser.add_subparsers(dest="command")

    sub.add_parser("audit", help="Auditoría completa del proyecto")
    sub.add_parser("doctor", help="Diagnóstico del proyecto")
    sub.add_parser("migrations", help="Revisar migraciones")
    sub.add_parser("models", help="Revisar modelos")
    sub.add_parser("admin", help="Revisar panel admin")
    sub.add_parser("urls", help="Revisar URLs")
    sub.add_parser("security", help="Auditoría de seguridad")
    sub.add_parser("performance", help="Auditoría de rendimiento")
    sub.add_parser("marketplace", help="Auditoría del Marketplace")
    sub.add_parser("database", help="Auditoría de base de datos")
    sub.add_parser("report", help="Generar reporte")

    args = parser.parse_args()

    if args.command == "audit":
        from tools.audit import run
        run()

    elif args.command == "doctor":
        from tools.doctor import run
        run()

    elif args.command == "migrations":
        from tools.migrations import run
        run()

    elif args.command == "models":
        from tools.models import run
        run()

    elif args.command == "admin":
        from tools.admin import run
        run()

    elif args.command == "urls":
        from tools.urls import run
        run()

    elif args.command == "security":
        from tools.security import run
        run()

    elif args.command == "performance":
        from tools.performance import run
        run()

    elif args.command == "marketplace":
        from tools.marketplace import run
        run()

    elif args.command == "database":
        from tools.database import run
        run()

    elif args.command == "report":
        from tools.report import run
        run()

    else:
        parser.print_help()


if __name__ == "__main__":
    main()