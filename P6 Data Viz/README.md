# Data Viz Project
The visualization can be viewed here: http://bl.ocks.org/stasSajin/raw/a13083b75b6adb92fcfd3e33655eec01/

##Summary
This project aims to compare the realized returns with the estimated returns for about 25,000 loans from the Prosper Loan Data. The dataset used includes only the loans that have either been paid in full, charged-off or defaulted. In other words, it does not include loans that have not been repaid yet. I have cleaned up the data in R (see the .rmd file).

* The visualization focuses on a very clear and specific finding, which is that Prosper's estimated return had been over-estimated relative to the realized return. 
* This finding is communicated by showcasing that the the realized returns are consistently lower during the July 2009 till Nov 2013.
* This visualization also showcases that Prosper has gotten better with their under-writing, as the divergence between the estimated and realized returns has improved over time. 

##Design
Initially, I reflected on using a bar chart, which shows the bar for the estimated and the realized returns. Nonetheless, the bar chart hides a very interesting pattern in the data, which is that the realized and estimated returns converge over time, so I decided to rely on line plots. I used line plots for several reasons:

1. I wanted to showcase the viewer that Prosper has gotten better at accurately estimating the returns on newer loans. This *learning* could be showcased by showing how realized and estimated returns differ from each other over time.
2. Jonathan mentioned in the lecture that it is best to use line-charts to showcase the continuity for the time in the x-axis. 
3. I also used a mouse-hover tool (see resources). This interactive tool is very crucial to the visualization, since it highlights and showcases the values for the two returns for a particular period that the viewer chooses. This makes it very easy to see just how big, numerically, was the difference between the two types of returns. Without this tool, the reader would be left with no choice but to ball-park the difference between the two returns for a particular month.  

Here are my initial decisions for what I wanted in a graph:

* I wanted to use a multi-series time plot that shows the return on the y-axis and the date on the x-axis. Initially, I thought to set the date to monthly, but this made the axis very cluttered, so I chose the axis ticks to be roughly every 4-th month.
* I wanted the lines to be encoded in a color-blind color. The legend would be used to specify which color corresponds to which return. 
* I did not want any grid-lines, since I planned to use the mouse-hover tool


##Feedback

###Linda Zhang
Ok, so this graph shows that Prosper is likely over-estimating the returns on the loans. This is interesting and very informative. The information is also very easy to grasp, since the difference between realized and actual returns is so large. What I find interesting is that Prosper got better at estimating their returns and that towards the end of the 2014, the realized and estimated returns converge.

One question that I have is why is there a dip in realized returns towards the end?

Some suggestion for improving the plot would be to include an introductory paragraph and a summary paragraph at the end. Also, I would suggest to make the title of the axes larger and to clean up the ticks.

(I talked with this reviewer more and we decided after this to present the loans only up until the November of 2013. The dip in realized returns towards the end of the graph appears because there are only very few loans that have matured during that period (either because of pre-payments or because of defaults). Since the loans were just issued, their status is not yet completed (in other words the loan is still current; it can achieve a completed status if it was fully repaid, defaulted, or charged-off)

###Henry Zhang
This graph indicates that one should be wary of the promises Prosper makes in regard to the loans they are under-writing. The line plot is very easy to process and understand. I also appreciate the interactivity present in the plot. Here are some issues that need to be fixed:

* The x-axis title needs to be lager
* The ticks for the x-axis need to be changed (right now they are overlapping)
* It would be useful to include a description as to what estimated and realized returns are
* A summary with the main points should be included at the end, where the message is clearly conveyed to the user.

###Mihai Sajin
This graphs helps explain a lot of questions as to why I was never achieving the promised returns on my diversified loan portfolio through prosper. It clearly shows that investors are over-promised in regard to the expected return and the actual return is much lower. 

What is the issue with the dip in realized returns? Is it because there are only a few loans for that period? Also, why is there no info present for the more recent loans?

I suggest you fix the axis and include a summary for the plot, so that the main take-a-way is easily available. 


**I have improved in the feedback above in the following ways:**

* I have included a summary and a small conclusions section above and below the visualization
* I have decided to cut out the portion of the data where there is a dip in realized returns, as that portion reflects only a small amount of loans and is over-represented with defaulted loans.
* I have cleaned up the x-axis, so that is not so cluttered. 

##Resources used

* [d3 tutorial](https://d3js.org/)
* [CSS Tutorial](http://www.w3schools.com/css/default.asp)
* [Creating multi-series line plot with mouse-over](http://stackoverflow.com/questions/34886070/d3-js-multiseries-line-chart-with-mouseover-tooltip/34887578#34887578) This resource was very helpful, as the base code in my plot was taken from here.
* [Scott Murray's Book Introduction to D3](http://alignedleft.com/tutorials/d3)
* [D3 in Action by Elijah Meeks](https://www.manning.com/books/d3-js-in-action)