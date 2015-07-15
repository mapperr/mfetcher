#! /usr/bin/python

import sys
import requests
import json
import os

try:
   usage = "update, fetch <manga_alias> [chapter]"


   if len(sys.argv) > 1:
       command = sys.argv[1]
   else:
      print usage
      sys.exit(2)
  
   if len(sys.argv) > 2:
      manga_name = sys.argv[2]

   if len(sys.argv) > 3:
      chapter = sys.argv[3]
  
   base_mangaeden_url = "https://www.mangaeden.com/api"
   base_images_url = "https://cdn.mangaeden.com/mangasimg"
   database_file = "mangadb.json"


   if command == "update":
      r = requests.get(base_mangaeden_url + "/list/0")
      f = open(database_file,"w")
      f.write(r.text)
      f.close()
      sys.exit(0)


   if command == "fetch":
      
      if manga_name == None:
         print usage
         sys.exit(2)

      with open(database_file) as dbfile:
         data = json.load(dbfile)
      
      manga_id = None
      
      for manga in data["manga"]:
         if manga["a"] == manga_name:
            manga_id = manga["i"]
            break

      if manga_id == None:
         print "[", manga_name, "] not found"
         sys.exit(1)

      r = requests.get(base_mangaeden_url + "/manga/" + manga_id)
      manga_data = r.json()
      chapters_data = manga_data["chapters"]

      try:
         chapter
      except NameError:
         chapter = None

      if chapter != None:
         
         chapter_id = None
         
         for chapter_data in chapters_data:
            if chapter_data[0] == int(chapter):
               chapter_id = chapter_data[3]
               break
         
         if chapter_id == None:
            print "chapter [",chapter,"] not found"
            sys.exit(1)

         r = requests.get(base_mangaeden_url + "/chapter/" + chapter_id)
         images_data = r.json()["images"]
         directory = manga_name + "__" + chapter
         if not os.path.exists(directory):
            os.makedirs(directory)
         for image_data in images_data:
            image_url = image_data[1]
            image_number = image_data[0]
            r = requests.get(base_images_url + "/" + image_url)
            f = open(directory+"/"+str(image_number)+".jpg", "w")
            f.write(r.content)
            f.close()
      else:
         print r.text

      sys.exit(0)
      

#  r = requests.get(base_mangaeden_url + "/0?p=1")
#  for manga in r.json()["manga"]:
#    print manga["a"], "\t", manga["i"]

except SystemExit, e:
   sys.exit(e)

except:
   e = sys.exc_info()[1]
   print e
   sys.exit(1)
