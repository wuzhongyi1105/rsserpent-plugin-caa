from rsserpent.models import Persona, Plugin

from . import html


plugin = Plugin(
    name="rsserpent-plugin-caa",
    author=Persona(
        name="wuzhongyi1105",
        link="https://github.com/wuzhongyi1105",
        email="dw@watelier.cn",
    ),
    prefix="/caa",
    repository="https://github.com/wuzhongyi1105/rsserpent-plugin-caa",
    routers={html.path: html.provider},
)
