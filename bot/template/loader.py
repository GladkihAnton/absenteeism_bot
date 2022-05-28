from jinja2 import Environment, FileSystemLoader, Template

jinja_env = Environment(loader=FileSystemLoader('template'))


def render_template(name: str | Template, *args, **kwargs) -> str:
    return jinja_env.get_template(name).render(*args, **kwargs)
