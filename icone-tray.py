import pystray
import PIL.Image

Image = PIL.Image.open("dados_forex.png")


def clicar(icon, item):
	print("clicou ...")
	icon.visible = False
	icon.stop()
	os._exit(0)

def sair(icon, item):
	print("saiu ...")
	icon.stop()
	os._exit(0)

def gravador(icon, item):
	print("Gravador ...")
	exec(open("gravador.py").read())
	icon.stop()
	os._exit(0)

def resolution(icon, item):
	print("Gravador ...")
	exec(open("resolution.py").read())
	icon.stop()
	os._exit(0)




icon = pystray.Icon("euBRASIL", Image, title="Eletron-Bit", menu = pystray.Menu(
pystray.MenuItem("euBRASIL", clicar),
pystray.MenuItem("Eletron", sair),
pystray.MenuItem("Gravador", gravador),
pystray.MenuItem("Resolution", resolution),
))

icon.run()
