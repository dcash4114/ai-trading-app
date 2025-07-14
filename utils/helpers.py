import logging

def setup_logging():
    logging.basicConfig(filename='log.txt', level=logging.INFO)

def get_theme_stylesheet(theme):
    if theme == "dark":
        return """
        QWidget { background-color: #333; color: #fff; font-family: Arial; }
        QLineEdit { background-color: #555; border: #777; }
        # Neon accents
        QPushButton { background-color: #444; border: #00ff00; }
        """
    return ""

setup_logging()