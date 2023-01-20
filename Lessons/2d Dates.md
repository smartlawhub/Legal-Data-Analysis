parsed_date = datetime.strptime(date.text, "%Y-%m-%d")  # Introducing datetime elements ! The function strptime allows you to read a text (first argument), and if it matches the pattern in second argument, you will create a datetime object (parsed_date here).
full_date = parsed_date.strftime("%A %d %B %Y")  # Your datetime object can then be transforme (strftime) into a more pleasant date format, again using a pattern
date.set("date", full_date)  # And this is how you set new attributes into an element

el_to_remove = root.xpath(".//Numero_Role")[0]  # Looking for an element to remove, we'll explain xPath below
el_to_remove.getparent().remove(el_to_remove) # Finally, let's say you want to remove an element, you can do it by finding the parent element and using "remove", passing the element to remove as argument

xml_file.write(file)   # And finally you can save it like this

new_date_el = root.xpath(".//Date_Lecture[@date='" + full_date + "']")  # Notice that this works here only because we set the "full_date" attribute at an earlier stage
