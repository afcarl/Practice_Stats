'''
Stats Sprint
'''


def rank_ks():
    cleveland = [c_array[:,2], c_array[:,3], c_array[:,5]]
    labels= ['chest pain', 'resting blood pressure', 'blood sugar']
    results = {}
    
    for idx, data in enumerate(cleveland):
        count, bin, ignore = hist(data, 30, color="red", normed=True)
        
        norm_cdf = st.norm.cdf(bin, mean(data), std(data))
        data_cdf = cumsum(count) * (bin[1] - bin[0])
        
        # low ks_stat or high p_val cannot reject hypothesis the distribution of hte two samples are the same
        ks_stat, p_val = st.ks_2samp(data_cdf, norm_cdf) 
        results[labels[idx]] = (ks_stat, p_val)
#    print sorted(results.iteritems(), key=lambda x: x[1])
    pvals, dvals= [], []
    for k,v in results.iteritems():
        pvals.append(v[1])
        dvals.append(v[0])
    
    #plt.imshow([pvals, dvals])
    plt.show()

rank_ks()