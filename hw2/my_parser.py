
"""
FILE: skeleton_parser.py
------------------
Author: Firas Abuzaid (fabuzaid@stanford.edu)
Author: Perth Charernwattanagul (puch@stanford.edu)
Modified: 04/21/2014

Skeleton parser for CS564 programming project 1. Has useful imports and
functions for parsing, including:

1) Directory handling -- the parser takes a list of eBay json files
and opens each file inside of a loop. You just need to fill in the rest.
2) Dollar value conversions -- the json files store dollar value amounts in
a string like $3,453.23 -- we provide a function to convert it to a string
like XXXXX.xx.
3) Date/time conversions -- the json files store dates/ times in the form
Mon-DD-YY HH:MM:SS -- we wrote a function (transformDttm) that converts to the
for YYYY-MM-DD HH:MM:SS, which will sort chronologically in SQL.

Your job is to implement the parseJson function, which is invoked on each file by
the main function. We create the initial Python dictionary object of items for
you; the rest is up to you!
Happy parsing!
"""

import sys
from json import loads
from re import sub

columnSeparator = "|"

# Dictionary of months used for date transformation
MONTHS = {'Jan':'01','Feb':'02','Mar':'03','Apr':'04','May':'05','Jun':'06',\
        'Jul':'07','Aug':'08','Sep':'09','Oct':'10','Nov':'11','Dec':'12'}

"""
Returns true if a file ends in .json
"""
def isJson(f):
    return len(f) > 5 and f[-5:] == '.json'

"""
Converts month to a number, e.g. 'Dec' to '12'
"""
def transformMonth(mon):
    if mon in MONTHS:
        return MONTHS[mon]
    else:
        return mon

"""
Transforms a timestamp from Mon-DD-YY HH:MM:SS to YYYY-MM-DD HH:MM:SS
"""
def transformDttm(dttm):
    dttm = dttm.strip().split(' ')
    dt = dttm[0].split('-')
    date = '20' + dt[2] + '-'
    date += transformMonth(dt[0]) + '-' + dt[1]
    return date + ' ' + dttm[1]

"""
Transform a dollar value amount from a string like $3,453.23 to XXXXX.xx
"""

def transformDollar(money):
    if money == None or len(money) == 0:
        return money
    return sub(r'[^\d.]', '', money)


seen_users = set()
seen_cats = set()

users_file = open('Users.dat', 'w')
items_file = open('Items.dat', 'w')
bids_file = open('Bids.dat', 'w')
cats_file = open('ItemCategories.dat', 'w')

def quotes(val): return '"' + str(val).replace('"', '""') + '"'

def user_file_writer(user_id, rating, location, country):
    if user_id not in seen_users:
        seen_users.add(user_id)
        row = columnSeparator.join([
            user_id,
            rating,
            quotes(location),
            quotes(country)
        ])
        users_file.write(row + '\n')

"""
Parses a single json file. Currently, there's a loop that iterates over each
item in the data set. Your job is to extend this functionality to create all
of the necessary SQL tables for your database.
"""
def parseJson(json_file):
    with open(json_file, 'r') as f:
        items = loads(f.read())['Items'] # creates a Python dictionary of Items for the supplied json file
        for item in items:
            """
            TODO: traverse the items dictionary to extract information from the
            given `json_file' and generate the necessary .dat files to generate
            the SQL tables based on your relation design
            """
            item_id = item['ItemID']
            seller = item['Seller']
            seller_id = seller['UserID']
            bids = item.get('Bids') or []

            user_file_writer(
                seller_id,
                seller['Rating'],
                item.get('Location'),
                item.get('Country')
            )

            buy_price = transformDollar(item.get('Buy_Price'))
            row = columnSeparator.join([
                item_id,
                quotes(item['Name']),
                transformDollar(item['Currently']),
                buy_price if buy_price else 'NULL',
                transformDollar(item['First_Bid']),
                item['Number_of_Bids'],
                quotes(item.get('Location')),
                quotes(item.get('Country')),
                quotes(transformDttm(item['Started'])),
                quotes(transformDttm(item['Ends'])),
                quotes(item.get('Description')),
                seller_id
            ])
            items_file.write(row + '\n')

            for category in item.get('Category', []):
                key = (item_id, category)
                if key not in seen_cats:
                    seen_cats.add(key)
                    cat_row = columnSeparator.join([
                        item_id,
                        quotes(category)
                    ])
                    cats_file.write(cat_row + '\n')

            for bid_wrapper in bids:
                bid = bid_wrapper['Bid']
                bidder = bid['Bidder']

                user_file_writer(
                    bidder['UserID'],
                    bidder['Rating'],
                    bidder.get('Location'),
                    bidder.get('Country'),
                )

                bid_row = columnSeparator.join([
                    bidder['UserID'],
                    item_id,
                    quotes(transformDttm(bid['Time'])),
                    transformDollar(bid['Amount'])
                ])
                bids_file.write(bid_row + '\n')

"""
Loops through each json files provided on the command line and passes each file
to the parser
"""
def main(argv):
    if len(argv) < 2:
        print >> sys.stderr, 'Usage: python skeleton_json_parser.py <path to json files>'
        sys.exit(1)

    import glob
    files = []
    for arg in argv[1:]:
        expanded = glob.glob(arg)
        if expanded:
            files.extend(expanded)
        else:
            files.append(arg)
    for f in files:
        if isJson(f):
            parseJson(f)
            print("Success parsing " + f)

    # loops over all .json files in the argument
    # for f in argv[1:]:
      #  if isJson(f):
       #     parseJson(f)
        #    print ("Success parsing " + f)

    users_file.close()
    items_file.close()
    bids_file.close()
    cats_file.close()

if __name__ == '__main__':
    main(sys.argv)
