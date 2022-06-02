#!/usr/bin/python3

import sys
import os
import uuid

def make_file(my_uuid, doc_number):
	lines_to_write = [
		"<?xml version=\"1.0\" encoding=\"utf-8\"?>\n",
		"	<RTSZDocument>\n",
		"	  <RoyalDocument>\n",
		"	    <ID>" + str(my_uuid) + "</ID>\n",
		"	    <Name>RENAME ME " + str(doc_number) + "</Name>\n",
		"	    <PositionNr>0</PositionNr>\n",
		"	    <IsExpanded>True</IsExpanded>\n",
		"	    <AutoMergeOption>1</AutoMergeOption>\n",
		"	    <AutoSaveAfterChange>True</AutoSaveAfterChange>\n",
		"	    <AutoSaveOnClose>True</AutoSaveOnClose>\n",
		"	    <ColorFromParent>False</ColorFromParent>\n",
		"	    <DocumentType>Workspace</DocumentType>\n",
		"	    <LockdownFeaturesInUse>{}</LockdownFeaturesInUse>\n",
		"	    <PasswordHash>5DA6DFA33F149E9208E8B6064729EFA7C3B09CB2E3E7C12AB6CEE93121580D53200E13BEFF0EBA66F22942CCEBE814680C1878E62809006A1A5987705B7E2B5E7BBB60F5FB8C63E920DDED2929BF25630D537C9498FE1876D2D9918DB258EB54D9F4EA4766AAF180D44DF8EC3190EF86EF0DC7390D8C09CCE6BE192783123362</PasswordHash>\n",
		"	    <SaveOption>2</SaveOption>\n",
		"	    <StoreFavoritesInUserConfig>True</StoreFavoritesInUserConfig>\n",
		"	    <StoreFolderExpandStateInUserConfig>True</StoreFolderExpandStateInUserConfig>\n",
		"	    <Description />\n",
		"	    <ColorName />\n",
		"	    <Color />\n",
		"	  </RoyalDocument>\n",
		"	</RTSZDocument>"
		]
	return lines_to_write

for i in range (1, 1001):
	filename = "RENAME ME " + str(i) + ".rtsz"
	f = open(filename, "w")
	file_contents = make_file(uuid.uuid4(), i)
	for line in file_contents:
		f.write(line)
	f.close