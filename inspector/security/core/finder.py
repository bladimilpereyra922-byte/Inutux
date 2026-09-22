class Finder:

    def __init__(self, project):

        self.project = project

    def files(self, group):

        return self.project.get(group, [])

    def python(self):

        return self.files("python")

    def settings(self):

        return self.files("settings")

    def urls(self):

        return self.files("urls")

    def models(self):

        return self.files("models")

    def views(self):

        return self.files("views")

    def forms(self):

        return self.files("forms")

    def admin(self):

        return self.files("admin")

    def serializers(self):

        return self.files("serializers")

    def env(self):

        return self.files("env")

    def docker(self):

        return self.files("docker")

    def requirements(self):

        return self.files("requirements")

    def manage(self):

        return self.files("manage")

    def html(self):

        return self.files("html")

    def javascript(self):

        return self.files("javascript")

    def css(self):

        return self.files("css")

    def yaml(self):

        return self.files("yaml")

    def json(self):

        return self.files("json")

    def toml(self):

        return self.files("toml")

    def all(self):

        return self.files("all_files")