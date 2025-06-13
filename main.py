# main.py
def generate_html():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pickleball Hello</title>
    </head>
    <body>
        <h1>Hello, Pickleball World!</h1>
    </body>
    </html>
    """
    with open("output/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML generated at output/index.html")

if __name__ == "__main__":
    generate_html()