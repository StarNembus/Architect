from api import Main

main = Main()


@main.route("/home")
def home(request, response):
    response.text = "Привет! Это страница home"


@main.route("/about")
def about(request, response):
    response.text = "Привет! Это страница about"


@main.route("/hello/{name}")
def greeting(request, response, name):
    response.text = f"Hello, {name}"
