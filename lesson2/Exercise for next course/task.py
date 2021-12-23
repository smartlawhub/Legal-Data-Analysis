import re
import os
from bs4 import BeautifulSoup
from selenium import webdriver
from collections import Counter, defaultdict
import pandas as pd
import time

codes = {"Code civil": "codes/texte_lc/LEGITEXT000006070721?etatTexte=VIGUEUR&etatTexte=VIGUEUR_DIFF"}

data_scrapped = []

#Answer Here
