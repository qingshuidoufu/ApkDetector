import os

from django.test import TestCase

# Create your tests here.
import django



os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ApkDetector.settings")
django.setup()
from apk.models import ApkJson
from support.interpret_json import get_csv
from support.predict import mechine_analyse

if __name__ == "__main__":

    apk_json = ApkJson.objects.get(hash_value='5cfeb9dabe032761ac0b5e671cc5ebab')

    result = mechine_analyse(apk_json.data)
    print(result)


    # get_csv(apk_json.data)
    #
    # model_path='./classifierModel/knn.joblib'
    # csv_path='./sampleCsv/csvReport.csv'
    # from support.predict import pre_process
    # from support.predict import standarize
    # sample_data = pre_process(csv_path)
    # test=standarize(sample_data)
    # from  joblib import load
    # classifier=load(model_path)
    # predicted=classifier.predict(test)
    # print(predicted[0])

