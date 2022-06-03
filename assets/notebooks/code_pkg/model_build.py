from sklearn import metrics
import itertools
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

def plot_confusion_matrix(cm, classes, normalize=False, title='Confusion matrix', cmap=plt.cm.Blues):
    """
    Function to plot the confusion matrix.
    Normalization can be applied by setting `normalize=True`.
    """
    if normalize:
        cm = cm.astype('float') / cm.sum(axis=1)[:, np.newaxis]
    plt.imshow(cm, interpolation='nearest', cmap=cmap)
    plt.title(title, fontsize=14)
    tick_marks = np.arange(len(classes))
    plt.xticks(tick_marks, classes)
    plt.yticks(tick_marks, classes)
    fmt = '.2f' if normalize else 'd'
    thresh = cm.max() / 2.
    for i, j in itertools.product(range(cm.shape[0]), range(cm.shape[1])):
        plt.text(j, i, format(cm[i, j], fmt),
                 horizontalalignment="center",
                 color="white" if cm[i, j] > thresh else "black")
    plt.ylabel('Actual Label')
    plt.xlabel('Predicted Label')
    plt.tight_layout()

    
def build_models(_X_train, _y_train, _X_test, _y_test):
    from sklearn.linear_model import LogisticRegression
    from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
    # Logistic Regression, Random Forest, and Gradient Boost
    lr_model = LogisticRegression(penalty='l1', solver='saga', tol=0.1).fit(_X_train, _y_train)
    rf_model = RandomForestClassifier(n_estimators=500, max_depth=9, random_state=1234).fit(_X_train, _y_train)
    gb_model = GradientBoostingClassifier(learning_rate=0.01, n_estimators=500, max_depth=12, random_state=1234).fit(_X_train, _y_train)
    
    models = {"Logistic Regression": lr_model,
          "Random Forest": rf_model,
          "Gradient Boosting": gb_model}
    
    fig  = plt.figure(figsize=(20,10))
    plot = 1
    
    for model_type, model in models.items():
        y_pred_test = model.predict(_X_test)
        confusion_matrix = metrics.confusion_matrix(_y_test, y_pred_test, labels=[0,1])
        fig.add_subplot(130+plot)
        plot_confusion_matrix(confusion_matrix, normalize=False, classes=['0','1'], title=model_type+' \n')
        plot += 1
    acc = pd.DataFrame(columns = ['Type', 'accuracy'])
    for model_type, model in models.items():
        acc = acc.append({'Type': model_type, 'accuracy': round(model.score(_X_test, _y_test),4)}, ignore_index=True)

    print("\nModel Test Accuracy : ")
    print(acc)
    return models