# solarCorrelations
ECE 225A project analyzing solar energy resource correlations across states.

 ## Introduction:
Low cost solar power has rapidly transformed new electricity supply in the United States.
Photovoltaics account for more than half of new generation capacity as of 2024 [CITATION]. As the
price of solar continues to go down, it is only expected to play a larger role in the future of electrical grids.

But even while solar has been a significant favorite in recent years to older generation technology, due to its renewable
nature and cheap generation, it also introduces new challenges. The most obvious problem is variabilty. The sun, while
a nearly infinite source of energy, does not always have a clear path to the panels harvesting that energy. While day-night
cycles can be accounted for with dispatchable energy storage, which has also seen a meteoric rise in the local grid,
there are also days where solar generation is lower than the expected capacity.

If this variability was uncorrelated between different power plants, this would not be a significant issue.
But because these plants can be heavily correlated, for instance a storm system crossing over California, could
cause low production across the entire state.

Because of this, projects that connect the grids of different regions have become more popular recently. One such example is SunZia,
a high voltage DC cable that connects New Mexico to southern California. Ideally this HVDC line would provide *independent* sources of
solar electricity to either California or New Mexico.

In this project, I want to measure the empirical independence or correlation of New Mexico and California's expected sunlight.
I will use a variety of techniques to get an understanding of the relationship between their respective solar irradiance.

 ## Methods

Four locations in southern California, and four locations in New Mexico will first be selected. Solar irradiance in the form of
direct normal irradiance (DNI) or global horizontal irradiance (GHI) will be used, as they closely correlate with solar panel production
(CITATION). These values can be retrieved from the National Solar Radiation Database. This database provides hourly solar radiation for
selectable locations across the United States.

Using the four locations, we can first get a baseline correlation within states, and also get a state average of radiation data.
Using these state averages, we can remove some local variance while still comparing state variance. Then we can measure the covariance,
and look at how related these power sources are. On top of this, we can remove some of the annual variance that we expect by looking
at the covariance of individual months, and also look at extreme deviations from the mean, e.g. multiple standard deviations, to see if
they are likely to be shared between states.

There are multiple other statistical analyses that can be run on this dataset.
