# Blender-Python
Apuntes blender 2.8x + python API


agregar objeto	shift + A
loop cuts	ctrl + R
parent	ctrl + P
wireframe	z
selecionar todas las caras anillo	alt + click

[segmentos de una esfera](https://i.stack.imgur.com/M8Xp4.gif)

join	ctrl + j
set cursor to world center	ctrl + s
focus an object	numpad .

## Ejecutar Blender desde cmd
```
cd "C:\Program Files\Blender Foundation\Blender 2.81"
.\blender.exe
```

## Instalar liberías con pip en Blender
```
cd "C:\Program Files\Blender Foundation\Blender 2.81\2.81\python\bin"
.\python.exe -m pip install {nombre lib} --user
```

## Referencias

[setup for developing](https://medium.com/@satishgoda/setting-up-blender-2-8-for-developing-with-python-3-7-6330d87c17b4)
[speed up cycles rendering](https://www.blenderguru.com/articles/4-easy-ways-to-speed-up-cycles)
[GPU render by script](https://gist.github.com/S1U/13b8efe2c616a25d99de3d2ac4b34e86#file-render28-py)

## [Libros](http://www.allitebooks.org/)
[The Blender Python API](http://www.allitebooks.org/the-blender-python-api/)
[Blender Cycles Materials & Textures Cookbook](http://www.allitebooks.org/blender-cycles-materials-and-textures-cookbook-third-edition/)

## Commit style

The type is contained within the title and can be one of these types:

- **feat:** a new feature
- **fix:** a bug fix
- **docs:** changes to documentation
- **data:** data transformations or adding (DVCs repos)
- **style:** formatting, missing semi colons, etc; no code change
- **refactor:** refactoring production code
- **test:** adding tests, refactoring test; no production code change
- **chore:** updating build tasks, package manager configs, etc; no production code change

## Jira Taks
[PoC: Generar workers para clasificación](https://odd.atlassian.net/browse/OAIT-299)

## Confluence
[Propuesta I+D: Datasets Artificiales](https://odd.atlassian.net/wiki/spaces/OAT/pages/59441403/Propuesta+I+D+Datasets+Artificiales)