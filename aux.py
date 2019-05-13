def gen_params():
    params={}
    params['M']   = 0.938
    params['M_h'] = 0.139
    params['x_bj']= 0.1
    params['z_h'] = 0.1
    params['eta']   = 0
    params['Q']   = 10.0
    params['T_t'] = 0.1
    params['xi']  = 0.3
    params['zeta']= 0.3
    params['delta_k_t']=0.1
    params['k_i_t']=0.01
    params['M_ki']=0.1
    params['M_kf']=0.1
    return params

def evaluate(func,params=None,verb=False):
    if params==None: params=gen_params()
    keys=['M','M_h','x_bj','z_h','eta','Q','T_t','xi','zeta','delta_k_t','k_i_t','M_ki','M_kf']
    args=[params[_] for _ in keys]
    return func(*args)

