/index  
- default landing page
- provides links to search, browse, and add entry

/search  
- provides interface to user to input search terms
- makes use of building a SQL query based on form string inputs then executing it on the database session
GET:   
- provides blank search form
POST:   
- provides number of returned rows and displays returned rows

/show/pagenumber  
- displays paginated results from current table row by row
- provides links to edit or delete each row
- provides links to move through paginated results
- provides link to filter and sort resulting table
- pagenumber indicates how many pages into the pagination

/sortBy/<string>  
- displays paginated results from current table sorted by the selected column
- ascending/descending toggle by number of clicks
- string indicates which column name the currently displayed table is being sorted on

/edit/id  
GET:  
- provides form populated with contents of table entry identified by id
POST:  
- takes contents of form, including any user alterations, updates the database, and tables
- returns user to XXXXXX page and notifies them of edited entries

/delete/id  
- using the <id>, delete the selected entry from the database using a query created by SQLAchemey
- update the database and tables
- return the user to the show page, displaying the updated table, paginated

/add  
GET:  
- render form with blank fields  
POST:  
- use contents of form to insert new database entry using a SQLAchemey built query
- update db session and tables
- return user to index page with notification of addition

/filter  
POST:  
- takes values from html form and uses them as input for the SQLAlchemy's filter
- displays resulting values, paginated, using the show page template


Current Known Issues:  
- the edit row item will crash if any field contains an ' (throws off SQL input)
- investigating inconsistent behavior with table persistence differences in locally hosted v. web hosted versions of app
- did not configure database to autoincrement primary key --> currently new entries are assigned a primary key in a very hacky manner
- not crazy about an in repo json with credentials as a means for connection --> try other options
