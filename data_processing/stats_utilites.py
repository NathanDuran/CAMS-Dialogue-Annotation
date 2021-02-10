import pandas as pd
import numpy as np
from scipy.stats import entropy as H
from scipy.stats import ttest_ind, chi2, chi2_contingency
import statsmodels.api as sm
from statsmodels.formula.api import ols
from statsmodels.stats.multicomp import MultiComparison
from statsmodels.stats.power import TTestIndPower, FTestAnovaPower
from statsmodels.stats.oneway import effectsize_oneway
from math import sqrt
from statistics import variance, mean


def cohen_d(data_a, data_b):
    """"Cohens d effect size, for calculating the difference between the mean value of groups.

    Args:
        data_a (list): One group of samples.
        data_b (list): One group of samples.

    Returns:
        cohens_d (float): Cohens d effect size.
    """
    # Calculate the size of samples
    n1, n2 = len(data_a), len(data_b)

    # Calculate the variance of the samples
    s1, s2 = np.var(data_a, ddof=1), np.var(data_b, ddof=1)

    # Calculate the pooled standard deviation
    s = sqrt(((n1 - 1) * s1 + (n2 - 1) * s2) / (n1 + n2 - 2))

    # Calculate the means of the samples
    u1, u2 = np.mean(data_a), np.mean(data_b)

    # Calculate the effect size
    return (u1 - u2) / s


def t_test_power_analysis(data_a, data_b, alpha=0.05, power=0.8):
    """Performs statistical power analysis for t-test.
    First calculates cohens d effect size,
    then calculates an expected number of samples for given power, and the actual power given the actual sample size.

    Args:
        data_a (list): One group of samples.
        data_b (list): One group of samples.
        alpha (float): Significance level.
        power (float): Desired statistical power for calculating the expected num samples.

    Returns:
        cohens_d (float): Cohens d effect size.
        exp_n_samples (float): The expected number of samples given desired power, effect size and alpha.
        act_power (float): The actual power given the actual n_samples, effect size and alpha.
    """
    # Parameters for power analysis
    effect = cohen_d(data_a, data_b)  # Cohens d effect size
    n_samples = len(data_a)

    # perform power analysis
    analysis = TTestIndPower()
    exp_n_samples = analysis.solve_power(effect_size=effect, power=power, ratio=1.0, alpha=alpha)
    # print('Expected Sample Size: %.3f' % exp_n_samples)

    act_power = analysis.solve_power(effect_size=effect, nobs1=n_samples, ratio=1.0, alpha=alpha)
    # print('Actual Power: %.3f' % act_power)
    return effect, exp_n_samples, act_power


def t_test(data, groups, metric):
    """T-test for two experiment groups

    Args:
        data (Dataframe): Dataframe grouped by dialogue group and label_type values.
        groups (string): Indicates which column has the primary groups to compare.
        metric (string): Indicates which column name has the result values i.e. values/times.

    Returns:
        t_test_frame (Dataframe): Columns are t-statistic and p-value

                 t-statistic   p-value
        0          2.598956  0.011838
    """
    # Get the list of models and ranges of experiment
    group_names = data[groups].unique()
    if len(group_names) != 2:
        raise ValueError("Too many groups in groups column! Found " + str(len(group_names)) + " but should == 2.")

    # Select the data to compare
    data_a = data.loc[(data[groups] == group_names[0])]
    data_b = data.loc[(data[groups] == group_names[1])]

    # Perform power analysis
    effect, exp_n, act_power = t_test_power_analysis(data_a[metric], data_b[metric], alpha=0.05, power=0.8)

    # T-test
    t_and_p = ttest_ind(data_a[metric], data_b[metric])

    # Create dataframe
    t_test_frame = pd.DataFrame({'t-statistic': t_and_p[0], 'p-value': t_and_p[1], 'cohen-d': effect,
                                 'n': len(data_a), 'exp_n': exp_n, 'power': act_power, 'exp_power': 0.8}, index=[0])

    return t_test_frame


def multi_t_test(data, groups, experiment_type, metric):
    """Multi t-test for each consecutive experiment value between two groups.

    Args:
        data (Dataframe): Dataframe grouped by dialogue group and label_type values.
        groups (string): Indicates which column has the primary groups to compare.
        experiment_type (string): Indicates which columns values to group data for comparison i.e. label_type.
        metric (string): Indicates which column name has the result values i.e. values/times.

    Returns:
        t_test_frame (Dataframe): Columns are t-statistic and p-value, rows are experiment_type.

                 t-statistic   p-value
        ap          2.598956  0.011838
        ap type     4.196354  0.000094
        da          2.777065  0.007375
    """
    # Get the list of groups and ranges of experiment
    group_names = data[groups].unique()
    if len(group_names) != 2:
        raise ValueError("Too many groups in groups column! Found " + str(len(group_names)) + " but should == 2.")

    experiment_values = data[experiment_type].unique()

    results_dict = dict()
    for exp_type in experiment_values:
        # Select the data to compare
        data_a = data.loc[(data[groups] == group_names[0]) & (data[experiment_type] == exp_type)]
        data_b = data.loc[(data[groups] == group_names[1]) & (data[experiment_type] == exp_type)]

        # Perform power analysis
        effect, exp_n, act_power = t_test_power_analysis(data_a[metric], data_b[metric], alpha=0.05, power=0.8)

        # T-test
        t_and_p = ttest_ind(data_a[metric], data_b[metric])

        results_dict[exp_type] = {'t-statistic': t_and_p[0], 'p-value': t_and_p[1], 'cohen-d': effect,
                                  'n': len(data_a), 'exp_n': exp_n, 'power': act_power, 'exp_power': 0.8}

    # Create dataframe
    t_test_frame = pd.DataFrame.from_dict(results_dict, orient='index').reindex(results_dict.keys())

    return t_test_frame


def coehen_f(data, groups, metric):
    """"Cohens f, for calculating the effect size for anova power analysis.

    Args:
        data (DataFrame): DataFrame with columns 'groups' and 'metric'.
        groups (str): Name of the groups column in the data, i.e. the groups for the anova test.
        metric (str): Name of the metric column in the data, i.e. the dependant variable.

    Returns:
        cohens_f (float): Cohens f effect size.
    """
    # Get the means and variance of the data
    means = data.groupby([groups], sort=False).apply(lambda x: mean(x[metric])).to_list()
    variances = data.groupby([groups], sort=False).apply(lambda x: variance(x[metric])).to_list()

    # Calculate effect size
    cohens_f = effectsize_oneway(means, variances, len(data), use_var='equal')
    return cohens_f


def anova_power_analysis(data, groups, metric, alpha=0.05, power=0.8):
    """Performs statistical power analysis for t-test.
    First calculates cohens d effect size,
    then calculates an expected number of samples for given power, and the actual power given the actual sample size.

    Args:
        data (DataFrame): DataFrame with columns 'groups' and 'metric'.
        groups (str): Name of the groups column in the data, i.e. the groups for the anova test.
        metric (str): Name of the metric column in the data, i.e. the dependant variable.
        alpha (float): Significance level.
        power (float): Desired statistical power for calculating the expected num samples.

    Returns:
        cohens_f (float): Cohens f effect size.
        exp_n_samples (float): The expected number of samples given desired power, effect size and alpha.
        act_power (float): The actual power given the actual n_samples, effect size and alpha.
    """
    # Calculate Cohen's f effect size
    effect = coehen_f(data, groups, metric)

    # Number of samples
    n_samples = len(data)
    n_groups = len(data[groups].unique())

    # Expected num samples
    exp_n_samples = FTestAnovaPower().solve_power(effect_size=sqrt(effect), alpha=alpha, power=power, k_groups=n_groups)
    # print('Expected Sample Size: %.3f' % exp_n_samples)
    act_power = FTestAnovaPower().solve_power(effect_size=sqrt(effect), nobs=n_samples, alpha=alpha, k_groups=n_groups)
    # print('Actual Power: %.3f' % act_power)

    return effect, exp_n_samples, act_power


def anova_test(data, groups, metric):
    """ANOVA test with statsmodels.

    Eta-squared and omega-squared share the same suggested ranges for effect size classification:
    Low (0.01 – 0.059)
    Medium (0.06 – 0.139)
    Large (0.14+)
    Omega is considered a better measure of effect size than eta because it is unbiased in it’s calculation.

    Args:
        data (Dataframe): Dataframe grouped by dialogue group and label_type values.
        groups (string): Indicates which columns values to group data for comparison i.e. label_type.
        metric (string): Indicates which column name has the result values i.e. values/times.

    Returns:
        anova_frame (Dataframe): Contains f-statistic, p-value and eta/omega effect sizes.

                           sum_sq     df   mean_sq         F    PR(>F)    eta_sq  omega_sq
        C(label_type)    1.411111    2.0  0.705556  0.605495  0.546931  0.006795 -0.004403
        Residual       206.250000  177.0  1.165254       NaN       NaN       NaN       NaN
    """
    def _anova_table(aov_data):
        """Calculates the effect size statisctics."""
        aov_data['mean_sq'] = aov_data[:]['sum_sq'] / aov_data[:]['df']
        aov_data['eta_sq'] = aov_data[:-1]['sum_sq'] / sum(aov_data['sum_sq'])
        aov_data['omega_sq'] = (aov_data[:-1]['sum_sq'] - (aov_data[:-1]['df'] * aov_data['mean_sq'][-1])) / (sum(aov_data['sum_sq']) + aov_data['mean_sq'][-1])
        cols = ['sum_sq', 'df', 'mean_sq', 'F', 'PR(>F)', 'eta_sq', 'omega_sq']
        aov_data = aov_data[cols]
        return aov_data

    # Regression (ordinary least squares) for this metric and experiment type
    anova = ols(metric + '~ C(' + groups + ')', data=data).fit()
    # print(anova.summary())

    # Calculate the stats table
    anova_table = sm.stats.anova_lm(anova, typ=2)

    # Add effect size to table
    anova_frame = _anova_table(anova_table)

    # Add power analysis
    effect, exp_n, power = anova_power_analysis(data, groups, metric, alpha=0.05, power=0.8)

    power_analysis_cols = {'cohen_f': effect, 'n': len(data), 'exp_n': exp_n, 'power': power, 'exp_power': 0.8}
    anova_frame = anova_frame.assign(**power_analysis_cols)

    # Round to 6 decimal places
    # anova_frame = anova_frame.round(6)
    return anova_frame


def tukey_hsd(data, groups, metric):
    """ANOVA and Tukey HSD post-hoc comparison from statsmodels.

    The Tukey HSD post-hoc comparison test controls for type I error and maintains the familywise error rate at 0.05.
    The group1 and group2 columns are the groups being compared,
    meandiff column is the difference in means of the two groups being calculated as group2 – group1,
    lower/upper columns are the lower/upper boundaries of the 95% confidence interval,
    reject column states whether or not the null hypothesis should be rejected.

    Args:
        data (Dataframe): Dataframe grouped by dialogue group and label_type values.
        groups (string): Indicates which columns values to group data for comparison i.e. label_type.
        metric (string): Indicates which column name has the result values i.e. values/times.

    Returns:
        tukey_frame (Dataframe): Contains f-statistic, p-value and eta/omega effect sizes.

            group1   group2  meandiff  p-value   lower   upper  reject
        0       ap  ap type   -0.1167   0.8059 -0.5825  0.3492   False
        1       ap       da    0.1000   0.8543 -0.3659  0.5659   False
        2  ap type       da    0.2167   0.5158 -0.2492  0.6825   False
    """
    # Compare the results (metric) for the range of values for this experiment_type
    multi_comparison = MultiComparison(data=data[metric], groups=data[groups])
    # Create the tukey results table
    tukey_results = multi_comparison.tukeyhsd()

    # Convert the results to a dataframe
    tukey_frame = pd.DataFrame(data=tukey_results._results_table.data[1:], columns=tukey_results._results_table.data[0])
    tukey_frame.rename(columns={'p-adj': 'p-value'}, inplace=True)

    return tukey_frame


def chi_squared(group_1, group_2):
    """Chi Squared from scipy stats.

    Chi-square test of independence of variables in a contingency table.

    This function computes the chi-square statistic and p-value for the hypothesis test of independence of the observed
    frequencies in the contingency table observed.
    The expected frequencies are computed based on the marginal sums under the assumption of independence;
    If p-value ≤ alpha or chi statistic ≥ critical value, then reject null hypothesis -
    distributions are considered dependant on group variable.
    Else accept null hypothesis - distributions are considered independent of group variable.
    The number of degrees of freedom is (expressed using numpy functions and attributes)

    Args:
        group_1 (list): List of observed frequencies for one group of variables.
        group_2 (list): List of observed frequencies for one group of variables.

    Returns:
        dof (float): Degrees of freedom, calculated as (rows − 1) × (cols − 1).
        critical (float): Critical value for interpreting Chi stat.
        chi (float): Chi squared value.
        p (float): P-value for interpreting result.
        reject (bool): Whether to accept or reject null hypothesis.
    """
    # Create contingency table
    for i, e in reversed(list(enumerate(group_1))):
        if group_1[i] == 0 and group_2[i] == 0:
            del group_1[i]
            del group_2[i]
    table = [group_1, group_2]

    # Compare categorical distributions
    chi, p, dof, expected = chi2_contingency(table)

    # Interpret test-statistic
    prob = 0.95
    critical = chi2.ppf(prob, dof)
    reject = True if abs(chi) >= critical else False

    return dof, critical, chi, p, reject


def jensen_shannnon(prob_distributions, logbase=2):
    """Generalised version of Jensen-Shannon Divergence

    Compares two or more probability distributions and returns a distance value.
    Distance value is bounded as 0<JSD<log2(n) where n is the number of distributions compared.

    Args:
        prob_distributions (list): 2 Dimensional list of probability distributions (each row a distribution).
        logbase (int): The base of the logarithm used to compute the output.

    Returns:
        divergence (float): Distance between probability distributions.
    """

    prob_distributions = np.array(prob_distributions)
    # All equal weights
    weights = 1 / len(prob_distributions)
    # Left term: entropy of mixture
    weight_probs = weights * prob_distributions
    mixture = weight_probs.sum(axis=0)
    entropy_of_mixture = H(mixture, base=logbase)

    # Right term: sum of entropies
    entropies = np.array([H(P_i, base=logbase) for P_i in prob_distributions])
    weight_entropies = weights * entropies
    sum_of_entropies = weight_entropies.sum()

    divergence = entropy_of_mixture - sum_of_entropies
    return divergence
