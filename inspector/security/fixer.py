from pathlib import Path
import shutil


class AutoFixEngine:

    def backup(self, file):

        file = Path(file)

        backup = file.with_suffix(
            file.suffix + ".bak"
        )

        shutil.copy2(file, backup)

        return backup

    def restore(self, file):

        file = Path(file)

        backup = file.with_suffix(
            file.suffix + ".bak"
        )

        if backup.exists():

            shutil.copy2(
                backup,
                file,
            )

            return True

        return False

    def replace(

        self,

        file,

        old,

        new,

    ):

        file = Path(file)

        text = file.read_text(
            encoding="utf-8",
            errors="ignore",
        )

        if old not in text:
            return False

        self.backup(file)

        text = text.replace(
            old,
            new,
        )

        file.write_text(
            text,
            encoding="utf-8",
        )

        return True