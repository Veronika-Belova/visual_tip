import time
import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import streamlit as st
import plotly.express as px



st.write("""## Чаевые в ресторане""")
path = 'https://raw.githubusercontent.com/mwaskom/seaborn-data/master/tips.csv'
tips = pd.read_csv(path)
st.dataframe(tips)

@st.cache_data
def convert_df(tips):
    return tips.to_csv().encode('utf-8')

csv = convert_df(tips)
st.download_button(
    label="Download data as CSV",
    data=csv,
    file_name='tips.csv.csv',
    mime='text/csv',
)

tips['time_order']= pd.DataFrame(np.random.choice(pd.date_range('2023-01-01', '2023-01-31'), 244))

st.write("""### Построение график, показывающего динамику чаевых во времени""")

plt.style.use('ggplot')
fig, ax = plt.subplots(figsize=(10, 5))
sns.lineplot(data=tips, x="time_order", y="tip", hue="time", ax=ax)
plt.xticks(rotation=60, size=13, color='k')
st.pyplot(fig)

st.write("""### Построение гистограммы для **total_bill**""")

fig, ax = plt.subplots(figsize=(10, 5))
min_value = float(0)
max_value = tips["total_bill"].max()
bin_width = (max_value - min_value) / 50
value = st.slider("Выберите диапазон значений:", min_value, max_value, (min_value, max_value), step=bin_width)
filtered_data = tips[(tips["total_bill"] >= value[0]) & (tips["total_bill"] <= value[1])]
sns.histplot(data=filtered_data, x="total_bill", ax=ax, color='purple')
st.pyplot(fig)


st.write("""### На графике видна разница суммы чека в зависимости от времени""")

fig = px.histogram(tips, x="total_bill", color="time", hover_data=tips.columns)
fig.update_layout(plot_bgcolor='lightgray')
fig.update_traces(marker=dict(line=dict(width=0.5, color='black')))
st.plotly_chart(fig)

st.write("""### Scatterplot, показывающий связь между total_bill and tip""")

fig, ax = plt.subplots(figsize=(5, 5))
sns.scatterplot(data=tips, x='total_bill', y='tip', hue='time', s=30)
st.pyplot(fig)


st.write("""### График, который связывает total_bill, tip, и size""")

fig = px.scatter(tips, x="total_bill", y="tip", color="size", hover_data=tips.columns)
fig.update_layout(plot_bgcolor='lightgray', paper_bgcolor='darkslategrey')
fig.update_traces(marker=dict(line=dict(width=0.5, color='black')))
st.plotly_chart(fig)

st.write("""### График, показывающий вязь между днем недели и размером счета""")
fig = px.scatter(tips, x="total_bill", y="tip", color="day", facet_col="day", facet_col_wrap=2, height=500)
fig.update_layout(paper_bgcolor="#f5f5f5", plot_bgcolor="#ffffff", margin=dict(l=20, r=20, b=20, t=20))
st.plotly_chart(fig)


st.write("""**Я думаю вы немного проголодались за время изучения графиков, давайте перекусим**""")
def cook_snack():
    msg = st.toast('Gathering ingredients...')
    time.sleep(2)
    msg.toast('Cooking...')
    time.sleep(2)
    msg.toast('Ready! Bon appetit!', icon = "🥞")

if st.button('Cook snack'):
    cook_snack()

st.write("""### Scatter plot с днем недели по оси Y, чаевыми по оси X, и цветом по полу""")

fig = px.scatter(tips, x="tip", y="day", color="sex", hover_data=tips.columns, height=500)
fig.update_layout(plot_bgcolor='lightgray', paper_bgcolor='darkslategrey')
st.plotly_chart(fig)

st.write("""### Box plot c суммой всех счетов за каждый день,по time (Dinner/Lunch)""")
fig = px.box(tips, x="day", y="total_bill", color="time")
fig.update_layout(width=600, height=400)
fig.update_layout(
    plot_bgcolor='lightgray', 
    paper_bgcolor='darkslategrey'
)
st.plotly_chart(fig)

st.write("""### 2 гистограммы чаевых на обед и ужин. Расположите их рядом по горизонтали""")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 5))
tips[tips['time'] == 'Lunch'].tip.hist(ax=ax1, bins=20, alpha=0.5, label='Lunch', edgecolor='black')
tips[tips['time'] == 'Dinner'].tip.hist(ax=ax2, bins=20, alpha=0.5, label='Dinner', edgecolor='black')
ax1.set_title('Чаевые на обед')
ax2.set_title('Чаевые на ужин')
st.pyplot(fig)


st.write("""### 2 scatterplots (для мужчин и женщин), которые показывают связь размера счета и чаевых, дополнительно разбиты на курящий/некурящий.""")
st.write("""***Используй фильтр чаевых для более точной оценки***""")

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 8))

filtered_data = tips.copy()
filtered_data['smoker'] = pd.Categorical(filtered_data['smoker']).codes
st.sidebar.title('Фильтры данных для scatter plots')

tip_threshold = st.sidebar.slider('Минимальный размер чаевых', 0.0, 10.0, 0.0)
filtered_data = filtered_data.query(f'tip > {tip_threshold}')

filtered_data[filtered_data['sex'] == 'Male'].plot.scatter(x='total_bill', y='tip', c='smoker', colormap='viridis', ax=ax1)
filtered_data[filtered_data['sex'] == 'Female'].plot.scatter(x='total_bill', y='tip', c='smoker', colormap='viridis', ax=ax2)
ax1.set_title('Чаевые в зависимости от размера счета (мужчины)')
ax2.set_title('Чаевые в зависимости от размера счета (женщины)')
st.pyplot(fig)


st.write("""### Тепловая карта зависимостей численных переменных""")
fig, ax = plt.subplots(figsize=(10, 6))
heatmap = sns.heatmap(tips.corr(), annot=True, cmap="crest", linewidths=0.5)
st.pyplot(fig)

st.success('DONE DONE DONE!', icon="✅")