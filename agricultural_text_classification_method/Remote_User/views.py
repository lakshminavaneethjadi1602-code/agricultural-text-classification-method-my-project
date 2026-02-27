from django.db.models import Count
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import VotingClassifier
# Create your views here.

from Remote_User.models import ClientRegister_Model,agriculture_text_classification,detection_ratio,detection_accuracy

def login(request):


    if request.method == "POST" and 'submit1' in request.POST:

        username = request.POST.get('username')
        password = request.POST.get('password')
        try:
            enter = ClientRegister_Model.objects.get(username=username,password=password)
            request.session["userid"] = enter.id

            return redirect('ViewYourProfile')
        except:
            pass

    return render(request,'RUser/login.html')
def index(request):
    return render(request, 'RUser/index.html')

def Register1(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phoneno = request.POST.get('phoneno')
        country = request.POST.get('country')
        state = request.POST.get('state')
        city = request.POST.get('city')
        address = request.POST.get('address')
        gender = request.POST.get('gender')
        ClientRegister_Model.objects.create(username=username, email=email, password=password, phoneno=phoneno,
                                            country=country, state=state, city=city, address=address, gender=gender)
        obj = "Registered Successfully"
        return render(request, 'RUser/Register1.html', {'object': obj})
    else:
        return render(request,'RUser/Register1.html')

def ViewYourProfile(request):
    userid = request.session['userid']
    obj = ClientRegister_Model.objects.get(id= userid)
    return render(request,'RUser/ViewYourProfile.html',{'object':obj})


def predict_text_classification(request):

    if request.method == "POST":

        Fid = request.POST.get('Fid')
        State_Name = request.POST.get('State_Name')
        District_Name = request.POST.get('District_Name')
        Crop_Year = request.POST.get('Crop_Year')
        Season = request.POST.get('Season')
        Area = request.POST.get('Area')
        Production = request.POST.get('Production')

        df = pd.read_csv('Datasets.csv', encoding='latin-1')
        df
        df.columns

        def apply_response(Label):
            if (Label != "Wheat"):
                return 0  # Others
            elif (Label == "Wheat"):
                return 1  # Wheat

        df['results'] = df['Crop'].apply(apply_response)

        X = df['Fid']
        y = df['results']

        print("Fid")
        print(X)
        print("Results")
        print(y)

        cv = CountVectorizer(lowercase=False, strip_accents='unicode', ngram_range=(1, 1))
        #X = cv.fit_transform(df['ipaddress'].apply(lambda x: np.str_(X)))

        X = cv.fit_transform(X)

        models = []
        from sklearn.model_selection import train_test_split
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.20)
        X_train.shape, X_test.shape, y_train.shape

        print("Multi scale convolution kernel convolutional neural network--Mul-CNN")
        from sklearn.neural_network import MLPClassifier
        mlpc = MLPClassifier().fit(X_train, y_train)
        y_pred = mlpc.predict(X_test)
        testscore_mlpc = accuracy_score(y_test, y_pred)
        accuracy_score(y_test, y_pred)
        print(accuracy_score(y_test, y_pred))
        print(accuracy_score(y_test, y_pred) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, y_pred))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, y_pred))
        models.append(('Mul CNN', mlpc))

        print("Gradient Boosting Classifier")

        from sklearn.ensemble import GradientBoostingClassifier
        clf = GradientBoostingClassifier(n_estimators=100, learning_rate=1.0, max_depth=1, random_state=0).fit(
            X_train,
            y_train)
        clfpredict = clf.predict(X_test)
        print("ACCURACY")
        print(accuracy_score(y_test, clfpredict) * 100)
        print("CLASSIFICATION REPORT")
        print(classification_report(y_test, clfpredict))
        print("CONFUSION MATRIX")
        print(confusion_matrix(y_test, clfpredict))
        models.append(('GradientBoostingClassifier', clf))

        classifier = VotingClassifier(models)
        classifier.fit(X_train, y_train)
        y_pred = classifier.predict(X_test)

        Fid1 = [Fid]
        vector1 = cv.transform(Fid1).toarray()
        predict_text = classifier.predict(vector1)

        pred = str(predict_text).replace("[", "")
        pred1 = pred.replace("]", "")

        prediction = int(pred1)

        if (prediction == 0):
            val = 'Others'
        elif (prediction == 1):
            val = 'Wheat'

        print(val)
        print(pred1)

        agriculture_text_classification.objects.create(
            Fid=Fid,
            State_Name=State_Name,
            District_Name=District_Name,
            Crop_Year=Crop_Year,
            Season=Season,
            Area=Area,
            Production=Production,
            Prediction=val)

        return render(request, 'RUser/predict_text_classification.html',{'objs': val})
    return render(request, 'RUser/predict_text_classification.html')



