import httplib
import re
import argparse
import ttk
from Tkinter import *
from ttk import *

def open_GUI():
	root= Tk()
	root.title("Crawl UsedVictoria")

	mainframe = ttk.Frame(root, padding="3 3 12 12")
	mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
	mainframe.columnconfigure(0, weight=1)
	mainframe.rowconfigure(0, weight=1)
	    
	url = StringVar()
	depth = StringVar()
	search = StringVar()
	    
	url_entry = ttk.Entry(mainframe, width=7, textvariable=url)
	url_entry.grid(column=2, row=1, sticky=(W,E))
	depth_entry = ttk.Entry(mainframe, width=7, textvariable=depth)
	depth_entry.grid(column=2, row=2, sticky=(W,E))
	search_entry = ttk.Entry(mainframe, width=7, textvariable=search)
	search_entry.grid(column=2, row=3, sticky=(W,E))


	ttk.Label(mainframe, textvariable=url).grid(column=5, row=1, sticky=(W,E))
	ttk.Label(mainframe, textvariable=depth).grid(column=5, row=2, sticky=(W))
	ttk.Label(mainframe, textvariable=search).grid(column=5, row=3, sticky=(W))

	for child in mainframe.winfo_children(): child.grid_configure(padx=5, pady=5)

	url_entry.focus()
	depth_entry.focus()
	search_entry.focus()
	ttk.Button(mainframe, text="searchURL", command=lambda  : searchURL(url.get(),int(depth.get()),search.get())).grid(column=3, row=4, sticky=W)
    
	root.mainloop()
	
	
def searchURL(url1,depth1,search1):
	print(url1)
	print(depth1)
	print(search1)
	processed = []
    # only do http links

	if url1.startswith("http://") and (not url1 in processed):
	        processed.append(url1)
	        url1 = url1.replace("http://", "", 1)
	        
	        # split out the url into host and doc
	        host, path = url1, "/"

	        urlparts = url1.split("/")
	        if len(urlparts) > 1:
	                host = urlparts[0]
	                path = url1.replace(host, "", 1)

	        # make the first request
	        print "crawling host: " + host + " path: " + path
	        conn = httplib.HTTPConnection(host)
	        req = conn.request("GET", path)
	        res = conn.getresponse()

	        # find the links
	        contents = res.read()
	        m = re.findall('href="(/classifieds+.*?)"', contents)
	        
	        if search1 in contents:
	                print "Found " + search1 + " at " + url1

	        print str(depth1) + ": processing " + str(len(m)) + " links"
	        for href in m:
	                # do relative urls
	                if href.startswith("/"):
	                        href = "http://" + host + href

	                # follow the links
	                if depth1:
	                        searchURL(href, depth1-1, search1)
	else:
	        print "skipping " + url1

	
	
if __name__ == "__main__":
	open_GUI()
                        
