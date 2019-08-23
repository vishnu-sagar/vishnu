import pandas as pd
import os
from sklearn import preprocessing,ensemble,model_selection,tree,neighbors
import seaborn as sns
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm, gridspec
from matplotlib.colors import ListedColormap
from sklearn import decomposition, tree,ensemble,svm,neighbors
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
import xgboost as xgb
import sys
import os
path = os.path.abspath(os.path.join('.'))
sys.path.append(path)
path = 'Documents'
sys.path.append(path)
from common_utils import *
from common_utils  import *
def get_continuous_features(df):
    return df.select_dtypes(include=['number']).columns

def get_categorical_features(df):
    return df.select_dtypes(exclude=['number']).columns

def cast_cont_to_cat(df, features):
    for feature in features:
        df[feature] = df[feature].astype('category')


def plot_data_2d(X, y, labels=['X1', 'X2']):
    colors = ['red','green','purple','blue']
    plt.scatter(X[:,0], X[:,1], c=y, cmap=ListedColormap(colors), s=30)
    plt.xlabel(labels[0])
    plt.ylabel(labels[1])
    
def plot_data_3d(X, y, labels=['X1', 'X2','X3']):
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    colors = ['red','green','purple','blue']
    ax.scatter(X[:,0], X[:,1], X[:,2], c = y, cmap=ListedColormap(colors), s=30)
    ax.set_xlabel(labels[0])
    ax.set_ylabel(labels[1])
    ax.set_zlabel(labels[2])
pd.get_dummies


dir="D:\ML"
train=pd.read_csv(os.path.join(dir,"card.csv"))
master_train=pd.read_csv(os.path.join(dir,"card.csv"))
print(train.info())
print(train.columns)
y_train=master_train["Y"]

train=train.drop(["ID","Y",'X6', 'X7', 'X8', 'X9', 'X10', 'X11'],axis=1)

##################################################
get_categorical_features(train)
get_continuous_features(train)

features=['X2', 'X3', 'X4']
cast_cont_to_cat(train,features)

print(get_categorical_features(train))
print(get_continuous_features(train))

cat_features=get_categorical_features(train)
cont_features=get_continuous_features(train)
#ohe########################
ohe = preprocessing.OneHotEncoder()
ohe.fit(train[cat_features])
print(ohe.n_values_)
tmp1 = ohe.transform(train[cat_features]).toarray()
tmp1 = pd.DataFrame(tmp1)


tmp2 = train[cont_features]

tmp = pd.concat([tmp1, tmp2], axis=1)
################################################
X_train=ohe(train,cat_features)########ohe by get_dummies
names=X_train.columns
#######################################
scaler1 = preprocessing.StandardScaler()
X_train1 = pd.DataFrame(scaler1.fit_transform(X_train),columns=names)

scaler2=preprocessing.MinMaxScaler()
X_train2 = pd.DataFrame(scaler2.fit_transform(X_train),columns=names)

scaler3=preprocessing.RobustScaler()
X_train3 = pd.DataFrame(scaler3.fit_transform(X_train),columns=names)
sns.kdeplot(X_train["X1"])
sns.kdeplot(X_train1["X1"])
sns.kdeplot(X_train2["X1"])
sns.kdeplot(X_train3["X1"])
####################
#feature selection
#feature selection via RF
feature_selector = ensemble.RandomForestClassifier()
feature_selector.fit(X_train1, y_train)
print(feature_selector.feature_importances_)
plot_feature_importances(feature_selector, X_train1, cutoff=80)

tmp_model1 = feature_selection.SelectFromModel(feature_selector, threshold="median", prefit=True)
selected_features = X_train1.columns[tmp_model1.get_support()]

X_trainRF = pd.DataFrame(tmp_model1.transform(X_train1),columns=selected_features)

#####################
feature_selector = ensemble.RandomForestClassifier()
#recursive feature selection 
tmp_model = feature_selection.RFE(feature_selector, 10, 2)
print(tmp_model.decision_functio
#########################
lpca = decomposition.PCA(2)
pca_data2 = lpca.fit_transform(X_train)
print(np.cumsum(lpca.explained_variance_ratio_))
plot_data_2d(pca_data2, y_train, ['PC1', 'PC2'])
pca_data2=pd.DataFrame(pca_data2)

lpca = decomposition.PCA(3)
pca_data3 = lpca.fit_transform(X_train)
print(lpca.explained_variance_ratio_)
print(np.cumsum(lpca.explained_variance_ratio_))
plot_data_3d(pca_data3, y_train, ['PC1', 'PC2', 'PC3'])
pca_data3=pd.DataFrame(pca_data3)
###################################################


rf_estimator = ensemble.RandomForestClassifier()
rf_grid = {'n_estimators':[10, 50, 100, 200], 'max_depth':[3,4,5,6,7], 'max_features':[2,3,4] }
rf_grid_estimator = model_selection.GridSearchCV(rf_estimator, rf_grid, cv=10, return_train_score=True)
rf_grid_estimator.fit(X_trainRF, y_train)

print(rf_grid_estimator.best_score_)
print(rf_grid_estimator.best_params_)
final_estimator = rf_grid_estimator.best_estimator_
final_estimator.score(X_trainRF, y_train)
print(final_estimator.estimators_)


xgb_estimator = xgb.XGBClassifier(random_state=100, n_jobs=-1)
xgb_grid = {'n_estimators':list(range(50,101,50)), 'learning_rate':[0.1,0.2,1.0], 'max_depth':[1,3,5], 'gamma':[0,0.01,0.1,0.2], 'reg_alpha':[0,0.5,1], 'reg_lambda':[0,0.5,1]}
xgb_grid_estimator = model_selection.GridSearchCV(xgb_estimator, xgb_grid, scoring='accuracy', cv=10, return_train_score=True)
xgb_grid_estimator.fit(train, y_train)

print(xgb_grid_estimator.best_score_)
print(xgb_grid_estimator.best_params_)
final_estimator = xgb_grid_estimator.best_estimator_
print(final_estimator.score(train, y_train))

#linear svm###########################
lsvm_estimator = svm.LinearSVC(random_state=100)
lsvm_grid = {'C':[0.1,0.2,0.5,1] }
grid_lsvm_estimator = model_selection.GridSearchCV(lsvm_estimator, lsvm_grid, cv=10)
grid_lsvm_estimator.fit(X_trainRF, y_train)
print(grid_lsvm_estimator.best_params_)
final_estimator = grid_lsvm_estimator.best_estimator_
print(final_estimator.coef_)
print(final_estimator.intercept_)
print(grid_lsvm_estimator.best_score_)
print(final_estimator.score(X_trainRF, y_train))
#################################################
knn_estimator = neighbors.KNeighborsClassifier()
knn_grid = {'n_neighbors':[5,7,8,10,20], 'weights':['uniform','distance']}
knn_grid_estimator = model_selection.GridSearchCV(knn_estimator, knn_grid, cv=10, return_train_score=True)
knn_grid_estimator.fit(X_trainRF, y_train)

print(knn_grid_estimator.best_score_)
print(knn_grid_estimator.best_params_)
results = knn_grid_estimator.cv_results_
final_estimator = knn_grid_estimator.best_estimator_

results.get("mean_test_score")
results.get("mean_train_score")
results.get('params')
#########################################################################
scoring = 'accuracy'
dt_estimator = tree.DecisionTreeClassifier()
ada_estimator = ensemble.AdaBoostClassifier(base_estimator=dt_estimator)
ada_grid = {'n_estimators':[100], 'base_estimator__max_depth':list(range(1,4)), 'learning_rate':[0.1,0.5]}
grid_search_plot_models_classification(ada_estimator, ada_grid, pca_data2, y_train)
grid_search_plot_two_parameter_curves(ada_estimator, ada_grid, pca_data2, y_train, scoring =  scoring)
ada_final_model = grid_search_best_model(ada_estimator, ada_grid, pca_data2, y_train, scoring = scoring )
plot_model_2d_classification(ada_final_model, pca_data2, y_train)
performance_metrics_hard_binary_classification(ada_final_model, X_test, y_test)
#################################################
rf_estimator = ensemble.RandomForestClassifier()
rf_grid = {'n_estimators':list(range(10,100,40)), 'max_depth':list(range(3,6))}
grid_search_plot_models_classification(rf_estimator, rf_grid, pca_data2, y_train)
grid_search_plot_two_parameter_curves(rf_estimator, rf_grid, pca_data2, y_train, scoring =  scoring)
rf_final_model = grid_search_best_model(rf_estimator, rf_grid, pca_data2, y_train, scoring = scoring )
plot_model_2d_classification(rf_final_model,pca_data2, y_train)
performance_metrics_hard_binary_classification(rf_final_model, X_test, y_test)
#_________________________________________________________________

size =50

#create a dataframe with only 'size' features
data=X_train1.iloc[:,:size] 

#get the names of all the columns
cols=data.columns 

# Calculates pearson co-efficient for all combinations
data_corr = data.corr()

# Set the threshold to select only only highly correlated attributes
threshold = 0.5

# List of pairs along with correlation above threshold
corr_list = []

#Search for the highly correlated pairs
for i in range(0,size): #for 'size' features
    for j in range(i+1,size): #avoid repetition
        if (data_corr.iloc[i,j] >= threshold and data_corr.iloc[i,j] < 1) or (data_corr.iloc[i,j] < 0 and data_corr.iloc[i,j] <= -threshold):
            corr_list.append([data_corr.iloc[i,j],i,j]) #store correlation and columns index

#Sort to show higher ones first            
s_corr_list = sorted(corr_list,key=lambda x: -abs(x[0]))

#Print correlations and column names
for v,i,j in s_corr_list:
    print ("%s and %s = %.2f" % (cols[i],cols[j],v))
      
      
 import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
%matplotlib inline
dir=r"D:\Users\sagarv\Documents\loan"
#os.chdir(r'C:\Users\prana\Desktop')
df = pd.read_csv(os.path.join(dir,"train.csv"))
df_test = pd.read_csv(os.path.join(dir,"test.csv"))
df.head()

pd.options.display.max_seq_items = 4000

df_test1 = pd.read_csv(os.path.join(dir,"test.csv"))


def get_continuous_features(df):
    return df.select_dtypes(include=['number']).columns

def get_categorical_features(df):
    return df.select_dtypes(exclude=['number']).columns

def cast_cont_to_cat(df, features):
    for feature in features:
        df[feature] = df[feature].astype('category')
        
        
        
cat_features=get_categorical_features(df)
cont_features=get_continuous_features(df)
print(cat_features)
print(cont_features)


from sklearn import preprocessing
for col in df[cat_features]:
    le_all=preprocessing.LabelEncoder()
    le_all.fit(df[col])
    print(le_all.classes_)
    df[col]=le_all.transform(df[col])
    
    
df_test=df_test.replace(['Apr-12','Feb-12','Mar-12','May-12'],['04/2012','02/2012','03/2012','05/2012'])

df_test=df_test.replace(['01/01/12','01/02/12','01/03/12'],['2012-01-01','2012-02-01','2012-03-01'])


for col in df_test[cat_features]:
    le_all=preprocessing.LabelEncoder()
    le_all.fit(df_test[col])
    print(le_all.classes_)
    df_test[col]=le_all.transform(df_test[col])

df_train=df
    
import numpy as np
df_train['loan_to_value_log'] = np.log(df_train['loan_to_value'])
df_test['loan_to_value_log'] = np.log(df_test['loan_to_value'])
df_train['loan_to_value_log'].hist(bins=25)

df_train['unpaid_principal_bal_log'] = np.log(df_train['unpaid_principal_bal'])
df_test['unpaid_principal_bal_log'] = np.log(df_test['unpaid_principal_bal'])
df_train['unpaid_principal_bal_log'].hist(bins=25)


df_train=df_train.drop(['loan_id','unpaid_principal_bal','loan_to_value'], axis=1)
#df_train=df_train.drop('Loan_ID',axis=1) 
df_test=df_test.drop(['loan_id','unpaid_principal_bal','loan_to_value'],axis=1)
#df_train = df_train.drop('LoanAmount',axis=1)
#df_test = df_test.drop('LoanAmount',axis=1)
X = df_train 
y = df_train.m13
X=pd.get_dummies(X,columns=cat_features)


df_train=pd.get_dummies(df_train,columns=cat_features) 
df_test=pd.get_dummies(df_test,columns=cat_features)


df_train=df_train.drop(['number_of_borrowers'], axis=1) 
df_test=df_test.drop(['number_of_borrowers'], axis=1)



from sklearn.linear_model import LogisticRegression
#import xgboost as xgb
from sklearn import ensemble,tree
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score,confusion_matrix,f1_score,precision_score,recall_score
features=['m7', 'm8', 'm9', 'm10', 'm11', 'm12','borrower_credit_score']
X = df_train[features]
y=df_train.m13
i=1 
kf = StratifiedKFold(n_splits=5,random_state=1,shuffle=True) 
for train_index,test_index in kf.split(X,y):     
    print('\n{} of kfold {}'.format(i,kf.n_splits))    
    xtr,xvl = X.loc[train_index],X.loc[test_index]     
    ytr,yvl = y[train_index],y[test_index]         
    #dt_estimator = ensemble.GradientBoostingClassifier(learning_rate=1,n_estimators=300,random_state=100)
    model2 = ensemble.GradientBoostingClassifier(learning_rate=1,n_estimators=400,random_state=100,max_depth=3,max_features=6)
    model2.fit(xtr, ytr)     
    pred_test1 = model2.predict(xvl)    
    score = accuracy_score(yvl,pred_test1)
    matrix=confusion_matrix(yvl,pred_test1)
    f1=f1_score(yvl,pred_test1)
    p=precision_score(yvl,pred_test1)
    r=recall_score(yvl,pred_test1)
    print('accuracy_score',score)
    print('matrix',matrix)
    print('f1',f1)
    print('pres',p)
    print('rec',r)
    i+=1
  
    
importances=pd.Series(model2.feature_importances_, index=X.columns) 
importances.plot(kind='barh', figsize=(12,8))
    
df_test=df_test[features]
pred_test1 = model2.predict(df_test)


np.bincount(pred_test1)

df_test1['m13']=pred_test1
df_test1.to_csv(os.path.join(dir,'submission.csv'), columns=['loan_id','m13'], index=False)
