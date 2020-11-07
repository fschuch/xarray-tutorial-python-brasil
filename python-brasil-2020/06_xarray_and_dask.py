#!/usr/bin/env python
# coding: utf-8

# <img src="http://xarray.pydata.org/en/stable/_static/dataset-diagram-logo.png" align="right" width="30%">
# 
# # Xarray and Dask
# 
# This notebook demonstrates one of xarray's most powerful features: the ability
# to wrap dask arrays and allow users to seamlessly execute analysis code in
# parallel.
# 
# By the end of this notebook, you will:
# 
# 1. Xarray DataArrays and Datasets are "dask collections" i.e. you can execute
#    top-level dask functions such as `dask.visualize(xarray_object)`
# 2. Learn that all xarray built-in operations can transparently use dask
# 3. Learn that xarray provides tools to easily parallelize custom functions
#    across blocks of dask-backed xarray objects.
# 
# ## Table of contents
# 
# 1. [Reading data with Dask and Xarray](#readwrite)
# 2. [Parallel/streaming/lazy computation using dask.array with Xarray](#compute)
# 3. [Automatic parallelization with apply_ufunc and map_blocks](#applymap)
# 
# First lets do the necessary imports, start a dask cluster and test the dashboard
# 

# In[2]:


import expectexception
import numpy as np
import xarray as xr


# First lets set up a `LocalCluster` using `dask.distributed`.
# 
# You can use any kind of dask cluster. This step is completely independent of
# xarray.
# 

# In[3]:


from dask.distributed import Client

client = Client()
client


# <p>&#128070</p> Click the Dashboard link above. Or click the "Search" button in the dashboard.
# 
# Let's test that the dashboard is working..
# 

# In[1]:


import dask.array

dask.array.ones(
    (1000, 4), chunks=(2, 1)
).compute()  # should see activity in dashboard


# <a id='readwrite'></a>
# 
# ## Reading data with Dask and Xarray
# 
# The `chunks` argument to both `open_dataset` and `open_mfdataset` allow you to
# read datasets as dask arrays. See
# https://xarray.pydata.org/en/stable/dask.html#reading-and-writing-data for more
# details
# 

# In[4]:


ds = xr.tutorial.open_dataset(
    "air_temperature",
    chunks={
        "lat": 25,
        "lon": 25,
        "time": -1,
    },  # this tells xarray to open the dataset as a dask array
)
ds


# The repr for the `air` DataArray shows the dask repr.
# 

# In[5]:


ds.air


# In[6]:


ds.air.chunks


# **Tip**: All variables in a `Dataset` need _not_ have the same chunk size along
# common dimensions.
# 

# In[7]:


mean = ds.air.mean("time")  # no activity on dashboard
mean  # contains a dask array


# This is true for all xarray operations including slicing
# 

# In[8]:


ds.air.isel(lon=1, lat=20)


# and more complicated operations...
# 

# <a id='compute'></a>
# 
# ## Parallel/streaming/lazy computation using dask.array with Xarray
# 
# Xarray seamlessly wraps dask so all computation is deferred until explicitly
# requested
# 

# In[9]:


mean = ds.air.mean("time")  # no activity on dashboard
mean  # contains a dask array


# This is true for all xarray operations including slicing
# 

# In[10]:


timeseries = (
    ds.air.rolling(time=5).mean().isel(lon=1, lat=20)
)  # no activity on dashboard
timeseries  # contains dask array


# In[11]:


timeseries = ds.air.rolling(time=5).mean()  # no activity on dashboard
timeseries  # contains dask array


# ### Getting concrete values from dask arrays
# 
# At some point, you will want to actually get concrete values from dask.
# 
# There are two ways to compute values on dask arrays. These concrete values are
# usually numpy arrays but could be a `pydata/sparse` array for example.
# 
# 1. `.compute()` returns an xarray object
# 2. `.load()` replaces the dask array in the xarray object with a numpy array.
#    This is equivalent to `ds = ds.compute()`
# 

# In[12]:


computed = mean.compute()  # activity on dashboard
computed  # has real numpy values


# Note that `mean` still contains a dask array
# 

# In[13]:


mean


# But if we call `.load()`, `mean` will now contain a numpy array
# 

# In[14]:


mean.load()


# Let's check that again...
# 

# In[ ]:


mean


# **Tip:** `.persist()` loads the values into distributed RAM. This is useful if
# you will be repeatedly using a dataset for computation but it is too large to
# load into local memory. You will see a persistent task on the dashboard.
# 
# See https://docs.dask.org/en/latest/api.html#dask.persist for more
# 

# ### Extracting underlying data: `.values` vs `.data`
# 
# There are two ways to pull out the underlying data in an xarray object.
# 
# 1. `.values` will always return a NumPy array. For dask-backed xarray objects,
#    this means that compute will always be called
# 2. `.data` will return a Dask array
# 
# #### Exercise
# 
# Try extracting a dask array from `ds.air`
# 

# Now extract a NumPy array from `ds.air`. Do you see compute activity on your
# dashboard?
# 

# ## Xarray data structures are first-class dask collections.
# 
# This means you can do things like `dask.compute(xarray_object)`,
# `dask.visualize(xarray_object)`, `dask.persist(xarray_object)`. This works for
# both DataArrays and Datasets
# 
# #### Exercise
# 
# Visualize the task graph for `mean`
# 

# Visualize the task graph for `mean.data`. Is that the same as the above graph?
# 

# <a id='applymap'></a>
# 
# ## Automatic parallelization with apply_ufunc and map_blocks
# 
# Almost all of xarray’s built-in operations work on Dask arrays.
# 
# Sometimes analysis calls for functions that aren't in xarray's API (e.g. scipy).
# There are three ways to apply these functions in parallel on each block of your
# xarray object:
# 
# 1. Extract Dask arrays from xarray objects (`.data`) and use Dask directly e.g.
#    (`apply_gufunc`, `map_blocks`, `map_overlap`, or `blockwise`)
# 
# 2. Use `xarray.apply_ufunc()` to apply functions that consume and return NumPy
#    arrays.
# 
# 3. Use `xarray.map_blocks()`, `Dataset.map_blocks()` or `DataArray.map_blocks()`
#    to apply functions that consume and return xarray objects.
# 
# Which method you use ultimately depends on the type of input objects expected by
# the function you're wrapping, and the level of performance or convenience you
# desire.
# 

# ### `map_blocks`
# 
# `map_blocks` is inspired by the `dask.array` function of the same name and lets
# you map a function on blocks of the xarray object (including Datasets!).
# 
# At _compute_ time, your function will receive an xarray object with concrete
# (computed) values along with appropriate metadata. This function should return
# an xarray object.
# 
# Here is an example
# 

# In[ ]:


def time_mean(obj):
    # use xarray's convenient API here
    # you could convert to a pandas dataframe and use pandas' extensive API
    # or use .plot() and plt.savefig to save visualizations to disk in parallel.
    return obj.mean("lat")


ds.map_blocks(time_mean)  # this is lazy!


# In[ ]:


# this will calculate values and will return True if the computation works as expected
ds.map_blocks(time_mean).identical(ds.mean("lat"))


# #### Exercise
# 
# Try applying the following function with `map_blocks`. Specify `scale` as an
# argument and `offset` as a kwarg.
# 
# The docstring should help:
# https://xarray.pydata.org/en/stable/generated/xarray.map_blocks.html
# 
# ```
# def time_mean_scaled(obj, scale, offset):
#     return obj.mean("lat") * scale + offset
# ```
# 

# #### More advanced functions
# 
# `map_blocks` needs to know what the returned object looks like _exactly_. It
# does so by passing a 0-shaped xarray object to the function and examining the
# result. This approach cannot work in all cases For such advanced use cases,
# `map_blocks` allows a `template` kwarg. See
# https://xarray.pydata.org/en/latest/dask.html#map-blocks for more details
# 

# ### apply_ufunc
# 
# `apply_ufunc` is a more advanced wrapper that is designed to apply functions
# that expect and return NumPy (or other arrays). For example, this would include
# all of SciPy's API. Since `apply_ufunc` operates on lower-level NumPy or Dask
# objects, it skips the overhead of using Xarray objects making it a good choice
# for performance-critical functions.
# 
# `apply_ufunc` can be a little tricky to get right since it operates at a lower
# level than `map_blocks`. On the other hand, Xarray uses `apply_ufunc` internally
# to implement much of its API, meaning that it is quite powerful!
# 

# ### A simple example
# 
# Simple functions that act independently on each value should work without any
# additional arguments. However `dask` handling needs to be explictly enabled
# 

# In[ ]:


get_ipython().run_cell_magic('expect_exception', '', '\nsquared_error = lambda x, y: (x - y) ** 2\n\nxr.apply_ufunc(squared_error, ds.air, 1)')


# There are two options for the `dask` kwarg.
# 
# 1. `dask="allowed"` Dask arrays are passed to the user function. This is a good
#    choice if your function can handle dask arrays and won't call compute
#    explicitly.
# 2. `dask="parallelized"`. This applies the user function over blocks of the dask
#    array using `dask.array.blockwise`. This is useful when your function cannot
#    handle dask arrays natively (e.g. scipy API).
# 
# Since `squared_error` can handle dask arrays without computing them, we specify
# `dask="allowed"`.
# 

# In[ ]:


sqer = xr.apply_ufunc(
    squared_error,
    ds.air,
    1,
    dask="allowed",
)
sqer  # dask-backed DataArray! with nice metadata!


# ### A more complicated example with a dask-aware function
# 
# For using more complex operations that consider some array values collectively,
# it’s important to understand the idea of **core dimensions** from NumPy’s
# generalized ufuncs. Core dimensions are defined as dimensions that should not be
# broadcast over. Usually, they correspond to the fundamental dimensions over
# which an operation is defined, e.g., the summed axis in `np.sum`. A good clue
# that core dimensions are needed is the presence of an `axis` argument on the
# corresponding NumPy function.
# 
# With `apply_ufunc`, core dimensions are recognized by name, and then moved to
# the last dimension of any input arguments before applying the given function.
# This means that for functions that accept an `axis` argument, you usually need
# to set `axis=-1`
# 
# Let's use `dask.array.mean` as an example of a function that can handle dask
# arrays and uses an `axis` kwarg
# 

# In[ ]:


def time_mean(da):
    return xr.apply_ufunc(
        dask.array.mean,
        da,
        input_core_dims=[["time"]],
        dask="allowed",
        kwargs={"axis": -1},  # core dimensions are moved to the end
    )


time_mean(ds.air)


# In[ ]:


ds.air.mean("time").identical(time_mean(ds.air))


# ### Automatically parallelizing dask-unaware functions
# 
# A very useful `apply_ufunc` feature is the ability to apply arbitrary functions
# in parallel to each block. This ability can be activated using
# `dask="parallelized"`. Again xarray needs a lot of extra metadata, so depending
# on the function, extra arguments such as `output_dtypes` and `output_sizes` may
# be necessary.
# 
# We will use `scipy.integrate.trapz` as an example of a function that cannot
# handle dask arrays and requires a core dimension.
# 

# In[ ]:


import scipy as sp
import scipy.integrate

sp.integrate.trapz(ds.air.data)  # does NOT return a dask array


# #### Exercise
# 
# Use `apply_ufunc` to apply `sp.integrate.trapz` along the `time` axis so that
# you get a dask array returned. You will need to specify `dask="parallelized"`
# and `output_dtypes` (a list of `dtypes` per returned variable).
# 

# ## More
# 
# 1. https://xarray.pydata.org/en/stable/examples/apply_ufunc_vectorize_1d.html#
# 2. https://docs.dask.org/en/latest/array-best-practices.html
# 
