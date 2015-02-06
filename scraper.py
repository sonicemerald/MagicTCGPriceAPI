#
#   Scraping Utilities
#

import urllib
import logging
from collections import OrderedDict

#
#   Retrieves a URL to the card's image as represented by http://magiccards.info
#
def getCardImageURL(cardName, cardSet):
    magicInfoURL = "http://magiccards.info/query?q=" + urllib.quote(cardName)
    if cardSet:
        magicInfoURL += urllib.quote(" e:" + cardSet + "/en")
    htmlFile = urllib.urlopen(magicInfoURL)
    rawHTML = htmlFile.read()
    startURLIndex = rawHTML.find("http://magiccards.info/scans")
    endURLIndex = rawHTML.find("\"", startURLIndex)
    imageURL = rawHTML[startURLIndex:endURLIndex]
    return [imageURL]

#
#   Retrieves a cards current price on Channel Fireball
#
def getCFBPrice(cardName, cardSet):
    cfbURL = "http://store.channelfireball.com/products/search?q=" + urllib.quote(cardName)
    if cardSet:
        cfbURL += " " + urllib.quote(cardSet)
    htmlFile = urllib.urlopen(cfbURL)
    rawHTML = htmlFile.read()    
    tempIndex = rawHTML.find("grid-item-price")
    startPriceIndex = rawHTML.find("$", tempIndex)
    endPriceIndex = rawHTML.find("<", startPriceIndex)
    cfbPrice = rawHTML[startPriceIndex:endPriceIndex]
    return [cfbPrice]

#
#   Retrieves the lowest buy it now price for a card on ebay
#
def getEbayPrice(cardName, cardSet):
    ebayURL = "http://www.ebay.com/sch/i.html?_sacat=0&_sop=15&LH_BIN=1&_nkw=" + urllib.quote(cardName)
    if cardSet:
        ebayURL += urllib.quote(" " + cardSet)
    ebayURL += urllib.quote( " mtg nm")
    logging.info(ebayURL)
    htmlFile = urllib.urlopen(ebayURL)
    rawHTML = htmlFile.read()
    startPriceIndex = rawHTML.find('span  class="g-b">')
    startPriceIndex = rawHTML.find("$", startPriceIndex)
    endPriceIndex = rawHTML.find("<", startPriceIndex)
    lowestBIN = rawHTML[startPriceIndex:endPriceIndex]
    return [lowestBIN]

#
#   Retrieves the low, mid, and high prices of a card as shown on http://tcgplayer.com
#
def getTCGPlayerPrices(cardName, cardSet):
    #   Open the TCGPlayer URL
    tcgPlayerURL = "http://magic.tcgplayer.com/db/magic_single_card.asp?cn=" + urllib.quote(cardName)
    if cardSet:
       tcgPlayerURL += "&sn=" + urllib.quote(cardSet)
    htmlFile = urllib.urlopen(tcgPlayerURL)
    rawHTML = htmlFile.read()

    # Scrape for Normal prices
    normalIndex = rawHTML.find('<b>Normal</b>')

    #   Scrape for the low price
    tempIndex = rawHTML.find(">Low:", normalIndex)
    startLowIndex = rawHTML.find("$", tempIndex)
    endLowIndex = rawHTML.find("<", startLowIndex)

    lowPrice = rawHTML[startLowIndex:endLowIndex]

    #   Scrape for the mid price
    tempIndex = rawHTML.find('>Median:', normalIndex)
    startMidIndex = rawHTML.find("$", tempIndex)
    endMidIndex = rawHTML.find("<", startMidIndex)
    
    midPrice = rawHTML[startMidIndex:endMidIndex]

    #   Scrape for the high price
    tempIndex = rawHTML.find('>High:', normalIndex)
    startHighIndex = rawHTML.find("$", tempIndex)
    endHighIndex = rawHTML.find("<", startHighIndex)
    
    highPrice = rawHTML[startHighIndex:endHighIndex]

    #Scrape for Foil Price
    foilIndex = rawHTML.find('<b>Foil</b>')

    #   Scrape for the mid price
    tempIndex = rawHTML.find('>Median:', foilIndex)
    startMidFoilIndex = rawHTML.find("$", tempIndex)
    endMidFoilIndex = rawHTML.find("<", startMidFoilIndex)
    
    foilPrice = rawHTML[startMidFoilIndex:endMidFoilIndex]

    return [lowPrice, midPrice, highPrice, foilPrice]

def getTCGPlayerSetPrices(cardSet):
    #   Open the TCGPlayer URL
    tcgPlayerURL = "http://magic.tcgplayer.com/db/price_guide.asp?setname="+urllib.quote(cardSet)    
    htmlFile = urllib.urlopen(tcgPlayerURL)
    rawHTML = htmlFile.read()
    setArray = []
    tempIndex = 0
    index = 0
    while tempIndex != -1:
        tempIndex = rawHTML.find("<td width=200", index)
        startNameIndex = rawHTML.find("7>", tempIndex)
        endNameIndex = rawHTML.find("</font>", startNameIndex)
        CardName = rawHTML[startNameIndex:endNameIndex]
        index = endNameIndex

        # Scrape for Rarity
        tempIndex = rawHTML.find("<td width=30", index)
        startRareIndex = rawHTML.find(";", tempIndex)
        endRareIndex = rawHTML.find("</font>", startRareIndex)
        index = endRareIndex
        Rarity = rawHTML[startRareIndex:endRareIndex]

        #   Scrape for the high price
        tempIndex = rawHTML.find("<td width=55", index)
        startHighIndex = rawHTML.find("$", tempIndex)
        endHighIndex = rawHTML.find("</font>", startHighIndex)
        index = endHighIndex
        highPrice = rawHTML[startHighIndex:endHighIndex]

        #   Scrape for the mid price
        tempIndex = rawHTML.find("<td width=55", endHighIndex)
        startMidIndex = rawHTML.find("$", tempIndex)
        endMidIndex = rawHTML.find("</font>", startMidIndex)
        index = endMidIndex
        midPrice = rawHTML[startMidIndex:endMidIndex]

        #   Scrape for the low price
        tempIndex = rawHTML.find("<td width=55", endMidIndex)
        startLowIndex = rawHTML.find("$", tempIndex)
        endLowIndex = rawHTML.find("</font>", startLowIndex)
        index = endLowIndex
        lowPrice = rawHTML[startLowIndex:endLowIndex]

        # old way
        # if ("Token" not in CardName):
        #     if ("Emblem" not in CardName):
        if("T" not in Rarity):
            print CardName + "does not have emblem or token"
            dict = (("name", CardName[8:len(CardName)]), ("low", lowPrice[0:len(lowPrice)-6]), ("med", midPrice[0:len(midPrice)-6]), ("high", highPrice[0:len(highPrice)-6]))
            dict = OrderedDict(dict)
            setArray.append(dict)   
    return setArray
    # return "HI"
