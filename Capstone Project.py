import streamlit as st
import pandas as pd
import altair as alt
import joblib
from keras.models import load_model
from PIL import Image

st.set_page_config(
    page_title = 'Project 2',
    layout = 'wide'
    )

# Data Preparation
tax_revenue_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\Tax Revenue\Tax Revenue Data.csv") # dari OECD
cpi_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\CPI Data\CPI Data.csv") # dari transparency international 
population_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\Population Data\Population Data.csv") # dari world bank
gdp_per_capita_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\GDP per Capita\GDP per Capita.csv") # dari world bank
inflation_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\Inflation Rate\Inflation Rate.csv") # dari world bank
unemployment_df = pd.read_csv("D:/Latihan Coding/TETRIS CEO BATCH 3/CAPSTONE PROJECT/Data/Unemployment Rate/Unemployment Rate.csv") # dari world bank
populationgrowth_df = pd.read_csv("D:/Latihan Coding/TETRIS CEO BATCH 3/CAPSTONE PROJECT/Data/Population Growth/Population Growth.csv") # dari world bank
fdi_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\FDI Data\FDI Data.csv") # dari world bank
labour_df = pd.read_csv("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Data\Labour Force Data\Labour Force.csv") # dari world bank

# Data Cleaning and Preprocessing
year_list = [x for x in range(2011,2021)]
str_year_list = [str(year) for year in range(2011, 2021)]
column_list = ['COU','Tax revenue','Year','Value']
clean_tax_revenue_df = tax_revenue_df[(tax_revenue_df['Indicator'] == "Tax revenue as % of GDP") & (tax_revenue_df['Tax revenue'] == '1000 Taxes on income, profits and capital gains') & (tax_revenue_df['Level of government'] == 'Total') & (tax_revenue_df['Year'].isin(year_list))][column_list]
clean_tax_revenue_df = clean_tax_revenue_df.rename(columns= {'COU':'Country Code'})
column_list = ['Year', 'Country', 'ISO3', 'CPI Score', 'Region']
clean_cpi_df = cpi_df[cpi_df.Year != 2010][column_list]
clean_cpi_df = clean_cpi_df.rename(columns = {'ISO3':'Country Code'})
clean_population_df = population_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_population_df = pd.melt(clean_population_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Population'})
clean_population_df['Year'] = clean_population_df['Year'].astype(int)
clean_gdp_per_capita_df = gdp_per_capita_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_gdp_per_capita_df = pd.melt(clean_gdp_per_capita_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'GDP per Capita'})
clean_gdp_per_capita_df['Year'] = clean_gdp_per_capita_df['Year'].astype(int)
clean_inflation_df = inflation_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_inflation_df = pd.melt(clean_inflation_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Inflation Rate'})
clean_inflation_df['Year'] = clean_inflation_df['Year'].astype(int)
clean_unemployment_df = unemployment_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_unemployment_df = pd.melt(clean_unemployment_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Unemployment Rate'})
clean_unemployment_df['Year'] = clean_unemployment_df['Year'].astype(int)
clean_populationgrowth_df = populationgrowth_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_populationgrowth_df = pd.melt(clean_populationgrowth_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Population Growth'})
clean_populationgrowth_df['Year'] = clean_populationgrowth_df['Year'].astype(int)
clean_fdi_df = fdi_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_fdi_df = pd.melt(clean_fdi_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Foreign Direct Investment'})
clean_fdi_df['Year'] = clean_fdi_df['Year'].astype(int)
clean_labour_df = labour_df[['Country Code'] + ['Country Name'] + str_year_list]
clean_labour_df = pd.melt(clean_labour_df, id_vars=['Country Name','Country Code'], value_vars=str_year_list).rename(columns = {'Country Name':'Country','variable':'Year', 'value':'Labour Force'})
clean_labour_df['Year'] = clean_labour_df['Year'].astype(int)
merge_df = pd.merge(clean_tax_revenue_df, clean_population_df, how='left', left_on=['Country Code','Year'], right_on = ['Country Code','Year'])
merge_df = pd.merge(merge_df, clean_cpi_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_gdp_per_capita_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_inflation_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_populationgrowth_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_fdi_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_unemployment_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df = pd.merge(merge_df, clean_labour_df, how='left', left_on=['Country','Country Code','Year'], right_on = ['Country','Country Code','Year'])
merge_df['Labour Force Rate'] = merge_df['Labour Force']/merge_df['Population']
merge_df = merge_df.rename(columns={'Value':'% Tax Revenue per GDP'})
merge_df = merge_df[['Country Code','Country','Region','Year','Tax revenue','% Tax Revenue per GDP','CPI Score','GDP per Capita','Inflation Rate','Foreign Direct Investment','Population Growth','Unemployment Rate','Population','Labour Force Rate']]
merge_df = merge_df.dropna()
parameter_list = ['% Tax Revenue per GDP','CPI Score','GDP per Capita','Inflation Rate','Population Growth','Unemployment Rate','Labour Force Rate']
for i in parameter_list:
    merge_df = merge_df[merge_df[i] != 0]
tax_df = merge_df.drop(['Population','Foreign Direct Investment'], axis = 1)

# Streamlit
st.markdown("<h1 style='text-align: center; margin-top: 0px'>Indonesia's Income and Capital Gain Tax Policy Performance Analysis over 10 Years from 2011 to 2020</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; line-height: 0.5;'>Author : Jevis Xandra</h4>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; line-height: 0.5'>Created on : 11 June 2023</h4>", unsafe_allow_html=True)
st.markdown("""___""")

st.markdown("<h2 style='text-align: left;'>Introduction to Tax</h2>", unsafe_allow_html=True)
col1, col2, col3 = st.columns(3)
col1.markdown("<h3 style='text-align: center;'>What is tax?</h3>", unsafe_allow_html=True)
col3.markdown("<h3 style='text-align: center;'>What is tax policy?</h3>", unsafe_allow_html=True)
col2.markdown("<h3 style='text-align: center;'>What is income and capital gain tax?</h3>", unsafe_allow_html=True)

exp1, exp2, exp3 = st.columns(3)
text_exp1 = "According to Investopedia, Taxes are mandatory contributions levied on individuals or corporations by a government entity—whether local, regional, or national. Tax revenues finance government activities, including public works and services such as roads and schools, or programs such as Social Security and Medicare. "
exp1.markdown("<p style='text-align: justify; font-size: 16px;'>" + text_exp1 + "</p>",
            unsafe_allow_html=True)
text_exp2 = "According to Investopedia, Income tax is paid on earnings from employment, interest, dividends, royalties, or self-employment, whether it’s in the form of services, money, or property. Capital gains tax is paid on income that derives from the sale or exchange of an asset, such as a stock or property that’s categorized as a capital asset."
exp2.markdown("<p style='text-align: justify; font-size: 16px;'>" + text_exp2 + "</p>",
            unsafe_allow_html=True)
text_exp3 = "Tax policy refers to the guidelines and principles established by a government for the imposition and collection of taxes. It encompasses both microeconomic and macroeconomic aspects, with the former focusing on issues of fairness and efficiency in tax collection, and the latter focusing on the overall quantity of taxes to be collected and its impact on economic activity."
exp3.markdown("<p style='text-align: justify; font-size: 16px;'>" + text_exp3 + "</p>",
            unsafe_allow_html=True)

st.markdown("<h3 style=''>" + "We have known a little about tax, let's talk about tax system in Indonesia"  + "</h3>",
            unsafe_allow_html=True)
text_pajak_indonesia_1 = "In Indonesia, there are several type of taxes that can be categorized based on their characteristic including : taxes' collection method, taxes' nature, and taxes' collecting institutions."
text_pajak_indonesia_2 = " The type of taxes based on the collection method are direct taxes and indirect taxes, the types of taxes based on their nature are subjective taxes and objective taxes. Last, the types of taxes based on the collecting institutions are central taxes and regional taxes."
st.markdown("<p style='text-align: justify; font-size: 16px;'>" + text_pajak_indonesia_1 + text_pajak_indonesia_2  + "</h3>",
            unsafe_allow_html=True)

tax1, tax2, tax3 = st.columns(3)
tax1.markdown("<h5 style='text-align: center;'>Direct and Indirect Tax</h5>", unsafe_allow_html=True)
tax2.markdown("<h5 style='text-align: center;'>Subjective and Objective Tax</h5>", unsafe_allow_html=True)
tax3.markdown("<h5 style='text-align: center;'>Central Tax and Regional Tax</h5>", unsafe_allow_html=True)

taxexp1, taxexp2, taxexp3 = st.columns(3)
tax_exp1_1 = "Direct tax is a tax that is borne directly by the taxpayer and cannot be transferred to others."
tax_exp1_2 = " In other words, the process of paying taxes must be done by the taxpayer themselves."
tax_exp1_3 = " For example, a child cannot transfer the tax burden to their parents, and similarly, a husband cannot transfer their tax obligation to their wife."
tax_exp1_4 = " On the other hand, Indirect tax is a tax where the burden can be shifted to others because this type of tax does not have a tax assessment notice."
tax_exp1_5 = " It means that the imposition of tax is not done periodically but is linked to specific events or actions, allowing the payment of taxes to be delegated to others."
taxexp1.markdown("<p style='text-align: justify; font-size: 16px;'>" + tax_exp1_1 + tax_exp1_2 + tax_exp1_3 + tax_exp1_4 + tax_exp1_5 + "</p>",
            unsafe_allow_html=True)
tax_exp2_1 = "Subjective tax is a tax that is based on the taxpayer, while objective tax is based on the tax object."
tax_exp2_2 = " A levy is called a subjective tax because it considers the taxpayer's circumstances."
tax_exp2_3 = " An example of a subjective tax is income tax (PPh), which takes into account the taxpayer's ability to generate income or money."
tax_exp2_4 = " Objective tax is a levy that considers the value of the tax object."
tax_exp2_5 = " An example of an objective tax is Value Added Tax (PPn) on taxable goods."
taxexp2.markdown("<p style='text-align: justify; font-size: 16px;'>" + tax_exp2_1 + tax_exp2_2 + tax_exp2_3 + tax_exp2_4 + tax_exp2_5 + "</p>",
            unsafe_allow_html=True)
tax_exp3_1 = "Central tax is a tax collected and managed by the Central Government, primarily handled by the Directorate General of Taxes (DJP)."
tax_exp3_2 = " The revenue collected from this type of tax is then used to finance state expenditures such as road construction, school development, healthcare assistance, and other purposes."
tax_exp3_3 = " On the other hand, local tax, or regional tax, is a tax collected and managed by the Local Government at the provincial and regency/municipality levels."
tax_exp3_4 = " The revenue collected from this type of tax is then used to finance local government expenditures."
taxexp3.markdown("<p style='text-align: justify; font-size: 16px;'>" + tax_exp3_1 + tax_exp3_2 + tax_exp3_3 + tax_exp3_4 + "</p>",
            unsafe_allow_html=True)

st.markdown(" ")

st.markdown("<h2 style=''>" + "Project Introduction"  + "</h2>",
            unsafe_allow_html=True)


pocol1, pocol2 = st.columns([3,7])
with pocol1:
    image_1 = Image.open("D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\Image\Berita_1.jpg")
    st.image(image_1, caption='Sumber : Pajakku.com', use_column_width=True)
with pocol2:
    potext_1 = " Menteri Keuangan Sri Mulyani Indrawati mengatakan rasio pajak Indonesia rendah. Penyebab rendahnya rasio pajak Indonesia dikarenakan tingkat kepatuhan masyarakat membayar pajak masih rendah. Tidak hanya itu, sebagian masyarakat yang masih menganggap membayar pajak merupakan bentuk penjajahan dan bukan suatu kewajiban."
    potext_2 = " Menurut Ekonom dari Institute for Development of Economics and Finance (INDEF), Bhima Yudhistira. Ia menyampaikan bahwa penerimaan pajak rendah bukan hanya dikarenakan pandangan negatif tersebut, namun masih banyak masyarakat kelas atas yang lari dari hak dan kewajiban dalam menjalankan perpajakan."
    potext_3 = " Bhima Yushistira menyampaikan kepada detik.com pada Jumat (04/12/2020), bahwa masih banyak masyarakat dari kelas atas yang belum memiliki Nomor Pokok Wajib Pajak atau NPWP. Meski demikian, saat ini mahasiswa diberikan sosialisasi dan diberikan himbauan untuk memiliki NPWP. Hal tersebut menjadi penyebab ketimpangan perpajakan yang menjadi akar kendalanya."
    potext_4 = " Bagaimanapun juga, pemerintah tidak dapat menjadikan hal tersebut sebagai alasan. Pemerintah bisa saja lebih banyak memungut pagi dari masyarakat dengan pendapatan yang rendah dibandingkan Wajib Pajak dengan penghasilan tinggi."
    potext_5 = " Bhima Yudhistira juga menyampaikan bahwa rendahnya rasio pajak ini tidak dapat kemudian disalahkan begitu saja, seperti Unit, Menengah, Kecil, dan Mikro yang belum melakukan pembayaran pajak karena menilai bayar pajak sebagai bentuk penjajahan. Apabila pemerintah tidak dapat bersikap tegas dalam memungut pajak, maka akan ada Wajib Pajak yang tidak mau membayar pajak."
    st.markdown("<p style='text-align: justify; font-size: 18px;'>" + potext_1 + potext_2 + potext_3 + potext_4 + potext_5 + "</h3>",
                unsafe_allow_html=True)



porev_1 = "Based on the news from Indonesia above, Minister of Finance Sri Mulyani Indrawati stated that the low tax ratio in Indonesia is caused by the low compliance rate of the society in paying taxes, and some people still perceive tax payment as a form of colonization."
porev_2 = " The question is are these the only causes? Has the tax regulation been perfectly assessed to adapt to the country's conditions so that people do not hesitate to paying taxes?"
porev_3 = " In this project, we will explore all the facts to answer these questions."
porev_4 = " In this project, the determination of the performance of tax policies regarding income and capital gain tax in Indonesia is based on the deficit of predicted tax revenue per GDP compared to actual tax revenue per GDP."
porev_5 = " Tax policy is intentionally not included among the variables used to predict tax revenue per GDP. Therefore, if the prediction results show a higher figure than the actual condition, it can be assumed that outside of the variables used, there are factors that cause the tax performance to decrease to a lower figure, and one of these variables is tax policy."
porev_6 = " Thus, if the prediction results show an increasing figure compared to the actual condition, it means that the performance of tax policies regarding income and capital gain tax in Indonesia is getting worse."
st.markdown("<p style='text-align: justify; font-size: 16px;'>" + porev_1 + porev_2 + porev_3 + porev_4 + porev_5 + porev_6 + "</h3>",
unsafe_allow_html=True)

st.markdown("<h2 style=''>" + "Project Step"  + "</h2>",
            unsafe_allow_html=True)
step1, step2, step3 = st.columns(3)
with step1:
    st.markdown("<h3 style='text-align: center;'>Step 1 : Data Preparation </h3>",
            unsafe_allow_html=True)
with step2:
    st.markdown("<h3 style='text-align: center;'>Step 2 : Data Exploration </h3>",
            unsafe_allow_html=True)
with step3:
    st.markdown("<h3 style='text-align: center;'>Step 3 : Data Cleaning and Pre-processing </h3>",
            unsafe_allow_html=True)
step1_sub, step2_sub, step3_sub = st.columns(3)
with step1_sub:
    step1_text1 = "In this step, there are several data that I have prepared to build a machine learning model that will be used to predict the realization of income and capital gain tax in Indonesia. The initial selection of parameters to build the machine learning model includes 8 parameters : "
    step1_text2 = "<br> 1. % Tax Revenue per GDP data from OECD <br> 2. Corruption Perception Index data from Transparency International <br> 3. Population data from the World Bank <br> 4. GDP per Capita data from the World Bank <br> 6. Unemployment Rate data from the World Bank <br> 7. Population Growth data from the World Bank <br> 8. Foreign Direct Investment data from the World Bank <br> 9. Labour Force Rate data from the World Bank"
    step1_text3 = "<br> However, in the subsequent data processing, some parameters are discarded due to their low correlation with the level of realization of income and capital gain tax."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step1_text1 + step1_text2 + step1_text3 + "</h3>",
    unsafe_allow_html=True)
with step2_sub:
    step2_text1 = "In this phase, I conducted data exploration related to the data that I will use. The exploration starts with checking the contents of the table to understand the overall layout of the table, followed by checking the table's information such as the number of rows, number of columns, number of rows containing null values, and the data types of each column." 
    step2_text2 = " Such checks are performed for all the datasets that have been collected, starting from the % Tax Revenue per GDP data to the Labour Force Rate data."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step2_text1 + step2_text2 + "</h3>",
    unsafe_allow_html=True)
with step3_sub:
    step3_text1 = "After going through the data exploration phase, we now have an understanding of the data contents. In this phase, the previously separate data will be combined into a single table, keeping the desired columns or parameters and removing unwanted parameters. Several steps are taken in this phase: "
    step3_text2 = "<br>1. Rearranging the table format for each dataset to make them compatible for merging.<br>2. Adjusting the data types of the tables if needed.<br>3. Combining all the data into a single table with the desired parameters.<br>4. Removing rows containing null values.<br>5. Removing rows with a value of 0 in the % Tax Revenue per GDP variable.<br>6. Checking the correlation between variables.<br>7. Discarding parameters/variables with low correlation to the target variable."
    step3_text3 = "Once all these steps are completed, the data is ready to be used for building a machine learning model."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step3_text1 + step3_text2 + step3_text3 + "</h3>",
    unsafe_allow_html=True)





step4, step5, step6 = st.columns(3)
with step4:
    st.markdown("<h3 style='text-align: center;'>Step 4 : Data Visualization </h3>",
            unsafe_allow_html=True)
    step4_text1 = "The visualization phase aims to gain insights from the data in a more visually appealing and understandable manner. Data visualization is performed using Python and Tableau."
    step4_text2 = "<br> In Python: <br>1. Heatmap visualization is used to examine the correlation between parameters in the data for each year.<br>2. Graph visualization is used to compare the predicted and actual values of income and value-added tax realizations."
    step4_text3 = "<br>In Tableau:<br>1. Visualization is done to show the levels of income and value-added tax realizations based on countries.<br>2. Frequency distribution visualization is used to assess the distribution of various parameters or variables that contribute to the level of income and value-added tax realizations.<br>3. Line chart visualization shows the trends of income tax realization per GDP (%), CPI Score, and GDP per Capita (USD) from 2011 to 2020."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step4_text1 + step4_text2 + step4_text3 + "</h3>",
    unsafe_allow_html=True)
with step5:
    st.markdown("<h3 style='text-align: center;'>Step 5 : Machine Learning </h3>",
            unsafe_allow_html=True)
    step5_text1 = "In this phase, a linear regression machine learning model will be created using the sklearn module in Python. The details of the steps in this phase are as follows: "
    step5_text2 = "<br>1. Defining X and y for the machine learning model.<br>2. Performing train-test split for X and y.<br>3. Defining the linear regression model.<br>4. Training the model using the training data.<br>5. Making predictions on the testing data to evaluate the model's performance.<br>6. It's important to note that the machine learning model used to predict income and capital gain tax realizations is differentiated based on the year. Therefore, in this case, we have a total of 10 machine learning models for 10 years."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step5_text1 + step5_text2 + "</h3>",
    unsafe_allow_html=True)
with step6:
    st.markdown("<h3 style='text-align: center;'>Step 6 : Final Model and Evaluation </h3>",
            unsafe_allow_html=True)
    step6_text1 = "In this phase, a machine learning model will be created using the parameters from all countries except Indonesia over a period of 10 years. However, before that, the performance of the machine learning model will be evaluated based on the Mean Absolute Error metric. The detailed workflow for this phase is as follows:"
    step6_text2 = "<br>1. Evaluating the performance of the machine learning model using the test dataset and the Mean Absolute Error metric.<br>2. Building the final machine learning model using data/parameters from all countries except Indonesia.<br>3. Comparing the predicted tax realizations from the machine learning model with the actual conditions over a 10-year period.<br>4. Calculating the performance index over the 10-year period and visualizing it in the form of a graph."
    st.markdown("<p style='text-align: justify; font-size: 16px;'>" + step6_text1 + step6_text2 + "</h3>",
    unsafe_allow_html=True)



st.markdown("<h2 style='text-align: left;'>Income and Capital Gain Tax Factor Dashboard from Tableau</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: justify; font-size: 16px;'><i>This is an interactive dashboard, so feel free to explore</i></p>",
    unsafe_allow_html=True)

st.components.v1.html("""
<div class='tableauPlaceholder' id='viz1686502213137' style='position: relative'><noscript><a href='#'><img alt='Dashboard 1 ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ta&#47;TaxFactorAnalysis&#47;Dashboard1&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='TaxFactorAnalysis&#47;Dashboard1' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ta&#47;TaxFactorAnalysis&#47;Dashboard1&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-US' /></object></div>
<script type='text/javascript'>
var divElement = document.getElementById('viz1686502213137');
var vizElement = divElement.getElementsByTagName('object')[0];
if ( divElement.offsetWidth > 800 ) {{
    vizElement.style.width='100%';
    vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
}} else if ( divElement.offsetWidth > 500 ) {{
    vizElement.style.width='100%';
    vizElement.style.height=(divElement.offsetWidth*0.75)+'px';
}} else {{
    vizElement.style.width='100%';
    vizElement.style.height='2377px';
}}
var scriptElement = document.createElement('script');
scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
vizElement.parentNode.insertBefore(scriptElement, vizElement);
</script>
""", height = 1200)

st.markdown("<h2 style='text-align: left;'>What have we known so far?</h2>", unsafe_allow_html=True)

year_list = [x for x in range(2011,2021)]
indo_pred = []
for i in year_list:
    exec("loaded_model_" + str(i) + " = joblib.load('D:\Latihan Coding\TETRIS CEO BATCH 3\CAPSTONE PROJECT\linearmodel_" + str(i) + ".sav')")
    exec("indo_" + str(i) + " = loaded_model_" + str(i) + ".predict(tax_df[(tax_df['Year'] == " + str(i) + ") & (tax_df['Country'] == 'Indonesia')].drop(tax_df.columns[0:6], axis=1))")
    exec("indo_pred.append(indo_" + str(i) + "[0])")
indo_act = list(tax_df[tax_df['Country'] == 'Indonesia']['% Tax Revenue per GDP'])
indo_tax = pd.DataFrame(
    {'Year': year_list,
     'predicted': indo_pred,
     'actual': indo_act
    })
indo_tax['Year'] = indo_tax['Year'].astype(str)
indo_tax_melt = pd.melt(indo_tax, id_vars=['Year'], value_vars=['predicted','actual']).rename(columns = {'variable':'Condition', 'value':'Tax revenue per GDP (%)'})

correlation_data = tax_df.corr()
correlation_data = correlation_data.stack().reset_index().rename(columns={0: 'correlation', 'level_0':'x_parameters', 'level_1':'y_parameters'})

vis9, vis10 = st.columns([6,4])
with vis9:
    st.markdown(" ")
with vis10:
    st.markdown("<h4 style='text-align: center;'>Correlation Heatmap Chart</h4>", unsafe_allow_html=True) 


vis11, vis12 = st.columns([6,4])
with vis11:
    vis11_text1 = "From the heatmap chart attached on the right side, we can observe the correlation of Tax Revenue per GDP (%) to other parameters. Based on the chart, we can draw the following conclusions:"
    vis11_text2 = "<br>1. CPI Score and GDP per Capita have a strong positive correlation with income and capital gain tax revenue per GDP.<br>2. Labour Force Rate has a moderate positive correlation with income and capital gain tax revenue per GDP.<br>3. Unemployment Rate has a weak positive correlation with income and capital gain tax revenue per GDP.<br>4. Inflation Rate and Population Growth have a weak negative correlation with income and capital gain tax revenue per GDP.<br>5. Population and Foreign Direct Investment have no correlation with income and capital gain tax revenue per GDP."
    st.markdown("<p style='text-align: justify; font-size: 20px;'>" + vis11_text1 + vis11_text2 + "</h3>",
    unsafe_allow_html=True)
with vis12:
    corr_chart = alt.Chart(correlation_data).mark_rect().encode(
    x='x_parameters:N',
    y='y_parameters:N',
    color='correlation:Q'
    ).properties(
        width=400,
        height=400,
        title='Correlation Matrix'
    ).configure_mark(
        text='white'
    ).configure_title(
        fontSize=14
    ).configure_axisX(
        labelAngle=315
    )
    st.altair_chart(corr_chart, use_container_width=True)

vis1, vis2 = st.columns([6,4])
with vis1:
    st.markdown("<h4 style='text-align: center;'>Predicted vs Actual Tax Revenue per GDP (%) from 2011 to 2020</h4>", unsafe_allow_html=True) 
with vis2:
    st.markdown(" ")

vis3, vis4 = st.columns([6,4])
with vis3:
    tax_chart = alt.Chart(indo_tax_melt).mark_line().encode(
        x='Year:O',
        y='Tax revenue per GDP (%):Q',
        color = 'Condition:O',
        tooltip=['Year', 'Tax revenue per GDP (%)']
        ).configure_axisX(
        labelAngle=0
        )
    st.altair_chart(tax_chart, use_container_width=True)
with vis4:
    vis2_text1 = "From the chart on the left, it can be seen that the performance of income tax and value-added tax regulations in Indonesia over the 10-year period from 2011 to 2020 consistently falls short of expectations. This can be observed from the income tax and value-added tax revenue chart, which always remains below the predicted values. This is especially noticeable in the last 4 years, from 2017 to 2020."
    vis2_text2 = " During these 4 years, the decline in tax regulation performance becomes more pronounced each year. To further understand the performance of income tax and value-added tax regulations, a performance index will be calculated as an indicator. The performance index formula is calculated as follows: performance index (%) = (1 - (actual - predicted) / actual) * 100."
    st.markdown("<p style='text-align: justify; font-size: 20px;'>" + vis2_text1 + vis2_text2 + "</h3>",
    unsafe_allow_html=True)
vis5, vis6 = st.columns([4,6])
with vis5:
    st.markdown(" ")
with vis6:
    st.markdown("<h4 style='text-align: center;'>Indonesia's Tax Regulation Performance on Income and Capital Gain Tax from 2011 to 2020 </h4>", unsafe_allow_html=True)

vis7, vis8 = st.columns([4,6])
with vis7:
    vis7_text1 = "From the graph on the right, we can see the performance index of tax regulations in Indonesia regarding income tax and value-added tax from 2011 to 2020. From the graph, we can observe that Indonesia's tax performance from 2011 to 2016 showed relatively high values."
    vis7_text2 = " However, from 2017 to 2020, the performance index gradually declined, especially from 2019 to 2020. This decline is likely attributed to the COVID-19 pandemic that occurred in 2020, which resulted in a decrease in tax performance."
    st.markdown("<p style='text-align: justify; font-size: 20px;'>" + vis7_text1 + vis7_text2 + "</h3>",
    unsafe_allow_html=True)
with vis8:
    performance_index = [(1 - (x - y)/x)*100 for x, y in zip(indo_pred, indo_act)]
    indo_performance = pd.DataFrame(
    {'Year': year_list,
     'Performance Index (%)': performance_index})
    performance_chart = alt.Chart(indo_performance).mark_line().encode(
        x='Year:O',
        y='Performance Index (%):Q',
        tooltip=['Year', 'Performance Index (%)']
        ).configure_axisX(
        labelAngle=0
        )
    st.altair_chart(performance_chart, use_container_width=True)

st.markdown("<h2 style='text-align: left;'>Conclusion and Suggestion</h2>", unsafe_allow_html=True)
con1, con2 = st.columns([6,4])
with con1:
    con1_text1 = "Based on the data processing and analysis results, we have found that the low tax revenue in Indonesia, especially in income and capital gain tax, is not only caused by low compliance rates but also by several factors, including:"
    con1_text2 = "<br>1. High levels of corruption indicated by the low CPI Score in Indonesia, which makes people hesitant to pay taxes.<br>2. Low GDP per Capita, which leads to reduced welfare among the population and indirectly affects their willingness to pay taxes."
    st.markdown("<p style='text-align: justify; font-size: 20px;'>" + con1_text1 + con1_text2 + "</h3>",
    unsafe_allow_html=True)
    st.markdown("<h4 style='text-align: left;'>What can the government do?</h4>", unsafe_allow_html=True)
    con1_text3 = "1. Combat corruption through various measures, such as allocating a higher budget to anti-corruption institutions, reviewing criminal laws related to corruption, etc.<br>2. Focus the budget on Indonesia's economic growth through measures like improving the management of natural resources, maintaining infrastructure, etc.<br>3. Increase labor force participation by creating job opportunities for local workers and reducing the reliance on foreign labor."
    st.markdown("<p style='text-align: justify; font-size: 20px;'>" + con1_text3 + "</h3>",
    unsafe_allow_html=True)
    

