from django.template import Template, Context


class TestVersionTag:
    def test_version_returns_formatted_string(self):
        template = Template("{% load core %}{% version %}")
        rendered = template.render(Context({}))
        assert "drips: v" in rendered
        assert rendered.count("v") == 1
