#!/usr/bin/env python3
# Code for the log project
import psycopg2
from datetime import datetime

DBNAME = "news"

"""function to print the results of exercise #1 and """


def print_results(c, s):
    while True:
        row = c.fetchone()
        if row is None:
            break
        print("    * {0} - {1} {2}".format(row[0], row[1], s))
    return


"""Exercise #1: list the 3 most popular articles of all time.
    The most popular article at the top"""


def most_popular_article():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    """Count the views of each article (joining articles and log DB) then
        order the table descending"""
    c.execute("select title, \
                  count(log.id) as views \
              from articles \
                  join log \
                      on log.path = CONCAT('/article/', articles.slug) \
              group by title \
              order by views desc limit 3;")
    # Print the result of running the query
    print_results(c, "views")
    db.close()
    return


"""Exercise #2: list the most popular authors. Sum up all the articles each
    author has written and considering how many times they had been visited.
    Most popular author at the top"""


def most_popular_author():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    """Count the views of each article (joining articles, authors and log DB)
        then sum up all the views of articles written by the same author
        (grouping by author name)"""
    c.execute("select name,\
                  sum(views) as views \
              from (select title, \
                        name, count(log.id) as views \
                    from ((authors \
                        join articles \
                            on authors.id = author) \
                    join log \
                        on log.path like CONCAT('%', slug)) \
                    group by title, \
                    name) as subq\
              group by name \
              order by views desc;")
    print_results(c, "views")
    db.close()
    return


"""Exercise #3: List the days with more than 1% of requests
    leading to an error"""


def days_with_errors():
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    """Create a table with dates (one row per day) and number of request on
        that day, add a column with the number of request leading to an error.
        The final table will include only the rows with more than 1% of errors.
            This table will include the date, total number of views and number
            of views leading to an error.
            This data will be formatted in python before being displayed"""
    c.execute("select date_all, \
                  views, views_e \
              from (select to_char(time, 'YYYY-MM-DD') as date_all,\
                        count(*) as views \
                    from log \
                    group by date_all) as all_views \
                    join (select to_char(time, 'YYYY-MM-DD') as date_e, \
                              count(*) as views_e \
                          from log \
                          where status <> '200 OK' \
                          group by date_e) as error_views \
                    on date_all=date_e \
                        and error_views.views_e>(all_views.views*0.01) \
                group by date_all, \
                    views, \
                    views_e;")
    while True:
        row = c.fetchone()
        if row is None:
            break
        '''Get the string "YYYY-MM-DD" from the DB and put it in a
            datetime object'''
        date_obj = datetime.strptime(row[0], "%Y-%m-%d")
        '''convert the "YYYY-MM-DD" datetime object to "Month Day, Year"'''
        formatted_date = datetime.strftime(date_obj, "%B %d, %Y")
        '''Divide the views leading to an error by the total of views and
            multiply the result by 100 to get the percentage'''
        errors = (float(row[2])/float(row[1]))*100
        print("    * {0} - {1:.1f}% errors".format(formatted_date, errors))
    db.close()
    return


if __name__ == '__main__':
    print("\n\n3 Most Popular articles of all time:")
    most_popular_article()
    print("\n\nMost Popular authors:")
    most_popular_author()
    print("\n\nDays with more than 1% of requests leading to errors:")
    days_with_errors()
