from multiprocessing import Process, Pipe
from craigslist import CraigslistForSale
from bs4 import BeautifulSoup
import time
import math
import requests

sitesHold = ["sfbay", "seattle", "newyork", "boston", "losangeles", "sandiego", "portland", "washingtondc", "chicago",
             "sacramento", "denver", "atlanta", "austin", "vancouver", "philadelphia", "phoenix", "minneapolis",
             "fortlauderdale", "miami", "dallas", "detroit", "houston", "toronto", "lasvegas", "cleveland", "honolulu",
             "stlouis", "kansascity", "neworleans", "nashville", "pittsburgh", "baltimore", "cincinnati", "raleigh",
             "tampa", "providence", "orlando", "buffalo", "charlotte", "columbus", "fresno", "hartford", "indianapolis",
             "memphis", "milwaukee", "norfolk", "montreal", "albuquerque", "anchorage", "boise", "sanantonio",
             "oklahomacity", "omaha", "saltlakecity", "tucson", "louisville", "albany", "richmond", "greensboro",
             "santabarbara", "bakersfield", "auckland", "tulsa", "dublin", "ottawa", "calgary", "edmonton", "winnipeg",
             "jacksonville", "paris", "amsterdam", "reno", "eugene", "spokane", "modesto", "stockton", "desmoines",
             "wichita", "littlerock", "columbia", "monterey", "orangecounty", "inlandempire", "oslo", "copenhagen",
             "brussels", "saopaulo", "buenosaires", "fortmyers", "rochester", "bham", "charleston", "grandrapids",
             "syracuse", "dayton", "elpaso", "lexington", "jackson", "moscow", "rio", "stpetersburg", "marseilles",
             "lyon", "budapest", "jakarta", "santiago", "lima", "telaviv", "jerusalem", "cairo", "madison",
             "harrisburg", "allentown", "newhaven", "maine", "newjersey", "asheville", "annarbor", "westernmass",
             "halifax", "quebec", "saskatoon", "victoria", "caracas", "costarica", "puertorico", "puertorico",
             "tallahassee", "chico", "redding", "humboldt", "chambana", "slo", "montana", "delaware", "wv", "sd", "nd",
             "wyoming", "nh", "batonrouge", "mobile", "ithaca", "knoxville", "pensacola", "toledo", "savannah",
             "shreveport", "montgomery", "ventura", "palmsprings", "cosprings", "lansing", "hamilton", "kitchener",
             "dubai", "medford", "bellingham", "santafe", "gainesville", "chattanooga", "springfield", "columbiamo",
             "rockford", "peoria", "springfieldil", "fortwayne", "evansville", "southbend", "bloomington", "gulfport",
             "huntsville", "salem", "bend", "londonon", "windsor", "sarasota", "daytona", "capecod", "worcester",
             "greenbay", "eauclaire", "appleton", "flagstaff", "micronesia", "micronesia", "yakima", "utica",
             "binghamton", "hudsonvalley", "longisland", "akroncanton", "youngstown", "greenville", "myrtlebeach",
             "duluth", "augusta", "macon", "athensga", "flint", "saginaw", "kalamazoo", "up", "mcallen", "beaumont",
             "corpuschristi", "brownsville", "lubbock", "odessa", "amarillo", "waco", "laredo", "winstonsalem",
             "fayetteville", "wilmington", "erie", "scranton", "pennstate", "reading", "lancaster", "topeka",
             "newlondon", "lincoln", "lafayette", "lakecharles", "merced", "southjersey", "fortcollins", "rockies",
             "roanoke", "charlottesville", "blacksburg", "provo", "fayar", "pakistan", "bangladesh", "beirut",
             "malaysia", "panama", "caribbean", "christchurch", "wellington", "pei", "newfoundland", "cotedazur",
             "quadcities", "easttexas", "nmi", "vietnam", "pueblo", "rmn", "boulder", "westslope", "oregoncoast",
             "eastoregon", "tricities", "kpr", "wenatchee", "collegestation", "killeen", "easternshore", "westmd",
             "keys", "spacecoast", "treasure", "ocala", "lascruces", "eastnc", "outerbanks", "watertown", "plattsburgh",
             "iowacity", "cedarrapids", "siouxcity", "bgky", "columbusga", "bn", "carbondale", "visalia", "lawrence",
             "terrehaute", "cnj", "corvallis", "ogden", "stgeorge", "hiltonhead", "nwct", "altoona", "poconos", "york",
             "fortsmith", "texarkana", "tippecanoe", "muncie", "dubuque", "lacrosse", "abilene", "wichitafalls",
             "lynchburg", "danville", "pullman", "stcloud", "yuma", "tuscaloosa", "auburn", "goldcountry",
             "hattiesburg", "northmiss", "lakeland", "westky", "southcoast", "newbrunswick", "kelowna", "kamloops",
             "nanaimo", "princegeorge", "sudbury", "kingston", "niagara", "thunderbay", "peterborough", "barrie",
             "sherbrooke", "haifa", "salvador", "colombia", "toulouse", "bordeaux", "lille", "strasbourg", "loire",
             "prescott", "roswell", "mankato", "lawton", "joplin", "eastidaho", "jonesboro", "jxn", "valdosta", "ksu",
             "grandisland", "stillwater", "centralmich", "fargo", "mansfield", "limaohio", "athensohio", "charlestonwv",
             "morgantown", "parkersburg", "huntington", "wheeling", "martinsburg", "ames", "boone", "harrisonburg",
             "logan", "sanmarcos", "catskills", "chautauqua", "elmira", "mendocino", "imperial", "yubasutter",
             "fredericksburg", "wausau", "roseburg", "annapolis", "skagit", "hickory", "williamsport", "florencesc",
             "clarksville", "olympic", "dothan", "sierravista", "twinfalls", "galveston", "abbotsford", "whistler",
             "comoxvalley", "reddeer", "lethbridge", "ftmcmurray", "regina", "troisrivieres", "saguenay", "cornwall",
             "guelph", "belleville", "chatham", "soo", "sarnia", "owensound", "territories", "belohorizonte",
             "brasilia", "portoalegre", "recife", "curitiba", "fortaleza", "montpellier", "grenoble", "rennes", "rouen",
             "montevideo", "luxembourg", "quito", "zagreb", "ramallah", "racine", "janesville", "muskegon", "porthuron",
             "smd", "staugustine", "jacksontn", "gadsden", "shoals", "jerseyshore", "panamacity", "monroemi",
             "victoriatx", "mohave", "semo", "waterloo", "farmington", "decatur", "brunswick", "sheboygan", "swmi",
             "sandusky", "bucharest", "accra", "addisababa", "kuwait", "lapaz", "reykjavik", "casablanca", "tunis",
             "kenya", "ukraine", "bulgaria", "guatemala", "managua", "elsalvador", "baghdad", "tehran", "virgin",
             "virgin", "santodomingo", "hat", "peace", "cariboo", "sunshine", "skeena", "yellowknife", "whitehorse",
             "brantford", "thumb", "battlecreek", "monroe", "holland", "northernwi", "swv", "frederick", "onslow",
             "statesboro", "nwga", "albanyga", "lakecity", "cfl", "okaloosa", "meridian", "natchez", "houma", "cenla",
             "nacogdoches", "sanangelo", "delrio", "bigbend", "texoma", "enid", "showlow", "elko", "clovis", "lewiston",
             "moseslake", "missoula", "billings", "bozeman", "helena", "greatfalls", "butte", "kalispell", "bemidji",
             "brainerd", "marshall", "bismarck", "grandforks", "northplatte", "scottsbluff", "cookeville", "richmondin",
             "kokomo", "owensboro", "eastky", "klamath", "juneau", "fairbanks", "kenai", "siouxfalls", "rapidcity",
             "csd", "nesd", "potsdam", "oneonta", "fingerlakes", "glensfalls", "swks", "nwks", "seks", "salina",
             "ottumwa", "masoncity", "fortdodge", "stjoseph", "loz", "kirksville", "quincy", "lasalle", "mattoon",
             "ashtabula", "chillicothe", "zanesville", "tuscarawas", "twintiers", "chambersburg", "meadville",
             "susanville", "siskiyou", "hanford", "santamaria", "winchester", "swva", "eastco"]

results = []


def scan(sites, category, search_keys, conn):
    local_results = []
    for site in sites:
        cl_fs = CraigslistForSale(site=site, category=category, filters={'query': search_keys})
        for result in cl_fs.get_results(sort_by='newest'):
            local_results.append(result)
    conn.send(local_results)
    conn.close()


def confirm_contains(must_include, title):
    must_include = must_include.lower()
    title = title.lower()
    must_include = must_include.split(' ')
    for word in must_include:
        if word not in title:
            return False
    return True


def scan_handler(event, context):
    started_at = time.monotonic()
    print("Running...")
    parent_conn, child_conn = Pipe()
    amount_of_lists = int(event['amount_of_lists'])
    list_length = int(len(sitesHold) / amount_of_lists)
    extra_lists = math.ceil((len(sitesHold) - (amount_of_lists * list_length)) / list_length)
    site_list = []
    list_creator_counter = 0
    site_counter = 0
    for i in range(amount_of_lists + extra_lists):
        site_list.append(sitesHold[list_creator_counter:list_creator_counter + list_length])
        list_creator_counter += list_length
    processes = []
    for i in range(len(site_list)):
        site_counter = site_counter + len(site_list[i])
        processes.append(Process(target=scan, args=(site_list[i], event['category'], event['search_query'], child_conn,)))

    for process in processes:
        process.start()

    for process in processes:
        listings = parent_conn.recv()
        print(f'Process: {process.name}')
        if len(listings) > 0:
            for listing in listings:
                if not event['must_include_title']:
                    print(listing)
                    results.append(listing)
                else:
                    if confirm_contains(event['must_include_words'], listing['name']):
                        print(listing)
                        results.append(listing)

    for process in processes:
        process.join()

    listings = []
    for listing in results:
        if listing['has_image']:
            r = requests.get(listing['url'])
            soup = BeautifulSoup(r.content, features="html.parser")
            image_link = soup.find("div", {"class": "slide first visible"}).img["src"]
        else:
            image_link = ""

        listings.append({"id": listing['id'], "title": listing['name'], "link": listing['url'],
                         "post_date": listing['last_updated'], "price": listing['price'].replace("$", ""),
                         "photo": image_link, "has_image": listing['has_image']})

    total_time_took = time.monotonic() - started_at

    print(f"Results: {listings}")
    print(f"Amount of Results: {len(results)}")
    print(f"Sites processed: {site_counter}")
    print(f'Took {total_time_took} seconds long')

    response = {
        "statusCode": 200,
        "headers": {},
        "body": {"listings": listings}
    }
    return response


if __name__ == "__main__":
    scan_handler(
        {"amount_of_lists": 100, "category": "mca", "search_query": "1975 Honda CB550", "must_include_title": True,
         "must_include_words": "honda 1975"}, {})
