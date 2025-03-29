# This is a sample Python script.
from analyzer import Analyzer
from gpsloader import GPSLoader
from userfactory import UserFactory
from surveyloader import SurveyLoader
from user import User



def main():
    factory = UserFactory()
    surveyloader = SurveyLoader(factory)
    surveyloader.set_scores("C:\\Users\\Vincent\\Desktop\\data\\survey\\LonelinessScale.csv")
    gpsloader = GPSLoader(factory)
    gpsloader.load_user_data("C:\\Users\\Vincent\\Desktop\\data\\sensing\\gps")
    analyzer = Analyzer(factory)
    analyzer.print_stats()
    analyzer.show_plots()

if __name__ == '__main__':
    main()

