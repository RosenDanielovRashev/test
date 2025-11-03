import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
from io import BytesIO
import base64
from weasyprint import HTML
import tempfile
import os

st.set_page_config(page_title="Тестово приложение с HTML към PDF", layout="wide")

st.title("📊 Тестово приложение с HTML към PDF конвертиране")
st.markdown("---")

# Секция 1: Въвеждане на данни
st.header("📝 Въвеждане на данни")
col1, col2, col3 = st.columns(3)

with col1:
    име_проект = st.text_input("Име на проект", "Моят тестов проект")
    бюджет = st.number_input("Бюджет (лв)", min_value=0, value=10000)

with col2:
    начало_дата = st.date_input("Начална дата")
    край_дата = st.date_input("Крайна дата")

with col3:
    брой_елементи = st.slider("Брой елементи", 1, 100, 10)
    приоритет = st.selectbox("Приоритет", ["Нисък", "Среден", "Висок"])

# Изчисления
средна_стойност = бюджет / брой_елементи if брой_елементи > 0 else 0
дни_проект = (край_дата - начало_дата).days if край_дата and начало_дата else 0

st.markdown("---")

# Секция 2: Графики
st.header("📈 Графики и визуализации")

# Създаване на примерни данни
данни = pd.DataFrame({
    'Месец': ['Яну', 'Фев', 'Мар', 'Апр', 'Май', 'Юни'],
    'Приходи': np.random.randint(1000, 5000, 6),
    'Разходи': np.random.randint(500, 3000, 6)
})
данни['Печалба'] = данни['Приходи'] - данни['Разходи']

col1, col2 = st.columns(2)

with col1:
    st.subheader("Приходи и разходи")
    fig1 = px.bar(данни, x='Месец', y=['Приходи', 'Разходи'], 
                  title="Приходи и разходи по месеци",
                  barmode='group')
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    st.subheader("Печалба")
    fig2 = px.line(данни, x='Месец', y='Печалба', 
                   title="Печалба по месеци", markers=True)
    fig2.add_hline(y=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig2, use_container_width=True)

# Секция 3: Таблици
st.header("📋 Данни в таблица")
table_data = pd.DataFrame({
    'ID': range(1, 7),
    'Задача': [f'Задача {i}' for i in range(1, 7)],
    'Статус': ['Завършена', 'В прогрес', 'Чакаща', 'Завършена', 'В прогрес', 'Чакаща'],
    'Прогрес %': [100, 75, 0, 100, 50, 25],
    'Отговорен': ['Иван', 'Мария', 'Петър', 'Анна', 'Георги', 'Елена']
})
st.dataframe(table_data, use_container_width=True)

# Функция за създаване на HTML съдържание
def create_html_content():
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="UTF-8">
        <title>Отчет: {име_проект}</title>
        <style>
            @page {{
                margin: 1cm;
                size: A4;
            }}
            body {{
                font-family: Arial, sans-serif;
                margin: 0;
                padding: 20px;
                color: #333;
                line-height: 1.6;
            }}
            .header {{
                text-align: center;
                border-bottom: 2px solid #333;
                padding-bottom: 20px;
                margin-bottom: 30px;
            }}
            .section {{
                margin-bottom: 25px;
                page-break-inside: avoid;
            }}
            .section-title {{
                background-color: #f8f9fa;
                padding: 10px;
                border-left: 4px solid #007bff;
                margin-bottom: 15px;
                font-weight: bold;
                font-size: 16px;
            }}
            .info-grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 10px;
                margin-bottom: 15px;
            }}
            .info-item {{
                padding: 8px;
                border-bottom: 1px solid #eee;
            }}
            .info-label {{
                font-weight: bold;
                color: #555;
            }}
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 15px 0;
                font-size: 12px;
            }}
            th, td {{
                border: 1px solid #ddd;
                padding: 8px;
                text-align: left;
            }}
            th {{
                background-color: #f8f9fa;
                font-weight: bold;
            }}
            .calculation {{
                background-color: #e8f5e8;
                padding: 15px;
                border-radius: 5px;
                margin: 15px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 30px;
                padding-top: 20px;
                border-top: 1px solid #ddd;
                font-size: 11px;
                color: #666;
            }}
            .metrics {{
                display: grid;
                grid-template-columns: repeat(4, 1fr);
                gap: 10px;
                margin: 20px 0;
            }}
            .metric {{
                text-align: center;
                padding: 15px;
                background-color: #f8f9fa;
                border-radius: 5px;
                border: 1px solid #ddd;
            }}
            .metric-value {{
                font-size: 18px;
                font-weight: bold;
                color: #007bff;
            }}
            .metric-label {{
                font-size: 12px;
                color: #666;
            }}
        </style>
    </head>
    <body>
        <div class="header">
            <h1>ОТЧЕТ: {име_проект}</h1>
            <p>Генериран на: {datetime.now().strftime("%Y-%m-%d %H:%M")}</p>
        </div>

        <div class="section">
            <div class="section-title">📝 Основни параметри</div>
            <div class="info-grid">
                <div class="info-item">
                    <span class="info-label">Име на проект:</span> {име_проект}
                </div>
                <div class="info-item">
                    <span class="info-label">Бюджет:</span> {бюджет} лв
                </div>
                <div class="info-item">
                    <span class="info-label">Начална дата:</span> {начало_дата}
                </div>
                <div class="info-item">
                    <span class="info-label">Крайна дата:</span> {край_дата}
                </div>
                <div class="info-item">
                    <span class="info-label">Брой елементи:</span> {брой_елементи}
                </div>
                <div class="info-item">
                    <span class="info-label">Приоритет:</span> {приоритет}
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">🧮 Изчисления</div>
            <div class="calculation">
                <p><strong>Средна стойност на елемент:</strong> {средна_стойност:.2f} лв</p>
                <p><strong>Продължителност на проекта:</strong> {дни_проект} дни</p>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📊 Финансови показатели</div>
            <div class="metrics">
                <div class="metric">
                    <div class="metric-value">{данни['Приходи'].sum()} лв</div>
                    <div class="metric-label">Общ приход</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{данни['Разходи'].sum()} лв</div>
                    <div class="metric-label">Общ разход</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{данни['Печалба'].sum()} лв</div>
                    <div class="metric-label">Обща печалба</div>
                </div>
                <div class="metric">
                    <div class="metric-value">{данни['Печалба'].mean():.1f} лв</div>
                    <div class="metric-label">Средна печалба</div>
                </div>
            </div>
        </div>

        <div class="section">
            <div class="section-title">📋 Списък със задачи</div>
            <table>
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Задача</th>
                        <th>Статус</th>
                        <th>Прогрес %</th>
                        <th>Отговорен</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Добавяне на редовете в таблицата
    for _, row in table_data.iterrows():
        html_content += f"""
                    <tr>
                        <td>{row['ID']}</td>
                        <td>{row['Задача']}</td>
                        <td>{row['Статус']}</td>
                        <td>{row['Прогрес %']}%</td>
                        <td>{row['Отговорен']}</td>
                    </tr>
        """
    
    html_content += """
                </tbody>
            </table>
        </div>

        <div class="section">
            <div class="section-title">📈 Месечни данни</div>
            <table>
                <thead>
                    <tr>
                        <th>Месец</th>
                        <th>Приходи (лв)</th>
                        <th>Разходи (лв)</th>
                        <th>Печалба (лв)</th>
                    </tr>
                </thead>
                <tbody>
    """
    
    # Добавяне на финансовите данни
    for _, row in данни.iterrows():
        html_content += f"""
                    <tr>
                        <td>{row['Месец']}</td>
                        <td>{row['Приходи']}</td>
                        <td>{row['Разходи']}</td>
                        <td style="color: {'green' if row['Печалба'] >= 0 else 'red'}">{row['Печалба']}</td>
                    </tr>
        """
    
    html_content += f"""
                </tbody>
            </table>
        </div>

        <div class="footer">
            <p>Този отчет е генериран автоматично от тестовото приложение.</p>
            <p>Съдържа всички въведени данни, изчисления и таблици.</p>
        </div>
    </body>
    </html>
    """
    
    return html_content

# Функция за конвертиране на HTML към PDF
def html_to_pdf(html_content):
    # Създаване на временен файл
    with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False, encoding='utf-8') as f:
        f.write(html_content)
        temp_html = f.name
    
    try:
        # Конвертиране на HTML към PDF
        pdf_bytes = HTML(temp_html).write_pdf()
        return pdf_bytes
    except Exception as e:
        st.error(f"Грешка при конвертиране: {str(e)}")
        return None
    finally:
        # Изтриване на временния файл
        try:
            os.unlink(temp_html)
        except:
            pass

# Секция за генериране на PDF
st.markdown("---")
st.header("📄 Генериране на PDF отчет от HTML")

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
    ### 🎯 Преимущества:
    - **Професионално форматиране**
    - **Стилове и CSS**
    - **Таблици и метрики**
    - **Автоматично генериране**
    - **Висока качество на PDF**
    """)

with col2:
    if st.button("🔄 Генерирай PDF от HTML", type="primary", use_container_width=True):
        with st.spinner("Генериране на PDF..."):
            try:
                # Създаване на HTML съдържание
                html_content = create_html_content()
                
                # Конвертиране към PDF
                pdf_bytes = html_to_pdf(html_content)
                
                if pdf_bytes:
                    # Създаване на download бутон
                    st.download_button(
                        label="📥 Изтегли PDF файл",
                        data=pdf_bytes,
                        file_name=f"отчет_{име_проект}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf",
                        mime="application/pdf",
                        type="primary",
                        use_container_width=True
                    )
                    
                    st.success("✅ PDF отчетът е генериран успешно!")
                    
                    # Показване на HTML preview
                    with st.expander("🔍 Преглед на HTML съдържанието"):
                        st.code(html_content, language='html')
                else:
                    st.error("❌ Неуспешно генериране на PDF")
                    
            except Exception as e:
                st.error(f"❌ Грешка: {str(e)}")

# Информация за технологията
st.markdown("---")
st.info("""
**Технология:** Този подход използва **WeasyPrint** за конвертиране на HTML и CSS към PDF. 
Това позволява пълно контролиране на оформлението и стиловете, като същевременно 
генерира висококачествени PDF документи.
""")
