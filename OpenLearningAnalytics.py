
# coding: utf-8

# <h2> Open University Learning Analytics </h2>
# <h3> Task: Visualising factors associated with the completion of an OU module 
# <h3>  Platform: Jupyter Python Notebook </h3>

# <h3>1. Loading data and data inspection</h3>

# In[93]:

import pandas as pd
import math
import numpy as np
import matplotlib.pyplot as plt

df_studentReg = pd.read_csv("studentRegistration.csv")
df_studentReg.head()
len(df_studentReg)


# In[94]:

df_studentInfo = pd.read_csv("studentInfo.csv")
len(df_studentInfo)


# In[95]:

df_studentAssessment = pd.read_csv("studentAssessment.csv")
len(df_studentAssessment)


# In[96]:

print(df_studentAssessment.columns)
len(df_studentAssessment.groupby(['id_student']))


# In[97]:

df_studentVle = pd.read_csv("studentVle.csv")
df_studentVle.columns
len(df_studentVle)


# In[98]:

df_assessment = pd.read_csv("assessments.csv")
df_vle = pd.read_csv("vle.csv")
df_course = pd.read_csv("courses.csv")
df_course.head()
len(df_course)


# In[99]:

df_course.groupby(['code_module','code_presentation'])['code_presentation'].count()


# <h3>2. Checking data integrity</h3>

# In[100]:

df_studentInfo.groupby(['code_module','code_presentation'])['id_student'].count()


# In[101]:

df_studentReg.groupby(['code_module','code_presentation'])['id_student'].count()


# In[102]:

df_studentVle.groupby(['code_module','code_presentation','id_student'])['id_student'].count()[0:25]


# <h3> 3. Join Data Tables </h3>

# <h4>3.1 Join Table "StudentInfo" and "StudentRegistration" by "code_module", "code_presentation", "id_student" </h4>
# <p> Observation: each module have 2-4 code presentations, module CCC 2014J has the highest # of students registered</p>

# In[103]:

df_mergedInfoReg = pd.merge(df_studentInfo, df_studentReg, how="left", left_on=['code_module', 'code_presentation','id_student'],
                            right_on=['code_module', 'code_presentation','id_student'])
df_mergedInfoReg.head()


# In[104]:

mergedCount=df_mergedInfoReg.groupby(['code_module','code_presentation'])
mergedCount['id_student'].count()


# In[105]:

get_ipython().magic('matplotlib inline')
mergedCount['id_student'].size().plot.barh(title='# of students registered for each module',figsize=[10,10], grid=True,color="lightblue")


#  <h4>3.2 Join Table "StudentAssessment" and "Assessment" </h4>
#  <p> Observation: each module / presentation involves multiple assessments, most assessments DO NOT have 100% turn in rate. Module DDD has the most # of assessments 14, Module EEE has the least # of assessments 4 </p>

# In[106]:

get_ipython().magic('matplotlib inline')
df_mergedStuAss = pd.merge(df_studentAssessment, df_assessment, how="left", left_on=['id_assessment'],
                            right_on=['id_assessment'])
df_mergedStuAss.groupby(['code_module','code_presentation'] ).id_assessment.nunique().plot.barh(
    title='# of assessments for each module', figsize=[8,8], grid=True,color="lightblue")


# In[107]:

ass_count = df_mergedStuAss.groupby(['code_module','code_presentation','id_assessment']).id_assessment.count()
stu_count = df_mergedInfoReg.groupby(['code_module','code_presentation']).id_student.count()

ass_count[0:5]/stu_count[0]


# <h4> 3.3* Merge Table "studentVle" into the merged data frame on studentInfoReg </h4>
# <p> Observation: For each module, most student has multiple interactions with the VLE. Module FFF has the most # of average clicks. Module DDD has the least # of average clicks </p>

# In[108]:

df_mergedInfoRegVle = pd.merge(df_mergedInfoReg, df_studentVle, 
                               how="left", left_on=['code_module','code_presentation', "id_student"],
                               right_on=['code_module', 'code_presentation',"id_student"])
df_mergedInfoRegVle.head()


# In[109]:

print(df_mergedInfoRegVle.groupby(['code_module','code_presentation','id_student']).id_student.count()[0:10])
df_mergedInfoRegVle.groupby(['code_module','code_presentation']
                           )['sum_click'].mean().plot.barh(
    title='average # of clicks for each module presentation', figsize=[10,10], grid=True,color="lightblue")


# <h3> 4. Adding the attribute "completion" to the merged data frame</h3>

# In[110]:

df_mergedInfoReg['completion'] = np.isnan(df_mergedInfoReg['date_unregistration'])
df_mergedInfoReg.head()


# <h3>5. Select one particular code_module and code_presentation</h3>
# 

# In[111]:

get_ipython().magic('matplotlib inline')
fig, axs = plt.subplots(2,2, figsize=[20,20])
mergedCount['id_student'].size().plot.barh(title='# of students registered for each module', grid=True,color="green",ax=axs[0,0])
df_mergedStuAss.groupby(['code_module','code_presentation'] ).id_assessment.nunique().plot.barh(title='# of assessments for each module',  grid=True,color="green",ax=axs[0,1])
df_mergedInfoRegVle.groupby(['code_module','code_presentation'] )['sum_click'].mean().plot.barh(title='average # of clicks for each module presentation', grid=True,color="green",ax=axs[1,0])

Module = 'FFF'
presentation = '2013J'

AGp=df_mergedInfoReg.groupby(['code_module']).get_group(Module)
AGp_all = AGp.groupby(['code_presentation'])
AGp_all.get_group(presentation).groupby('completion').size().plot.pie(title="Module "+Module+"-"+presentation,ax=axs[1,1],autopct='%1.1f%%',
        shadow=True,fontsize=15)


# In[112]:

AGp_pr = AGp_all.get_group(presentation)
AGp_pr.head()


# In[113]:

# #saving to file
# AGp_pr.to_csv('Module_presentation.csv')


# <h3>6. Visualising variable association -- mosaic plot </h3>

# In[114]:

get_ipython().magic('matplotlib inline')
from statsmodels.graphics.mosaicplot import mosaic
fig, axs = plt.subplots(4,2, figsize=[16,32])
[f,d]=mosaic(AGp_pr, ['completion','disability'],statistic=False, gap=0.02, title="disability vs completion",ax=axs[0,0])
[f,d]=mosaic(AGp_pr, ['completion','gender'],statistic=False, gap=0.02, title="gender vs completion" ,ax=axs[0,1])
[f,d]=mosaic(AGp_pr, ['completion','age_band'],statistic=False, gap=0.02, title="age vs completion",ax=axs[1,0])
[f,d]=mosaic(AGp_pr, ['completion','imd_band'],statistic=False, gap=0.02, title="imd_band vs completion",ax=axs[1,1])
[f,d]=mosaic(AGp_pr, ['completion','final_result'],statistic=False, gap=0.02, title="final_result vs completion",ax=axs[2,1])
[f,d]=mosaic(AGp_pr, ['completion','region'],statistic=False, gap=0.02, title="region vs completion",ax=axs[2,0])
[f,d]=mosaic(AGp_pr, ['completion','highest_education'],statistic=False, gap=0.02, title="highest_education vs completion",ax=axs[3,0])
[f,d]=mosaic(AGp_pr, ['completion','num_of_prev_attempts'],statistic=False, gap=0.02, title="previous attempts vs completion",ax=axs[3,1])


# <h3>7. Calculating categorical variable pair-wise correlation </h3>

# In[115]:

from sklearn.preprocessing import LabelEncoder
lb_make = LabelEncoder()
SelectedDF = AGp_pr[['completion','num_of_prev_attempts','gender','highest_education','age_band','disability','final_result','imd_band','region']]
SelectedDF_code = pd.DataFrame(data=SelectedDF)
SelectedDF_code["gender"] = lb_make.fit_transform(SelectedDF["gender"])
SelectedDF_code["highest_education"] = lb_make.fit_transform(SelectedDF["highest_education"])
SelectedDF_code["age_band"] = lb_make.fit_transform(SelectedDF["age_band"])
SelectedDF_code["disability"] = lb_make.fit_transform(SelectedDF["disability"])
SelectedDF_code["final_result"] = lb_make.fit_transform(SelectedDF["final_result"])
SelectedDF_code["imd_band"] = lb_make.fit_transform(SelectedDF["imd_band"])
SelectedDF_code["region"] = lb_make.fit_transform(SelectedDF["region"])
SelectedDF_code["completion"] = lb_make.fit_transform(SelectedDF["completion"])
SelectedDF_code["index"] = SelectedDF_code.index
correlation = dict()
correlation["disability"] = SelectedDF_code["disability"].corr(SelectedDF_code["completion"],method="pearson")
correlation['gender'] = SelectedDF_code["gender"].corr(SelectedDF_code["completion"],method="pearson")
correlation['age_band'] = SelectedDF_code["age_band"].corr(SelectedDF_code["completion"],method="pearson")
correlation['imd_band']= SelectedDF_code["imd_band"].corr(SelectedDF_code["completion"],method="pearson")
correlation['final_result']= SelectedDF_code["final_result"].corr(SelectedDF_code["completion"],method="pearson")
correlation['region']= SelectedDF_code["region"].corr(SelectedDF_code["completion"],method="pearson")
correlation['highest_education']= SelectedDF_code["highest_education"].corr(SelectedDF_code["completion"],method="pearson")
correlation['previous_attempts']= SelectedDF_code["num_of_prev_attempts"].corr(SelectedDF_code["completion"],method="pearson")
print(correlation)
fig = plt.figure(figsize=[20,8])
plt.bar(range(len(correlation)), correlation.values(), align='center')
a=plt.xticks(range(len(correlation)), correlation.keys())
plt.grid()

