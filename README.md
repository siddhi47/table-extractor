# table-extractor
An adhoc table extractor that i created to scrape tables and throw it into a csv file.


<strong>1 install requirements</strong><br>
	pip install -r requirements.txt (if you do not have pandas and numpy installed)<br>
	pip install -r requirements_mini.txt (if you have pandas and numpy installed) <br>
	(If you are using anaconda version of python, you will have pandas and numpy installed)<br>
  
<strong>2 Create a folder named storage</strong><br>
	mkdir storage

<strong>3 run the code</strong><br>
	python awesomeTableExtractor.py
  
<strong>4 Give Inputs</strong><br>
  You will be prompted to enter the URL, string to match, filename to save the table in, and an offset (optional but highly recommended to use the offset.)

<strong>5 remove temporary files </strong><br>
	python remove.py
