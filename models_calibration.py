import numpy as np
import statsmodels as sm
from scipy import stats
import statsmodels.api as sm
from statsmodels.base.model import GenericLikelihoodModel


class UnivariateNormal(GenericLikelihoodModel):
    def __init__(self, endog, **kwds):
        super(UnivariateNormal, self).__init__(endog, **kwds)

    def loglike(self, params):
        return np.sum(
            np.log(stats.norm.pdf(self.endog, loc=params[0], scale=params[1]))
        )

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
        if start_params == None:
            # Reasonable starting values
            start_params = [np.mean(self.endog), np.std(self.endog)]
            return super(UnivariateNormal, self).fit(
                start_params=start_params, maxiter=maxiter, maxfun=maxfun, **kwds
            )


class UnivariateLogNormal(GenericLikelihoodModel):
    def __init__(self, endog, **kwds):
        super(UnivariateLogNormal, self).__init__(endog, **kwds)

    def loglike(self, params):
        return np.sum(
            np.log(stats.lognorm.pdf(self.endog, s=params[0], scale=params[1]))
        )

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
        if start_params == None:
            # Reasonable starting values
            _scale = np.median(self.endog)  # exp(mu)
            _shape = np.sqrt(2 * np.log(np.mean(self.endog) / _scale))
            start_params = [_shape, _scale]
            return super(UnivariateLogNormal, self).fit(
                start_params=start_params, maxiter=maxiter, maxfun=maxfun, **kwds
            )


class UnivariateBeta(GenericLikelihoodModel):
    def __init__(self, endog, **kwds):
        super(UnivariateBeta, self).__init__(endog, **kwds)

    def loglike(self, params):
        return np.sum(np.log(stats.beta.pdf(self.endog, a=params[0], b=params[1])))

    def fit(self, start_params=None, maxiter=10000, maxfun=5000, **kwds):
        if start_params == None:
            # Reasonable starting values
            _scale = np.median(self.endog)  # a
            _shape = np.sqrt(2 * np.log(np.mean(self.endog) / _scale))
            start_params = [_shape, _scale]
            return super(UnivariateBeta, self).fit(
                start_params=start_params, maxiter=maxiter, maxfun=maxfun, **kwds
            )


data = stats.lognorm.rvs(size=800, s=0.4, scale=0.01)
mod = UnivariateLogNormal(endog=data)
res = mod.fit()
print(f"Parameters : {res.params}")  # Parameters [shape, scale]
print(f"Standard errors {res.bse}")  # Standard errors
