from pathlib import Path
from re import sub
from sys import argv

from behave.model import Feature
from behave.parser import parse_file


def main():
    feature_file_path = argv[1]

    body_content = _parse_feature_to_html(feature_file_path)
    html_content = _prepare_html_content(body_content)

    output_path = Path(feature_file_path).with_suffix('.html').name
    with open(output_path, 'w') as html_file:
        html_file.write(html_content)

    print("HTML file has been generated.")


def _prepare_html_content(body_content: str) -> str:
    head_content = """<meta charset="UTF-8">
          <title>Feature File</title>
          <link rel="stylesheet" href="https://cdn.simplecss.org/simple.min.css">
          <style>
            body {grid-template-columns: 1fr min(55rem, 90%) 1fr;}
          </style>"""

    return f"""<html>
    <head>
        {head_content}
    </head>
    <body>
        {body_content}
    </body>
</html>"""


def _parse_feature_to_html(feature_file_path: str) -> str:
    feature: Feature = parse_file(feature_file_path)
    return _feature_to_html(feature)


def _feature_to_html(feature) -> str:
    scenarios_html = ''
    for scenario in feature.scenarios:
        scenario_html = _scenario_to_html(scenario)
        examples_html = _examples_to_html(scenario.examples[0]) if scenario.examples else ''
        scenarios_html += scenario_html + examples_html

    return (
        f'<h3><b style="color: rgb(160, 47, 111);">{feature.keyword}:</b> '
        f'{feature.name}</h3>\n{scenarios_html}'
    )


def _scenario_to_html(scenario) -> str:
    steps_html = ''.join(_step_to_html(step) for step in scenario.steps)
    return (
        f'<h4><b style="color: rgb(160, 47, 111);">{scenario.keyword}:</b> '
        f'{scenario.name}</h4>\n{steps_html}\n'
    )


def _examples_to_html(examples) -> str:
    header_html = ''.join(f'<th>{col}</th>\n' for col in examples.table.headings)

    rows_html = ''
    for row in examples.table.rows:
        row_html = ''.join(f'<td>{cell}</td>' for cell in row.cells)
        rows_html += f'<tr>{row_html}</tr>\n'

    return f'<table border="1"><tr>{header_html}</tr>{rows_html}</table>\n'


def _step_to_html(step) -> str:
    step_text = _emphasize_columns(step.name)
    keyword_color = 'rgb(32, 94, 166)'
    if step.keyword == 'When':
        keyword_color = 'rgb(188, 82, 21)'
    return (
        f'<div style="margin-left: {20*2}px;">'
        f'<b style="color: {keyword_color};">{step.keyword}</b> {step_text}</div>\n'
    )


def _emphasize_columns(text) -> str:
    """Emphasize column placeholders within the step text."""
    # First, escape HTML to prevent interpretation of < and > as HTML tags
    escaped_text = _escape_html(text)
    # Then, use regular expression to bold the placeholders
    return sub(r'(&lt;.+?&gt;)', r'<b style="color: rgb(173, 131, 1);">\1</b>', escaped_text)


def _escape_html(text) -> str:
    """Escapes HTML special characters in the text."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


if __name__ == "__main__":
    main()
