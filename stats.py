'''
Stats Sprint
'''

import numpy as np
import matplotlib.pyplot as plt
import seaborn
import scipy.stats as st

def read_data(filename):
    f = open(filename)
    important=['age', 'sex', 'resting_blod_pressuremm_hg', 'cholesterol_mg/dl', 'max_heart_rate']
    keys = f.readline().strip().split(",")
    key_to_index = {}
    for i in range(len(keys)):
        key_to_index[keys[i]] = i
    result = []
    for line in f:
        line = line.strip().split(",")
        skip = False
        for key in important:
            if line[key_to_index[key]] == '?':
                skip = True
        if not skip:
            line = map(lambda x: None if x == "?" else float(x), line)
            result.append(line)
    f.close()
    return key_to_index, np.array(result)

def age_distributions(loc_data):
    print "Location Age Histograms"
    fig, axes = plt.subplots(nrows=2, ncols=2)

    color_vals = ["orange","green","blue", "purple"]
    
    for i, (ax, (name, data)) in enumerate(zip(axes.flat,(loc_data))):
        ax.hist(data[:,0], color=color_vals[i])
        ax.set_title(name)
        ax.set_ylabel('age (avg=%d)' % np.mean(data[:,0]))
        ax.set_xlabel('count')
    plt.subplots_adjust(wspace = 0.3, hspace = 0.5)
    plt.show()


def boxplots(keys, loc_data):
    print
    print "Location Heart Rate & Cholesterol Box Plots"
    hr = keys['max_heart_rate']
    chl = keys['cholesterol_mg/dl']
    male_hr, female_hr, male_chl, female_chl = [], [], [], []

    for (name,data) in loc_data:
        male_hr = np.append(male_hr, data[data[:,1] == 0, hr], axis=0)
        female_hr = np.append(female_hr, data[data[:,1] == 1, hr], axis=0)
        male_chl = np.append(male_chl, data[data[:,1] == 0, chl], axis=0)
        female_chl = np.append(female_chl, data[data[:,1] == 1, chl], axis=0)

    fig, axes = plt.subplots(ncols=2)
    axes[0].boxplot((male_hr, female_hr))
    axes[0].set_title('Heart Rate')
    axes[0].set_xticklabels(['male', 'female'])

    axes[1].boxplot((male_chl, female_chl))
    axes[1].set_title('Cholesterol')
    axes[1].set_xticklabels(['male', 'female'])

    plt.show()


def blood_pressure(keys, loc_data):
    print
    print "Blood Pressure Histogram Comparison"

    bp = keys['resting_blod_pressuremm_hg']
    color_vals = ["red","blue"]

    fig, axes = plt.subplots(nrows=4, figsize=(6, 12))
    for i, (ax, (name, data)) in enumerate(zip(axes.flat,(loc_data))):
        ax.hist(data[data[:,1] == 1, bp], color="red")
        ax.hist(data[data[:,1] == 0, bp], color="blue")
        ax.set_title(name)
        ax.set_xlabel('blood pressure')
        ax.legend(['male', 'female'], loc="upper left")

    plt.subplots_adjust(hspace = 1)
    #plt.show()

def fit_the_line(keys, loc_data):
    print
    print "Probability Density Function"

    data = loc_data[0][1]
    bp = keys['resting_blod_pressuremm_hg']
    fig, axes = plt.subplots(nrows=4, figsize=(6, 12))

    for i, (ax, (name, data)) in enumerate(zip(axes.flat,(loc_data))):
        m_blood = data[data[:,1] == 1, bp]
        f_blood = data[data[:,1] == 0, bp]

        m_blood_mean = np.nanmean(m_blood)
        f_blood_mean = np.nanmean(f_blood)
        m_blood_std = np.std(m_blood)     
        f_blood_std = np.std(f_blood)

        m_count, m_bins, m_ignored = ax.hist(m_blood, 30, color="red", normed=True) 
        f_count, f_bins, f_ignored = ax.hist(f_blood, 30, color="blue", normed=True)

        m_pdf = st.norm.pdf(m_bins, loc=m_blood_mean, scale=m_blood_std)  
        f_pdf = st.norm.pdf(f_bins, loc=f_blood_mean, scale=f_blood_std)
    
        ax.plot(m_bins, m_pdf, color="green")  
        ax.plot(f_bins,f_pdf, color="purple")  
    plt.show()

def check_ks(keys, loc_data):
    print
    print "KS Test Distributions"
    print
    name, data = loc_data
    x = data[:,3]
    fig, axes = plt.subplots(nrows=2, figsize=(6, 12))
    
    count, bins, ignore= axes[0].hist(x, 30, color="green", normed=True)
    norm_cdf = st.norm.cdf(bins, np.mean(x), np.std(x))
    data_cdf = np.cumsum(count) * (bins[1] - bins[0])

    axes[1].plot(norm_cdf)
    axes[1].plot(data_cdf)
    axes[1].set_title("KS Plot")

    d_stat, p_val = st.ks_2samp(data_cdf, norm_cdf)
    
    print "D_stat = ", d_stat, "P_val = ", p_val
    print "The distributions are the same = ", ((d_stat < 0.20) and (p_val > 0.05))

# Need to sync below with above
def rank_ks(loc_data):
    name, data = loc_data
    data_per_issue = [data[:,2], data[:,3], data[:,5]]
    labels= ['chest pain', 'resting blood pressure', 'blood sugar']
    results = {}
    
    for idx, d in enumerate(data_per_issue):
        count, d_bin, ignore = plt.hist(d, 30, color="red", normed=True)
        try:
            norm_cdf = st.norm.cdf(d_bin, np.mean(data), np.std(data))
            data_cdf = np.cumsum(count) * (d_bin[1] - d_bin[0])
        except:
            print "error", count, d, d_bin
            data_cdf = 0
            norm_cdf = 0
        
        # low d_stat or high p_val cannot reject hypothesis - distribution are equal
        ks_stat, p_val = st.ks_2samp(data_cdf, norm_cdf) 
        results[labels[idx]] = (ks_stat, p_val)
#    print sorted(results.iteritems(), key=lambda x: x[1])
    pvals, dvals= [], []
    for k,v in results.iteritems():
        pvals.append(v[1])
        dvals.append(v[0])
    
    plt.imshow([pvals, dvals])
    plt.show()

def main():
    c_keys, c_array = read_data("./data/cleveland_heart.csv")
    h_keys, h_array = read_data("./data/hungarian_heart.csv")
    l_keys, l_array = read_data("./data/long_beach.csv")
    s_keys, s_array = read_data("./data/switzerland_heart.csv")
    
    loc_data = [('Cleveland',c_array), ('Hungary', h_array), ('Long Beach', l_array), ('Switzerland',s_array)]

    one_loc_data = ('Cleveland',c_array)

    age_distributions(loc_data)
    boxplots(c_keys, loc_data)
    blood_pressure(c_keys, loc_data)
    fit_the_line(c_keys, loc_data)
    check_ks(c_keys, one_loc_data)
    #rank_ks(one_loc_data)


if __name__ == "__main__":
    main()