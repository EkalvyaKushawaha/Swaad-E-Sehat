import os

p = 'templates/admin'
os.makedirs(p, exist_ok=True)

html_code = """{% extends 'admin/base.html' %}
{% block title %}{{ title }} | Swaad-e-Sehat Admin{% endblock %}
{% block extrastyle %}
{{ block.super }}
<style>
  :root {
    --primary: #133926;
    --secondary: #1d5337;
    --accent: #2ec4b6;
    --gold: #d4a373;
    --bg-light: #f4f7f4;
  }
  body {
    background-color: var(--bg-light) !important;
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif !important;
  }
  #header {
    background: linear-gradient(135deg, #0d281a, #1b4332) !important;
    color: #fff !important;
    padding: 18px 30px !important;
    box-shadow: 0 4px 20px rgba(13,40,26,0.2) !important;
  }
  #branding h1 {
    font-weight: 800 !important;
    letter-spacing: 0.5px !important;
    font-size: 1.35rem !important;
  }
  #branding h1 a:link, #branding h1 a:visited {
    color: #fff !important;
  }
  #user-tools {
    font-size: 0.85rem !important;
    color: #e2e8f0 !important;
  }
  #user-tools a {
    color: #2ec4b6 !important;
    font-weight: 600 !important;
    border-bottom: none !important;
  }
  div.breadcrumbs {
    background: #ffffff !important;
    border-bottom: 1px solid #e2e8f0 !important;
    color: #64748b !important;
    padding: 12px 30px !important;
  }
  div.breadcrumbs a {
    color: var(--secondary) !important;
    font-weight: 600 !important;
  }
  .module {
    background: #ffffff !important;
    border-radius: 14px !important;
    border: 1px solid rgba(0,0,0,0.06) !important;
    box-shadow: 0 8px 25px rgba(0,0,0,0.03) !important;
    margin-bottom: 24px !important;
    overflow: hidden !important;
  }
  .module caption, .module h2 {
    background: linear-gradient(135deg, #133926, #1d5337) !important;
    color: #ffffff !important;
    padding: 12px 18px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
  }
  .module table {
    width: 100% !important;
    border-collapse: collapse !important;
  }
  .module tr th, .module tr td {
    padding: 12px 18px !important;
    border-bottom: 1px solid #f1f5f9 !important;
  }
  .module tr:hover {
    background-color: #f8fafc !important;
  }
  .addlink, .changelink {
    color: var(--primary) !important;
    font-weight: 600 !important;
  }
  .button, input[type=submit], input[type=button], .submit-row input, a.button {
    background: linear-gradient(135deg, #2ec4b6, #208b81) !important;
    border: none !important;
    border-radius: 8px !important;
    color: #fff !important;
    font-weight: 600 !important;
    padding: 10px 18px !important;
    transition: all 0.2s ease !important;
  }
  .button:hover, input[type=submit]:hover {
    background: #186b62 !important;
    transform: translateY(-1px) !important;
  }
  .button.default, input[type=submit].default {
    background: linear-gradient(135deg, #133926, #1d5337) !important;
  }
</style>
{% endblock %}
{% block branding %}
<h1 id="site-name"><a href="{% url 'admin:index' %}">🍃 Swaad-e-Sehat | Master Control Panel</a></h1>
{% endblock %}
"""

with open(os.path.join(p, 'base_site.html'), 'w', encoding='utf-8') as f:
    f.write(html_code)

print("\n>>> SUCCESS: Master Admin Theme Applied! <<<\n")