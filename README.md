## log_project
**log_project** is a _udacity_ project to demostrate what was learned in the classroom. 
There are 3 questions to be solved by log_project:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?

## How to run the program
**log_project** has been tested using _python 3.6.3_ so the recommendation is to use that version. You can try other version and program may still run.
To run the program just open a terminal and run:`python log_project.py`
**Note**: make sure you have the "_news_" database which is used as an input to **log_project**. 
If you need to download the "_news_" database then click [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip), unzip the file to extract newsdata.sql then open a terminal and run `psql -d news -f newsdata.sql`

## log_project design
**log_project** code design is simple, it defines a _python_ function to respond each of the 3 questions for the project:
1. What are the most popular three articles of all time? `most_popular_article()`
2. Who are the most popular article authors of all time? `most_popular_author()`
3. On which days did more than 1% of requests lead to errors? `days_with_errors()`

`most_popular_article()` and `most_popular_author()` use `print result()` to display the result of the query using a loop.
`days_with_errors` displays the result of the query by itself since the data has to be converted to the required format ("YYYY-MM-DD" to "Month Day, Year").
There are additional comments in the code that explains the strategy followed to define each query that solves the 3 questions above.