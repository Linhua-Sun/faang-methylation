#----------------------------------------------------------------
# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
#
#----------------------------------------------------------------
#authors :
#---------
#	Piumi Francois (francois.piumi@inra.fr)		software conception and development (engineer in bioinformatics)
#	Jouneau Luc (luc.jouneau@inra.fr)		software conception and development (engineer in bioinformatics)
#	Gasselin Maxime (m.gasselin@hotmail.fr)		software user and data analysis (PhD student in Epigenetics)
#	Perrier Jean-Philippe (jp.perrier@hotmail.fr)	software user and data analysis (PhD student in Epigenetics)
#	Al Adhami Hala (hala_adhami@hotmail.com)	software user and data analysis (postdoctoral researcher in Epigenetics)
#	Jammes Helene (helene.jammes@inra.fr)		software user and data analysis (research group leader in Epigenetics)
#	Kiefer Helene (helene.kiefer@inra.fr)		software user and data analysis (principal invertigator in Epigenetics)
#

import os
from string import *
from sys import argv
import re

bismark_log_file = argv[1]

ifh = open(bismark_log_file,'r')

state = 0

while 1:
	line = ifh.readline()
	if not line:
		break

	line = line.rstrip('\n\r')

	pattern = re.search("Final Alignment report",line)
	if pattern:
		state = 1

	pattern2 = re.search("Sequence pairs analysed in total:\t([0-9]+)",line)
	if pattern2:
		totalAnalysed = pattern2.group(1)
	
	pattern3 = re.search("Number of paired-end alignments with a unique best hit:\t([0-9]+)",line)
	if pattern3:
		uniquelyMapped = pattern3.group(1)

	pattern4 = re.search("Mapping efficiency:",line)
	if pattern4:
		line = re.sub("Mapping efficiency:","Mapping efficiency (unique map):",line)


	pattern5 = re.search("Sequence pairs did not map uniquely:\t([0-9]+)",line)
	if pattern5:
		multiMapped = pattern5.group(1)
		mapping_efficiency_all_maps = round(((int(uniquelyMapped) + int(multiMapped)) / float(totalAnalysed))*100,1)
		line = "Mapping efficiency (all maps):" + '\t' + str(mapping_efficiency_all_maps) + '%' +'\n'
	
	
	pattern6 = re.search("Sequence pairs (with no alignments under any condition:|which were discarded because genomic sequence could not be extracted:)",line)
	if pattern6:
		continue

	pattern7 = re.search("^(GA.CT...)",line)
	if pattern7:
		continue

	
	pattern8 = re.search("Number of alignments to .merely theoretical. complementary strands being rejected in total",line)
	if pattern8:
		state = 2


	pattern9 = re.search("Number of sequence pairs with unique best .first. alignment came from the bowtie output:",line)
	if pattern9:
		line = line

	pattern10 = re.search("^$",line)
	if pattern10:
		continue

	
	if state == 1:
		print line

	pattern11 = re.search("^Final Cytosine Methylation Report",line)
	if pattern11:
		line = '\n' + line
		state = 3

	pattern12 = re.search("^Total (un)?methylated",line)
	if pattern12:
		continue

	pattern13 = re.search("Generating pie chart",line)
	if pattern13:
		state = 4

	if state == 3:
		print line


ifh.close()
	
	
