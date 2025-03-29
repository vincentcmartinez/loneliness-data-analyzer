import numpy as np
from user import User
import scipy.stats as stats
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns

matplotlib.use('TkAgg')


class Analyzer:

    def __init__(self, userbase):
        self.userbase = userbase
        self.complete_users = self.filter_nones()
        self.data = self.filter_outliers()
        self.home_times = [user.avg_time_at_home for user in self.data]
        self.loneliness_scores = [user.pre_survey_score for user in self.data]

    def filter_outliers(self) -> list[User]:
        hometimes = [user.avg_time_at_home for user in self.complete_users]
        filtered_keys = self.remove_outliers_iqr(hometimes)
        filtered_users = filter(lambda user: (user.avg_time_at_home in filtered_keys), self.complete_users)
        return list(filtered_users)

    def filter_nones(self) -> list[User]:
        filtered_users = filter(lambda user: user.data_complete(), self.userbase)
        return list(filtered_users)

    def remove_outliers_iqr(self, arr):
        q1 = np.percentile(arr, 25)
        q3 = np.percentile(arr, 75)
        iqr = q3 - q1
        lower_bound = q1 - 1.5 * iqr
        upper_bound = q3 + 1.5 * iqr
        filtered_arr = filter((lambda a: lower_bound <= a <= upper_bound), arr)
        return list(filtered_arr)

    def print_stats(self):
        pearson_corr, pearson_p = stats.pearsonr(self.home_times, self.loneliness_scores)
        slope, intercept, r_value, p_value, std_err = stats.linregress(self.home_times, self.loneliness_scores)

        print("Pearson Correlation:")
        print(f"Correlation: {pearson_corr:.4f}")
        print(f"P-value: {pearson_p:.4f}")

        print("\nLinear Regression:")
        print(f"Slope: {slope:.4f}")
        print(f"R-squared: {r_value ** 2:.4f}")
        print(f"P-value: {p_value:.4f}")

    def show_plots(self):
        plt.figure(figsize=(15, 5))

        plt.subplot(1, 3, 1)
        sns.histplot(self.home_times)
        plt.title('Home Times Distribution')

        plt.subplot(1, 3, 2)
        sns.histplot(self.loneliness_scores)
        plt.title('Loneliness Scores Distribution')

        plt.subplot(1, 3, 3)
        sns.scatterplot(x=self.home_times, y=self.loneliness_scores)
        plt.title('Home Times vs Loneliness Scores')
        plt.xlabel('Home Times')
        plt.ylabel('Loneliness Scores')

        plt.tight_layout()

        plt.savefig("fig.png")
        plt.show()

        _, home_times_p = stats.shapiro(self.home_times)
        _, loneliness_p = stats.shapiro(self.loneliness_scores)
