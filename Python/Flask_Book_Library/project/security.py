from html import escape, unescape


def escape_html_text(value):
    if value is None:
        return None
    return escape(unescape(str(value)))